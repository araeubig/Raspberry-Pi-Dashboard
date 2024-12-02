# Raspberry-Pi-Dashboard
A configurable LCD dashboard with touch functionality for headless Raspberry Pi servers.

<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Faraeubig%2FRaspberry-Pi-Dashboard&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<a href="/LICENSE"><img src="https://img.shields.io/badge/license-GPL-blue.svg" alt="license" /></a>

> This repository is in progress for the first documented version. The current version works perfectly, but there are still a few fine adjustments to make the configuration easier  - please be patient and visit again in some days. By searching for a solution to fulfill all important steps i found a repository as a very good starting point. I didn't create a fork because there are to many changes and enhancements. Therefore i started with this new repository. In the final README you will find all informations about the original repo, this repo and the changed parts.

![First display test](/files/examples/display_test_first.jpg)
## About the project
As the Raspberry is to be operated as a server in the distribution cabinet, it not only needs a DIN housing, but also a display to show the most important system information. A solution with various green and red LEDs seemed more complex to me than simply connecting a display. Another requirement was to be able to restart and shut down the Raspberry using buttons or a touch display. Last but not least, the Raspberry should not only be supplied with power via PoE, but also offer an M.2 slot for an NVMe SSD - because this is the only way to ensure long-term operation without possible SD card failures.

The search for the necessary components turned out to be more difficult than expected. The market offers only a few DIN housings for the Raspberry Pi - espacially for the model 5, and there are only a few displays with a touch option that are small enough to fit into the housing. The range of combined PoE-M.2 HATS is manageable, but more than sufficient.

While testing the possible components, I decided to document two variants for mounting on a DIN rail and another variant for desktop use:

1. Configuration with 4M wide housing for exclusive power supply via PoE
2. Configuration with 6M wide housing for optional power supply via 24V or 220V
3. Configuration with standard housing for power supply via USB plug-in power supply unit without touch functionality
## Use cases
As already mentioned in the introduction, the aim is to use the Raspberry as a headless server (i.e. without a screen) and to place it in a DIN-compliant distribution board. There it should perform its service, installed with any system according to the user's requirements.

In my case, I only need a 'lightweight' system with:
- InfluxDB
- Grafana

to record data from the KNX system.

In most cases, however, the Raspberry will certainly run as a server for
- NodeRed,
- HomeAssistant,
- OpenHAB or
- IOTStack (with the desired containers)

In the end, however, this is irrelevant, as it is all about DIN-compliant installation and the working dashboard.
## Dashboard features

Current version 0.1:
- Use with ST7789V2-based displays
  - portrait or landscape orientation
  - automatic resizing of text and fields based on display
- Use with CST816T-based touch panels
  - control dashboard menu with gestures and buttons
- Values
  - used RAM in percent
  - used CPU in percent
  - used HDD in percent
  - used SWAP in percent
  - current CPU temperature
  - current SSD temperature
  - current check if Influx is alive
  - Influx measurements of the last x-hours/days
  - current check if Grafana is alive
  - current upload/download transfer rate
- Value visualisation
  - entire value range from 0 to 100 in text color
  - Set threshold for each value to switch from text color to 'alert' color. Alert color makes a fading from green to red based on the real value
- Switch with touch panel between
  - Dashboard
    - with configurated values
  - System information
    - IP adress
    - hostname
    - Raspberry Pi version
  - Reboot system
  - Shutdown system 


## Example screenshots
### Waveshare 1.69" 240x280 display (landscape orientation)
#### Startup
![Startup](/files/examples/startup.jpg)
#### Dashboard
![Dashboard](/files/examples/dashboard.jpg)
#### System information
![System information](/files/examples/system_information.jpg)
#### Reboot
![Reboot](/files/examples/reboot.jpg)
#### Shutdown
![Shutdown](/files/examples/shutdown.jpg)
### Waveshare 1.69" 240x280 display (portrait orientation)
Upcoming
### Phoenix Contact 2.4" 320x240 display
Upcoming

