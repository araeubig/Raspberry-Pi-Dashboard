import logging
import os
import psutil
import subprocess
import sys
import time
import datetime
import netifaces
import threading
import socket
import gettext

import settings

from collections import deque
from PIL import Image, ImageDraw, ImageFont
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError

from display.LCD_TOUCH_Waveshare_1inch69 import LCD_1inch69
from display.LCD_TOUCH_Waveshare_1inch69 import Touch_1inch69

# Raspberry Pi pin configuration:
RST    = 27
DC     = 25
BL     = 18
TP_INT = 4
TP_RST = 17

# Set the local directory
appname = 'rpidashboard'
localedir = './locales'

# Set up Gettext
en_i18n = gettext.translation(appname, localedir, fallback=True, languages=['en'])
_ = en_i18n.gettext

# Create the translation function
en_i18n.install()

# Font sizes and font type
# https://www.github.com/adobe-fonts/source-code-pro
background_color = '#000000'
line_color = '#1f1f1f'
menu_size = 16
menu_color = '#b8b8b8'
menu_font = ImageFont.truetype('./fonts/SourceCodePro-Light.ttf', menu_size)
pagenumber_size = menu_size / 3 * 2
pagenumber_color = '#b8b8b8'
pagenumber_font = ImageFont.truetype('./fonts/SourceCodePro-Light.ttf', pagenumber_size)
header_size = 12
header_color = '#737373'
header_font = ImageFont.truetype('./fonts/SourceCodePro-Light.ttf', header_size)
value_size = 28
value_color = '#b8b8b8'
value_font = ImageFont.truetype('./fonts/SourceCodePro-Regular.ttf', value_size)
value_half_size = value_size / 2
value_half_font = ImageFont.truetype('./fonts/SourceCodePro-Regular.ttf', value_half_size)

testvar = 17

# Define logging level
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# Define touch callback
def touch_callback(TP_INT):
    global Flag, released, test
    if touch_mode == 1:       
        touch.get_point()
    elif touch_mode == 2:
        touch.Gestures = touch.Touch_Read_Byte(0x01)
        touch.get_point()
    else:
        touch.Gestures = touch.Touch_Read_Byte(0x01)

def set_display():
    global disp
    # Display with hardware SPI:
    disp = LCD_1inch69.LCD_1inch69(rst = RST,dc = DC,bl = BL,tp_int = TP_INT,tp_rst = TP_RST,bl_freq=100)
    # Initialize lcd library.
    disp.Init()
    # Clear display.
    disp.clear()
    # Set the backlight to 100
    disp.bl_DutyCycle(100)

def set_touch():
    global touch, touch_mode
    # Set touch mode
    touch_mode = 2
    # Touch with hardware I2C
    touch = Touch_1inch69.Touch_1inch69()
    # Initialize touch library.
    touch.init()
    # Set touch mode
    touch.Set_Mode(touch_mode)
    # Define callback for touch events
    touch.GPIO_TP_INT.when_pressed = touch_callback

set_display()
set_touch()


# Set display orientation, for landscape: landscape = True
landscape = True
if disp.height > disp.width and landscape == True:
    image_width = disp.height
    image_height = disp.width
else:
    image_width = disp.width
    image_height = disp.height

