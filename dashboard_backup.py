
def main():
    logging.info('Start dashboard application')

    def Int_Callback(TP_INT):
        global Flag, released, test
        if touch_mode == 1:       
            Flag = 1
            touch.get_point()
            
        elif touch_mode == 2:
            Flag = 1
            touch.Gestures = touch.Touch_Read_Byte(0x01)
            touch.get_point()
        else:
            touch.Gestures = touch.Touch_Read_Byte(0x01)
    
    # Display with hardware SPI:
    disp = LCD_1inch69.LCD_1inch69(rst = RST,dc = DC,bl = BL,tp_int = TP_INT,tp_rst = TP_RST,bl_freq=100)
    # Initialize lcd library.
    disp.Init()
    # Clear display.
    disp.clear()
    # Set the backlight to 100
    disp.bl_DutyCycle(100)

    # Define touch mode to gestures
    touch_mode = 2
    # Touch with hardware I2C
    touch = Touch_1inch69.Touch_1inch69()
    # Initialize touch library.
    touch.init()
    # Set touch mode
    touch.Set_Mode(touch_mode)
    # Define callback for touch events
    touch.GPIO_TP_INT.when_pressed = Int_Callback

    # Use display in landscape format by switching height and with.
    global image_width, image_height
    image_width = disp.height
    image_height = disp.width

    # Create start image for drawing.
    source = './images/logo_raspberry_' + str(image_width) + '_' + str(image_height) + '.png'
    image1 = Image.open(source)
    draw = ImageDraw.Draw(image1)
    # draw.text((image_width / 2,image_height - (font_header_size * 2 )), _('   Starting dashboard...'), fill='BLACK', font=font_header, anchor="mm")

    disp.ShowImage(image1)
    if is_running_as_service():
        splash_time = 10
    else:
        splash_time = 5
    time.sleep(splash_time - 1)

    # Get IP adress and set active network interface for later use
    get_raspberry_ip()

    # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
    global transfer_rate
    transfer_rate = deque(maxlen=1)
    global net_interface
    t = threading.Thread(target=calc_ul_dl, args=(1,net_interface))

    # The program will exit if there are only daemonic threads left.
    t.daemon = True
    t.start()

    # Run tasks to get first data
    low_frequency_tasks()
    high_frequency_tasks()
    medium_frequency_tasks()
    one_time_tasks()

    time.sleep(1)

    global skip

    try:
        # Get the current time (in seconds)
        next_time = time.time() + 1
        # Set base variables to starting values
        skip = 0
        page = 0
        timeout = screensaver

        logging.info('Entering loop')

        while True:
            try:
                # print(touch.X_point)
                # print(touch.Y_point)
                if timeout != 0 and touch.Gestures == 0x0B:
                    logging.debug('DOUBLE KLICK')
                elif timeout == 0 and touch.Gestures == 0x0C:
                    timeout = screensaver
                    disp.bl_DutyCycle(100)
                    logging.debug('LONG PRESS')
                    touch.Gestures = touch.Touch_Write_Byte(0x01, 0)
                    page = 0
                elif timeout != 0 and touch.Gestures == 0x01:
                    logging.debug('RIGHT')
                    touch.Gestures = touch.Touch_Write_Byte(0x01, 0)
                elif timeout != 0 and touch.Gestures == 0x02:
                    logging.debug('LEFT')
                    touch.Gestures = touch.Touch_Write_Byte(0x01, 0)
                elif timeout != 0 and touch.Gestures == 0x03:
                    timeout = screensaver
                    logging.debug('DOWN')
                    touch.Gestures = touch.Touch_Write_Byte(0x01, 0)
                    if page > 0 and page < 4:
                        page -= 1
                    logging.debug('Page: %i', page)
                elif timeout != 0 and touch.Gestures == 0x04:
                    timeout = screensaver
                    logging.debug('UP')
                    touch.Gestures = touch.Touch_Write_Byte(0x01, 0)
                    if page >= 0 and page <= 2:
                        page += 1
                    logging.debug('Page: %i', page)
                elif timeout != 0 and (page == 2 or page == 3) and (
                        touch.X_point > 20 and
                        touch.X_point < 60
                    ) and (
                        touch.Y_point > 155 and
                        touch.Y_point < 250
                    ):
                    page = 0
                elif timeout != 0 and page == 2 and (
                        touch.X_point > 20 and
                        touch.X_point < 60
                    ) and (
                        touch.Y_point > 30 and
                        touch.Y_point < 125
                    ):
                    page = 22
                    # state = True
                    os.system('systemctl reboot -i')
                

                if timeout != 0 and page == 0:
                    # Do every second
                    high_frequency_tasks()
                    # Do every 10th second
                    if skip % 10 == 0:
                        medium_frequency_tasks()
                    # Do every 30th second
                    if skip % 30 == 0:
                        low_frequency_tasks()
                    # Do every 5 minutes
                    if skip % 300 == 0:
                        logging_frequency_tasks()
                    # Show dashboard
                    show_stats(disp)
                elif timeout != 0 and page == 1:
                    show_systeminfo(disp)
                elif timeout != 0 and page == 2:
                    show_reboot(disp)
                # elif timeout != 0 and page == 2 and state == True:
                #     show_reboot(disp, True)    
                # elif timeout != 0 and page == 3:
                #     show_shutdown(disp)
                
                if timeout == 0:
                    show_alive(disp)
                
                skip += 1
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

    logging.info('Hardware Monitor End')

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