> The text is much brighter on the small displays (based on the backlight and pixel-pitch)
## Requirements
- Raspberry Pi 5
- Touch display that fits into the DIN housing / desktop case (preferably with ST7789V2 driver)
- DIN case / standard case
- 3D printed model of DIN Case top / desktop case cover
- Python >= 3.9
- NVMe-CLI Tool (if using Raspberry Pi with installed NVMe-SSD)
## Recommended Hardware
### Cases
#### DIN mount
- [Waveshare DIN RAIL CASE Pi 5](https://www.waveshare.com/pi5-case-din-rail-b.htm)
  - State: Tested
  - SKU: 26682 / PI5-CASE-DIN-RAIL-B
  - Use with: Raspberry Pi 5
  - Size: 4M
- [Italtronic MODULBOX XTS](https://eng.italtronic.com/accessori/25.0410000.RP5/) !!!CURRENTLY NO AIR VENTS 
    - State: Untested
    - SKU: 25.0410000.RP5
    - Use with: Raspberry Pi 5
    - Size: 4M
- [Phoenix Contact BC Series](https://www.phoenixcontact.com/en-pc/products/electronics-housings/electronics-housings-for-raspberry-pi-applications) CURRENTLY NOT OPTIMIZED FOR RPi 5
  - State: Currently Untested / Upcoming
  - SKU: 2202874
  - Use with: Raspberry Pi 5
  - Size: 6M
#### Standard case
- [Argon Neo 5 M.2 NVME](https://argon40.com/products/argon-neo-5-m-2-nvme-for-raspberry-pi-5)
  - State: Untested
  - SKU: N/A
  - Use with: Raspberry Pi 5
  - Size: standard
### Displays
- [Waveshare - 1.69inch LCD Touch Display Module, 240×280](https://www.waveshare.com/product/1.69inch-touch-lcd-module.htm)
    - State: Tested
    - SKU: 27057 - 1.69inch Touch LCD Module
    - Resolution: 240x280
    - Use with: DIN case
- [Waveshare - 1.69inch LCD Display Module, 240×280](https://www.waveshare.com/1.69inch-lcd-module.htm) WITHOUT TOUCH
    - State: Tested
    - SKU: 24382 - 1.69inch LCD Module
    - Resolution: 240x280
    - Use with: DIN case, standard case
- [Phoenix Contact - BC DKL 2.4" Touch Display](https://www.phoenixcontact.com/en-pc/products/electronics-housings/bc-modular-electronics-housings?f=NobwRAZglgNgLgUwE4EkAmYBcYAOSD2aArgMZwD6EAhgLaxQLkDmSOYANJAzBtgAoFiZAATU6MAJ4cu8ZABUJOBFjABZAKpyAggCEAMgFFp0WUgBqVGEQQBnLMDA6AwsICMABgDs7AGwA6PzAAXU4AO1plfkFSOFFaWCkAX3ZwE0RUXlxosnI4RWVOaAQeFQFCGOE8pWNYdIVq7A1tfSNC2uQLK1t7MCd8ADdkYLCI0uzYquVEoKA)
  - State: Currently untested / Upcoming
  - SKU: 2202874
  - Use with: Raspberry Pi 5
  - Size: 6M
### HAT's
- [Raspberry Pi M.2 HAT+](https://www.raspberrypi.com/products/m2-hat-plus/)
    - State: Tested
    - SKU: N/A
    - Use with: Raspberry Pi 5 with standard USB power supply
    - Supported form factors: 2230, 2242
- [Waveshare PoE M.2 HAT+](https://www.waveshare.com/pi5-case-din-rail-b.htm)
    - State: Tested
    - SKU: 28411
    - Use with: Raspberry Pi 5, DIN case
    - Supported form factors: 2230, 2242
- [52Pi P33 M.2 PoE+ HAT](https://52pi.com/products/p33-m-2-nvme-2280-poe-hat-extension-board-with-official-cooler-for-raspberry-pi-5?variant=45156837818520)
    - State: Tested
    - SKU: EP-0241
    - Use with: Raspberry Pi 5, DIN case
    - Supported form factors: 2230, 2242, 2260, 2280
- [52Pi M.2 NVME PoE+ HAT](https://52pi.com/products/m-2-nvme-m-key-poe-hat-with-official-pi-5-active-cooler-for-raspberry-pi-5-support-m-2-nvme-ssd-2230-2242?variant=44972209012888)
    - State: Currently untested / Upcoming
    - SKU: EP-0240
    - Use with: Raspberry Pi 5, DIN case
    - Supported form factors: 2230, 2242

A review about combined HATs was made by Jeff Geerling on YouTube:

[![PoE+ NVMe beats Raspberry Pi to the punch](http://img.youtube.com/vi/x9ceI0_r_Kg/0.jpg)](http://www.youtube.com/watch?v=x9ceI0_r_Kg "PoE+ NVMe beats Raspberry Pi to the punch")
### Accessory
- [Waveshare Micro HDMI to HDMI Multifunctional Adapter](https://www.waveshare.com/pi5-connector-adapter.htm)
    - State: Currently untested / Upcoming
    - SKU: 28411
    - Use with: Raspberry Pi 4, Raspberry Pi 5, DIN case 6M
- [DeskPi KL-P24 Micro HDMI to HDMI Adapter Board](https://deskpi.com/products/deskpi-kl-p24-raspberry-pi-adapter-board)
    - State: Currently untested / Upcoming
    - SKU: DP-0036-2pcs
    - Use with: Raspberry Pi 4, Raspberry Pi 5, DIN case 6M
- [Argon THRML 30mm Active Cooler](https://argon40.com/products/argon-thrml-30mm-active-cooler?variant=47734223077649)
    - State: Currently untested / Upcoming
    - SKU: N/A
    - Use with: Raspberry Pi 5, DIN case, standard case
- [Raspberry Pi Active Cooler](https://www.raspberrypi.com/products/active-cooler/)
    - State: Tested
    - SKU: N/A
    - Use with: Raspberry Pi 5, DIN case, standard case
### Special
- [Oratek TOFU Board](https://tofu.oratek.com/#/?id=tofu-board)
    - State: Tested without case / case test upcoming
    - SKU: N/A
    - Use with: Raspberry CM4, perhaps DIN case 6M
    - Special features: M.2 Slot, Raspberry CM4, flexible power supply
    
    A review about TOFU Board was made too by Jeff Geerling on YouTube:

    [![Native M.2 NVMe on a Raspberry Pi - CM4 TOFU](http://img.youtube.com/vi/x9ceI0_r_Kg/0.jpg)](https://www.youtube.com/watch?v=m-QSQ24_8LY&t=6s "Native M.2 NVMe on a Raspberry Pi - CM4 TOFU")
### Suitable configurations
#### DIN case, 4M
Upcoming
#### Standard case
Upcoming
## Assembly
Upcoming
### Connecting the display
Upcoming
#### Waveshare 1.69" touch display
Upcoming
#### Waveshare 1.69" display
Upcoming
#### Phoenix Contact
Upcoming
## Installation
### Use with NVMe-SSD
If the Raspberry Pi is used with an M.2 HAT with an NVMe-SSD installed, the NVMe-CLI tool should be installed beforehand with this command:
```shell
sudo apt install nvme-cli
```
### Download
Download this respository in your user folder with:
```shell
sudo apt-get install git
git clone https://github.com/araeubig/Raspberry-Pi-Dashboard
```
You could run the dashboard 'one-time' or as 'service'. For customizing and testing the one-time run makes sense. After customizing / configuring the service is the preffered option.
### Run one-time
Start the dashboard with:
```shell
cd Raspberry-Pi-Dashboard
./run.sh
```
Stop the running dashboard with <kbd>⌃ Control</kbd> + <kbd>C</kbd>
### Run dashboard as service
Start the dashboard and run as service on boot with:
```shell
cd Raspberry-Pi-Dashboard
sudo ./create_service.sh
```
### Stop dashboard service
Stop the dashboard service with:
```shell
sudo systemctl stop rpidashboard.service
```
### Remove dashboard service
Remove the dashboard service with:
```shell
cd Raspberry-Pi-Dashboard
sudo ./remove_service.sh
```
### Customizing
Upcoming
## 3D Models
Upcoming
### Printing services
Upcoming
### Print yourself
Upcoming
## To Do's
Upcoming
## Contribution
Upcoming
## Credits
Upcoming
## Disclaimer
Upcoming