def main():
    logging.info('Start dashboard application')

    global skip
    global do_reboot
    global testvar

    do_reboot = None

    # Get IP adress and set active network interface for later use
    get_ip_address()

    # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
    global transfer_rate
    transfer_rate = deque(maxlen=1)
    t = threading.Thread(target=calc_ul_dl, args=(1,net_interface))

    # The program will exit if there are only daemonic threads left.
    t.daemon = True
    t.start()

    # Show startup screen
    show_startup()

    # Start tasks one time before loop to normalize data
    high_frequency_tasks()
    medium_frequency_tasks()
    # low_frequency_tasks()
    onetime_frequency_tasks()

    try:
        # Get the current time (in seconds)
        next_time = time.time() + 1
        # Set base variables to starting values
        skip = 0
        page = 1
        do_reboot = ''
        timeout = settings.timeout

        logging.info('Entering loop')

        while True:
            try:
                # Reset screensaver by gesture
                if timeout == 0 and touch.Gestures != 0 and touch.Gestures != None:
                    timeout = settings.timeout
                    page = 1
                # Detect gesture
                if touch.Gestures == 0x0B:
                    logging.debug('DOUBLE KLICK')
                elif touch.Gestures == 0x0C:
                    logging.debug('LONG PRESS')
                elif touch.Gestures == 0x01:
                    logging.debug('RIGHT')
                elif touch.Gestures == 0x02:
                    logging.debug('LEFT')
                elif touch.Gestures == 0x03:
                    logging.debug('DOWN') 
                    if page >= 2 and page <= 4:
                        page -= 1
                    elif page == 1:
                        page = 4
                elif touch.Gestures == 0x04:
                    logging.debug('UP')
                    if page >= 1 and page <= 3:
                        page += 1
                    elif page == 4:
                        page = 1
                elif touch.Gestures == 0x05:
                    logging.debug('KLICK')

                # print(touch.X_point)
                # print(touch.Y_point) # 40-218 NO # 40-30 YES
                
                # Clear last gesture
                touch.Gestures = touch.Touch_Write_Byte(0x01, 0)

                if timeout == 0:
                    page = 0
                    # Show alive
                    
                logging.debug('Page: %i', page)

                # Do every second
                high_frequency_tasks()
                # Do every 10th second
                if skip % 10 == 0:
                    medium_frequency_tasks()
                # Do every 30th second
                if skip % 30 == 0:
                    low_frequency_tasks()
                # Do every 5 minutes
                if skip % 60 == 0 and settings.log == True : #300
                    log_frequency_tasks()

                # Set screen content based on status
                if timeout == 0 and page == 0:
                    show_alive()
                if timeout != 0 and page == 1:
                    show_dashboard()
                elif timeout != 0 and page == 2:
                    show_systeminfo()
                elif (timeout != 0 and
                      page == 3 and
                     (touch.X_point > 20 and
                      touch.X_point < 60) and
                     (touch.Y_point > 155 and
                      touch.Y_point < 250)):
                        print('No')
                        page = 1
                        testvar = 99
                elif (timeout != 0 and
                      page == 3 and
                     (touch.X_point > 20 and
                      touch.X_point < 60) and
                     (touch.Y_point > 30 and
                      touch.Y_point < 125)):
                        print('Yes')
                        # os.system('systemctl reboot -i')
                        subprocess.run(["reboot", "-i"])
                        # subprocess.run(["shutdown", "now"])
                        testvar = 300
                elif (timeout != 0 and
                      page == 3):
                        show_reboot()
                elif timeout != 0 and page == 4:
                    show_shutdown()

                # Incremet loop counter
                skip += 1
                # Decrement timeout counter
                if timeout > 0:
                    timeout -= 1
                logging.debug('Timeout: %s', timeout)

                # Wait until the next call
                time.sleep(max(0, next_time - time.time()))
                next_time += (time.time() - next_time) // 1 * 1 + 1

            except Exception as error:
                logging.error("An exception occurred: " + type(error).__name__)
                time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Loop interrupted by user")

    except Exception as error:
        logging.error("An exception occurred: " + type(error).__name__)

    logging.info('End forever loop')
    logging.info('End dashboard application')

def show_startup():
    logging.debug("show_startup()")

    # Create start image for drawing.
    source = './images/logo_raspberry_' + str(image_width) + '_' + str(image_height) + '.png'
    image1 = Image.open(source)
    draw = ImageDraw.Draw(image1)
    draw.text((image_width / 2,image_height - (header_size * 2 )), _('   Starting dashboard...'), fill='BLACK', font=header_font, anchor="mm")

    disp.ShowImage(image1)
    if is_running_as_service():
        splash_time = 10
    else:
        splash_time = 5

    time.sleep(splash_time - 1)