def get_temperature_cpu():
    """
    Retrieves the current CPU temperature using the psutil library.

    This function utilizes the `psutil.sensors_temperatures` method to fetch temperature
    sensor data from the system. If the sensors are not supported or an error occurs,
    it logs the issue and returns a default value of 0.

    Returns:
        float: The current CPU temperature in degrees Celsius. Returns 0 if sensor
               data is not available or an error occurs.

    Raises:
        KeyError: If the temperature data structure does not contain the expected keys.
                  This is caught and handled within the function.
    """
    temps = psutil.sensors_temperatures()
    if not temps:
        logging.error("w: sensors_temperatures not supported")
        return 0

    try:
        cpu_temp = temps[next(iter(temps))][0].current #cpu_thermal
    except KeyError:
        cpu_temp = 0

    return cpu_temp

def get_cooler_pwm():
    # cat /sys/devices/platform/cooling_fan/hwmon/*/pwm1
    # cat /sys/devices/platform/cooling_fan/hwmon/*/fan1_input

    # state = subprocess.call(["systemctl", "is-active", "--quiet", "rpidashboard"])

    # value = subprocess.call(["cat /sys/devices/platform/cooling_fan/hwmon/*/pwm1"])

    # cmd = 'cat /sys/devices/platform/cooling_fan/hwmon/*/pwm1'
    # data = os.popen(cmd)
    # res = data.read()
    # percent = round(float((int(res) / 255) * 100))

    # cooler = {'org': res, 'percent': percent, 'rpm': 127}

    # value_percent = float((value / 255) * 100)

    # rpm = psutil.sensors_fans()

    # print(rpm)
    # print(res)
    # print(percent)
    # print(cooler.rpm)
    # print(value_percent)

    return 100

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
    global influx_range_hours

    if influx_range_hours > -24:
        range = str(influx_range_hours) + _('h')
        return range
    else:
        value = influx_range_hours / 24
        if int(value) == value:
            y = int(value)
        else:
            y = value
        range = str(y) + _('d')
        return range