def show_dashboard():
    logging.debug("show_dashboard()")

    # Set backlight to 100%
    disp.bl_DutyCycle(100)

    # Draw background
    image1 = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image1)

    # Draw vertical lines
    draw.line(
        [
            (image_width / 3, 0),
            (image_width / 3, image_height)
        ],
        fill=line_color,
        width=2,
        joint=None
    )
    draw.line(
        [
            (image_width / 3 * 2, 0),
            (image_width / 3 * 2, image_height)
        ],
        fill=line_color,
        width=2,
        joint=None
    )

    # Draw horizontal lines
    draw.line(
        [
            (0, image_height / 3),
            (image_width, image_height / 3)
        ],
        fill=line_color,
        width=2,
        joint=None
    )
    draw.line(
        [
            (0, image_height / 3 * 2),
            (image_width, image_height / 3 * 2)
        ],
        fill=line_color,
        width=2,
        joint=None
    )

    # Tile: RAM use in percent
    row = 1
    column = 1

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'RAM %',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2
        ),
        f'{int(mem.percent)}',
        fill=f'{value_to_hex_color(int(mem.percent))}',
        font=value_font,
        anchor="mm"
    )

    # Tile: CPU use in percent
    row = 1
    column = 2

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'CPU %',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + (header_size / 2)
        ),
        f'{int(cpu_percent)}',
        fill=f'{value_to_hex_color(int(cpu_percent))}',
        font=value_font,
        anchor="mm"
    )

    # Tile: Disk use in percent (boot drive)
    row = 1
    column = 3

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'SSD %',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2
        ),
        f'{int(disk.percent)}',
        fill=f'{value_to_hex_color(int(disk.percent))}',
        font=value_font,
        anchor="mm"
    )

    # Tile: SWAP use in percent
    row = 2
    column = 1

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'SWAP %',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2),
            f'{int(swap.percent)}',
            fill=f'{value_to_hex_color(int(swap.percent))}',
            font=value_font,
            anchor="mm"
        )

    # Tile: CPU temperature
    row = 2
    column = 2

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'CPU °C',
        fill=header_color,
        font=header_font,
        anchor="mt"
    
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2
        ),
        f'{int(cpu_temp)}',
        fill=f'{value_to_hex_color(int(cpu_temp), 45)}',
        font=value_font,
        anchor="mm"
    )

    # Tile: SSD temperature
    row = 2
    column = 3

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'SSD °C',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2
        ),
        f'{int(ssd_temp)}',
        fill=f'{value_to_hex_color(int(ssd_temp))}',
        font=value_font,
        anchor="mm"
    )

    # Tile: Influx
    row = 3
    column = 1

    if influx_status == True:
        influx_value_color = value_color
    else:
        influx_value_color = 'RED'

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        f'INFLUX {get_influx_range()}',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2
        ),
        f'{int(influx_meas)}',
        fill=influx_value_color,
        font=value_font,
        anchor="mm"
    )
    # Test for text information at field bottom. Requires layout change of value to the real middle
    # draw.text(
    #     (
    #         (image_width / 3 * column) - (image_width / 3 / 2),
    #         (image_height / 3 * (row) - (header_size / 2))
    #     ),
    #     'LOG: OFF',
    #     fill=header_color,
    #     font=header_font,
    #     anchor="mb"
    # )
    
    # Tile: Grafana
    row = 3
    column = 2

    if grafana_status == True:
        grafana_value_color = value_color
        grafana_value = u"✓"
    else:
        grafana_value_color = 'RED'
        grafana_value = "x"

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        'GRAFANA',
        fill=header_color,
        font=header_font,
        anchor="mt"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2
        ),
        grafana_value,
        fill=grafana_value_color,
        font=value_font,
        anchor="mm"
    )

    # Tile: Network transfer
    row = 3
    column = 3

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (header_size / 2))
        ),
        net_interface.upper(),
        fill=header_color,
        font=header_font,
        anchor="mt"
    )

    if net_d >= 100 or net_u >= 100:
        draw.text(
            (
                (image_width / 3 * column) - (image_width / 3 / 2),
                (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 - (value_half_size / 2 )
            ),
            f"D:{net_d:4.0f}",
            fill=value_color,
            font=value_half_font,
            anchor="mm"
        )
        draw.text(
            (
                (image_width / 3 * column) - (image_width / 3 / 2),
                (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 + (value_half_size / 2 )
            ),
            f"U:{net_u:4.0f}",
            fill=value_color,
            font=value_half_font,
            anchor="mm"
        )
    else:
        draw.text(
            (
                (image_width / 3 * column) - (image_width / 3 / 2),
                (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 - (value_half_size / 2 )
            ),
            f"D:{net_d:4.1f}",
            fill=value_color,
            font=value_half_font,
            anchor="mm"
        )
        draw.text(
            (
                (image_width / 3 * column) - (image_width / 3 / 2),
                (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 + (value_half_size / 2 )
            ),
            f"U:{net_u:4.1f}",
            fill=value_color,
            font=value_half_font,
            anchor="mm"
        )

    # Show image
    disp.ShowImage(image1)

def show_systeminfo():
    logging.debug("show_systeminfo()")


    row = 1
    column = 2
    menu_text = 'Info'
    page_number = '2/4'
    image1 = Image.new(
        "RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image1)

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (menu_size / 2))
        ),
        menu_text.upper(),
        fill=menu_color,
        font=menu_font,
        anchor="mt"
    )

    row = 3

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row - (pagenumber_size / 2))
        ),
        page_number,
        fill=menu_color,
        font=pagenumber_font,
        anchor="mb"
    )
    
    row = 1

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 # - (value_half_size / 2 )
        ),
        f'{hostname}.local',
        fill=f'{value_to_hex_color(int(mem.percent))}',
        font=value_font,
        anchor="mm"
    )

    row = 2

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) # + header_size / 2 # + (value_half_size / 2 )
        ),
        f'{ip_address}',
        fill=f'{value_to_hex_color(int(mem.percent))}',
        font=value_font,
        anchor="mm"
    )

    row = 3

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 - (value_half_size / 2 )
        ),
        f'{model}',
        fill=f'{value_to_hex_color(int(mem.percent))}',
        font=value_half_font,
        anchor="mm"
    )
    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * row) - (image_height / 3 / 2) + header_size / 2 + (value_half_size / 2 )
        ),
        _('with') + f' {ram}' + 'MB RAM',
        fill=f'{value_to_hex_color(int(mem.percent))}',
        font=value_half_font,
        anchor="mm"
    )
    
    disp.ShowImage(image1)

def show_reboot():
    logging.debug("show_reboot()")

    # global do_reboot


    print(testvar)

    # if state == 'Y':
    #     color_state_yes = 'GREEN'
    #     color_state_no = header_color
    # elif state == 'N':
    #     color_state_yes = header_color
    #     color_state_no = 'GREEN'
    # elif state == 'E':
    color_state_yes = header_color
    color_state_no = header_color


    row = 1
    column = 2
    menu_text = 'Reboot'
    page_number = '3/4'
    image1 = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image1)

    draw.text(
        (
            (image_width / 3 * column) - (image_width / 3 / 2),
            (image_height / 3 * (row - 1) + (menu_size / 2))
        ),
        menu_text.upper(),
        fill=menu_color,
        font=menu_font,
        anchor="mt"
    )

    row = 3

    draw.text(
        ((image_width / 3 * column) - (image_width / 3 / 2),(image_height / 3 * row - (pagenumber_size / 2))), page_number, fill=menu_color, font=pagenumber_font, anchor="mb")

    draw.rounded_rectangle([(30,170),(125,210)], radius=2.5, fill=color_state_yes, outline=None, width=1)
    draw.text((77.5,190), _('Yes'), fill=value_color, font=menu_font, anchor="mm")
    draw.rounded_rectangle([(155,170),(250,210)], radius=2.5, fill=color_state_no, outline=None, width=1)
    draw.text((202.5,190), _('No'), fill=value_color, font=menu_font, anchor="mm")

    disp.ShowImage(image1)

def show_shutdown():
    logging.debug("show_shutdown()")

    row = 1
    column = 2
    menu_text = 'Shutdown'
    page_number = '4/4'
    image1 = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image1)
    draw.text(((image_width / 3 * column) - (image_width / 3 / 2),(image_height / 3 * (row - 1) + (menu_size / 2))), menu_text.upper(), fill=menu_color, font=menu_font, anchor="mt")
    row = 3
    draw.text(((image_width / 3 * column) - (image_width / 3 / 2),(image_height / 3 * row - (pagenumber_size / 2))), page_number, fill=menu_color, font=pagenumber_font, anchor="mb")

    # draw.rounded_rectangle([(30,170),(125,210)], radius=2.5, fill=color_state, outline=None, width=1)
    # draw.text((77.5,190), _('Yes'), fill=value_color, font=menu_font, anchor="mm")
    # draw.rounded_rectangle([(155,170),(250,210)], radius=2.5, fill=color_state, outline=None, width=1)
    # draw.text((202.5,190), _('No'), fill=value_color, font=menu_font, anchor="mm")

    disp.ShowImage(image1)

def show_alive():
    logging.debug("show_alive()")

    row = 2
    column = 2

    # Reduce backlight to minimum
    disp.bl_DutyCycle(5)

    image1 = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image1)
    text = u"●"
    if (skip % 2) == 0:
        draw.text(((image_width / 3 * column) - (image_width / 3 / 2),(image_height / 3 * row) - (image_height / 3 / 2)), text, fill="WHITE", font=value_font, anchor="mm")

    disp.ShowImage(image1)