def get_influx_measurements():
    global influx_range_hours

    if check_status_influx() == False:
        return 0

    p = {"_start": datetime.timedelta(hours= influx_range_hours)}
    host = "http://" + influx_host + ":" + str(influx_port)
    with InfluxDBClient(url=host, token=influx_token, org=influx_org, debug=False) as client:
        try:
            query_api = client.query_api()

            tables = query_api.query('''
                from(bucket:"X1-TEST") |> range(start: _start)
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
                raise Exception(f"Insufficient write permissions to 'my-bucket'.") from e
            raise
    return value

def create_influx_data():

    host = "http://" + influx_host + ":" + str(influx_port)

    client = InfluxDBClient(url=host, token='RCr-XfFQjE4_X0R31p372vCZ2OMbtIdNPVQOwIOEpRawUuETf2bajU-BOwqYKMNipAR_Iu8zVoxrxawEMxNfRA==', org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    _point1 = Point("Decimal").tag("sensor_id", "CPU").field(_("Temperature"), cpu_temp)
    _point2 = Point("Decimal").tag("sensor_id", "CPU").field(_("Usage"), cpu_percent)
    _point3 = Point("Decimal").tag("sensor_id", "SSD").field(_("Temperature"), ssd_temp)
    _point4 = Point("Decimal").tag("sensor_id", "SSD").field(_("Usage"), disk.percent)
    _point5 = Point("Decimal").tag("sensor_id", "RAM").field(_("Usage"), mem.percent)
    # _point4 = Point("Decimal").tag("sensor_id", "SWAP").field(_("Usage"), disk.percent)

    # print(type(cpu_temp))




    # _point2 = Point("my_measurement").tag("location", "New York").field("temperature", 24.3)

    write_api.write(bucket="raspi_test", record=[_point1, _point2, _point3, _point4, _point5])

    client.close()

    # host = "http://" + influx_host + ":" + str(influx_port)

    # if check_status_influx() == False:
    #     return 0
    
    # with InfluxDBClient(url=host, token=influx_token, org=influx_org, debug=False) as client:
    #     try:
    #         write_api = client.write_api(write_options=SYNCHRONOUS)
    #         p = InfluxDBClient.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
    #         write_api.write(bucket='Raspberry', org=influx_org, record=p)
    #     except InfluxDBError as e:
    #         if e.response.status == 401:
    #             raise Exception(f"Insufficient write permissions to 'my-bucket'.") from e
    #         raise

    
    # client = InfluxDBClient.InfluxDBClient(
    #     url=host,
    #     token=influx_token,
    #     org=influx_org
    # )

    # # Write script
    # write_api = client.write_api(write_options=SYNCHRONOUS)

    # p = InfluxDBClient.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
    # write_api.write(bucket='Raspberry', org=influx_org, record=p)

def check_status_influx():
    check = check_ip(influx_host, influx_port)
    logging.debug("Influx: %s", check)
    return check
    
def check_status_grafana():
    check = check_ip(grafana_host, grafana_port)
    logging.debug("Grafana: %s", check)
    return check

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

    print(mem)
    # print(swap)

    ssd_temp = get_temperature_ssd(0)
    create_influx_data()
    test = get_cooler_pwm()

def low_frequency_tasks():
    logging.debug("low_frequency_tasks()")

    global disk
    global disk_free_tb
    global ip_local_address
    global hostname
    global measurements
    global grafana_status

    # ToDo: Check and set it at start for optimization.
    if os.path.exists("/mnt/storage/") and os.path.isdir("/mnt/storage/"):
        disk = psutil.disk_usage("/mnt/storage/")
    else:
        disk = psutil.disk_usage("/home/")

    print(type(disk))

    disk_free_tb = disk.used / 1024 / 1024 / 1024 / 1024
    ip_local_address = get_raspberry_ip()
    hostname = get_raspberry_hostname()
    
    measurements = get_influx_measurements()

    grafana_status = check_status_grafana()

def logging_frequency_tasks():
    logging.debug("logging_frequency_tasks()")

def one_time_tasks():
    logging.debug("one_time_tasks")
    global model
    model = get_raspberry_model()

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


def get_raspberry_hostname():
    hostname = socket.gethostname()
    return hostname

def get_raspberry_ip():
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
                ip_address = ip_info[0]['addr']
                if ip_address and not ip_address.startswith("127."):
                    global net_interface
                    print(ip_address)
                    net_interface = interface
                    return ip_address
        except ValueError:
            continue
    return None

def get_raspberry_model() -> str:
    with open('/proc/device-tree/model') as f:
        model = f.read()
        model = model[:-1]
        return model

def show_systeminfo(disp):
    logging.debug("System information")
    global image_width, image_height, color_background, color_line, skip, ip_local_adress, hostname
    row = 1
    image1 = Image.new("RGB", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(image1)
    draw.text((image_width / 2,(image_height / 3 * row) - (image_height / 3 / 2) - (font_menu_size / 2) - (font_menu_size / 6)), f'{hostname}.local', fill=color_value, font=font_menu, anchor="mm")
    draw.text((image_width / 2,(image_height / 3 * row) - (image_height / 3 / 2) + (font_menu_size / 2) + (font_menu_size / 6)), f'{ip_local_address}', fill=color_value, font=font_menu, anchor="mm")
    row = 3
    draw.text((image_width / 2,(image_height / 3 * row) - (image_height / 3 / 2) + (font_header_size / 2) - (font_header_size / 6)), f'{model}', fill=color_value, font=font_header, anchor="mm")
    disp.ShowImage(image1)

def show_reboot(disp, state = False):
    logging.debug("System reboot")
    global image_width, image_height, color_background, color_line, skip
    if state == True:
        color_state = 'GREEN'
    else:
        color_state = color_header
    row = 1
    image1 = Image.new("RGB", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(image1)
    draw.text((image_width / 2,(image_height / 3 * row) - (image_height / 3 / 2) - (font_menu_size / 2) - (font_menu_size / 6)), _('REBOOT SYSTEM?'), fill=color_value, font=font_menu, anchor="mm")
    draw.rounded_rectangle([(30,180),(125,220)], radius=2.5, fill=color_state, outline=None, width=1)
    draw.text((77.5,200), _('Yes'), fill=color_value, font=font_menu, anchor="mm")
    draw.rounded_rectangle([(155,180),(250,220)], radius=2.5, fill=color_header, outline=None, width=1)
    draw.text((202.5,200), _('No'), fill=color_value, font=font_menu, anchor="mm")
    disp.ShowImage(image1)

def show_shutdown(disp):
    logging.debug("System shutdown")
    global image_width, image_height, color_background, color_line, skip
    row = 1
    image1 = Image.new("RGB", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(image1)
    draw.text((image_width / 2,(image_height / 3 * row) - (image_height / 3 / 2) - (font_menu_size / 2) - (font_menu_size / 6)), _('SHUTDOWN SYSTEM?'), fill=color_value, font=font_menu, anchor="mm")
    draw.rounded_rectangle([(30,180),(125,220)], radius=2.5, fill=color_header, outline=None, width=1)
    draw.text((77.5,200), _('Yes'), fill=color_value, font=font_menu, anchor="mm")
    draw.rounded_rectangle([(155,180),(250,220)], radius=2.5, fill=color_header, outline=None, width=1)
    draw.text((202.5,200), _('No'), fill=color_value, font=font_menu, anchor="mm")
    disp.ShowImage(image1)

def show_alive(disp):
    logging.debug("alive")
    global image_width, image_height, color_background, color_line, skip
    disp.bl_DutyCycle(5)
    # Draw background
    row = 2
    column = 2
    image1 = Image.new("RGB", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(image1)
    text = u"●"
    if (skip % 2) == 0:
        draw.text(((image_width / 3 * column) - (image_width / 3 / 2),(image_height / 3 * row) - (image_height / 3 / 2)), text, fill="WHITE", font=font_value, anchor="mm")

    disp.ShowImage(image1)