def check_ip(host,port,timeout=2):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably
    sock.settimeout(timeout)
    try:
       sock.connect((host,port))
    except:
       return False
    else:
       sock.close()
       return True

def get_percent_cpu():
    percent = psutil.cpu_percent()
    return percent

def get_temperature_cpu():
    temps = psutil.sensors_temperatures()
    if not temps:
        logging.error("w: sensors_temperatures not supported")
        return 0
    try:
        temp = temps[next(iter(temps))][0].current #cpu_thermal
    except KeyError:
        temp = 0
    return temp

def get_temperature_ssd(num):
    cmd = 'sudo nvme smart-log /dev/nvme' + str(num)
    data = os.popen(cmd)
    res = data.read()
    for item in res.split("\n"):
        if "temperature" in item:
            ssd_temp = item.strip().split(':')[1].split(" ")[1][:-2]
    if ssd_temp == '':
        ssd_temp = '0'
    return float(ssd_temp)

def get_influx_range():
    # global influx_range_hours

    try:
        if settings.influx_range_hours is None:
            print("is none")
            hours = -24
        else:
            hours = settings.influx_range_hours
    except NameError:
        print("not set")
        hours = -24

    if hours > -24:
        range = str(hours) + _('h')
        return range
    else:
        value = hours / 24
        if int(value) == value:
            y = int(value)
        else:
            y = value
        range = str(int(y)) + _('d')
        return range

def get_influx_meas():
    if check_status_influx() == False:
        return 0

    p = {"_start": datetime.timedelta(hours= settings.influx_range_hours), "_bucket": settings.influx_bucket_read}
    host = "http://" + settings.influx_host + ":" + str(settings.influx_port)
    with InfluxDBClient(url=host, token=settings.influx_token, org=settings.influx_org, debug=False) as client:
        try:
            query_api = client.query_api()

            tables = query_api.query('''
                from(bucket: _bucket) |> range(start: _start)
                    |> group(columns: ["_start"])
                    |> count()
            ''', params=p)

            if tables:
                for table in tables:
                    for record in table.records:
                        value = record.values['_value']
            elif not tables:
                value = 0
        except InfluxDBError as e:
            if e.response.status == 401:
                raise Exception(f"Insufficient read permissions to 'my-bucket'.") from e
            raise
    return value

def check_status_influx():
    global influx_status
    influx_status = check_ip(settings.influx_host, settings.influx_port)
    return influx_status

def create_influx_meas():
    logging.debug("create_influx_meas()")

    if check_status_influx() == False or settings.log == False:
        return 0
    
    host = "http://" + settings.influx_host + ":" + str(settings.influx_port)

    client = InfluxDBClient(url=host, token=settings.influx_token, org=settings.influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    _point1 = Point("Decimal").tag("sensor_id", "CPU").field(_("Temperature"), cpu_temp)
    _point2 = Point("Decimal").tag("sensor_id", "CPU").field(_("Usage"), cpu_percent)
    _point3 = Point("Decimal").tag("sensor_id", "SSD").field(_("Temperature"), ssd_temp)
    _point4 = Point("Decimal").tag("sensor_id", "RAM").field(_("Usage"), mem.percent)
    _point5 = Point("Decimal").tag("sensor_id", "RAM").field(_("Usage MB"), round(mem.used / 1024 / 1024 / 1024, 2))
    _point6 = Point("Decimal").tag("sensor_id", "SSD").field(_("Usage"), disk.percent)

    write_api.write(bucket=settings.influx_bucket_write, record=[_point1,_point2,_point3,_point4,_point5,_point6])

    client.close()

def check_status_grafana():
    global grafana_status
    grafana_status = check_ip(settings.grafana_host, settings.grafana_port)
    return grafana_status

def high_frequency_tasks():
    logging.debug("high_frequency_tasks()")

    global cpu_percent
    global cpu_temp

    cpu_percent = get_percent_cpu()
    cpu_temp = get_temperature_cpu()

def medium_frequency_tasks():
    logging.debug("medium_frequency_tasks()")

    global mem
    global swap
    global ssd_temp

    mem = psutil.virtual_memory()   
    swap = psutil.swap_memory()
    ssd_temp = get_temperature_ssd(0)

def low_frequency_tasks():
    logging.debug("low_frequency_tasks()")

    global disk
    global disk_free_tb
    global influx_meas

    # ToDo: Check and set it at start for optimization.
    if os.path.exists("/mnt/storage/") and os.path.isdir("/mnt/storage/"):
        disk = psutil.disk_usage("/mnt/storage/")
    else:
        disk = psutil.disk_usage("/home/")

    disk_free_tb = disk.used / 1024 / 1024 / 1024 / 1024

    influx_meas = get_influx_meas()
    create_influx_meas()

    check_status_grafana()

def log_frequency_tasks():
    logging.debug("log_frequency_tasks()")
    
    create_influx_meas()

def onetime_frequency_tasks():
    logging.debug("onetime_frequency_tasks()")

    global hostname
    global model
    global ram

    hostname = socket.gethostname()
    model = get_raspberry_model()
    ram = int(round(mem.total / 1024 / 1024 / 1000, 0))

def value_to_hex_color(value, base=50):
    if value < base:
        return value_color
    else:
        pct = value / 100
        pct_diff = 1.0 - pct
        green_color = int(min(255, pct_diff*2 * 255))
        red_color = int(min(255, pct*2 * 255))
        blue_color = 0

    return f'#{red_color:02x}{green_color:02x}{blue_color:02x}'

def get_ip_address():
    """
    Get the local IP address, prioritizing Ethernet over WiFi.

    Returns:
        str: The local IP address or None if no IP address is found.
    """
    interfaces = ['eth0', 'wlan0']
    for interface in interfaces:
        try:
            addresses = netifaces.ifaddresses(interface)
            ip_info = addresses.get(netifaces.AF_INET)
            if ip_info:
                global ip_address
                ip_address = ip_info[0]['addr']
                if ip_address and not ip_address.startswith("127."):
                    global net_interface, ip_adress
                    net_interface = interface
                    # return ip_address
        except ValueError:
            continue
    return None

def get_raspberry_model() -> str:
    with open('/proc/device-tree/model') as f:
        model = f.read()
        model = model[:-1]
        return model

def calc_ul_dl(dt=1, interface="eth0"):
    try:
        t0 = time.time()
        counter = psutil.net_io_counters(pernic=True)[interface]
        tot = (counter.bytes_sent, counter.bytes_recv)

        global net_u, net_d
        while True:
            last_tot = tot
            time.sleep(dt)
            counter = psutil.net_io_counters(pernic=True)[interface]
            t1 = time.time()
            tot = (counter.bytes_sent, counter.bytes_recv)
            ul, dl = [
                (now - last) / (t1 - t0) / 1000.0
                for now, last in zip(tot, last_tot)
            ]
            net_u = ul / 1024 * 8
            net_d = dl / 1024 * 8
            t0 = time.time()
    except Exception as error:
        logging.error("An exception occurred: " + type(error).__name__)

def is_running_as_service():
    state = subprocess.call(["systemctl", "is-active", "--quiet", "rpidashboard"])
    if state == 0:
        return True
    else:
        return False

def check_python_version():
    required_version = (3, 8)
    current_version = sys.version_info[:3]

    if current_version > required_version:
        return True
    else:
        return False

def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo:
                return True
    except FileNotFoundError:
        return False
    return False

def is_spi_enabled():
    spi_devices = ["/dev/spidev0.0", "/dev/spidev0.1", "/dev/spidev1.0", "/dev/spidev1.1"]
    for device in spi_devices:
        if os.path.exists(device):
            return True
    return False

def is_spi_enabled_config():
    try:
        with open('/boot/firmware/config.txt', 'r') as f:
            config = f.read()
            if 'dtparam=spi=on' in config:
                return True
    except FileNotFoundError:
        return False
    return False

def is_i2c_enabled():
    i2c_devices = ["/dev/i2c-1"]
    for device in i2c_devices:
        if os.path.exists(device):
            return True
        return False

def is_i2c_enabled_config():
    try:
        with open('/boot/firmware/config.txt', 'r') as f:
            config = f.read()
            if 'dtparam=i2c_arm=on' in config:
                return True
    except FileNotFoundError:
        return False
    return False

if __name__ == '__main__':
    if check_python_version():
        if is_raspberry_pi():
            if is_spi_enabled() or is_spi_enabled_config():
                if is_i2c_enabled() or is_i2c_enabled_config():
                    main()
                    # print("main")
                else:
                    sys.exit("I2C is not enabled on Raspberry Pi")
            else:
                sys.exit("SPI is not enabled on Raspberry Pi")
        else:
            sys.exit("Only Raspberry Pi is supported")
    else:
        sys.exit("Python version is not greater than 3.8")
