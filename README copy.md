# Raspberry-Pi-Dashboard
A configurable LCD dashboard with touch functionality for headless Raspberry Pi servers. (Optional without touch)

<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Faraeubig%2FRaspberry-Pi-Dashboard&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<a href="/LICENSE"><img src="https://img.shields.io/badge/license-GPL-blue.svg" alt="license" /></a>


> QUOTE This repository is in progress for the first running version - please be patient and visit again in some days.
By searching for a solution to fulfill all important steps i found a repository as a very good starting point. I didn't create a fork because there are to many changes and enhancements. Therefore i started with this new repository. In the final README you will find all informations about the original repo, this repo and the changed parts. 

This repository contains all needed files to get a small LCD-Touch display running as dashboard for a headless Raspberry Pi. The focus of the project is not only the software for the display, it's the complete running system for mounting on a DIN rail.

## About the project

### Why and for what?

### Hardware

#### M.2 (PoE) HATS

Possible HATS

- [Raspberry Pi M.2 HAT+](https://www.raspberrypi.com/products/m2-hat-plus/)
    - State: Tested
    - SKU: N/A
    - Use with: Raspberry Pi 5
    - Supported form factors: 2230, 2242
- [Waveshare PoE M.2 HAT+](https://www.waveshare.com/pi5-case-din-rail-b.htm)
    - State: Tested
    - SKU: 28411
    - Use with: Raspberry Pi 5
    - Supported form factors: 2230, 2242
- [52Pi P33 M.2 PoE+ HAT](https://52pi.com/products/p33-m-2-nvme-2280-poe-hat-extension-board-with-official-cooler-for-raspberry-pi-5?variant=45156837818520)
    - State: Tested
    - SKU: EP-0241
    - Use with: Raspberry Pi 5
    - Supported form factors: 2230, 2242, 2260, 2280
- [52Pi M.2 NVME PoE+ HAT](https://52pi.com/products/m-2-nvme-m-key-poe-hat-with-official-pi-5-active-cooler-for-raspberry-pi-5-support-m-2-nvme-ssd-2230-2242?variant=44972209012888)
    - State: Untested
    - SKU: EP-0240
    - Use with: Raspberry Pi 5
    - Supported form factors: 2230, 2242

A great review about combined HATs was made by Jeff Geerling om YouTube:

[![PoE+ NVMe beats Raspberry Pi to the punch](http://img.youtube.com/vi/x9ceI0_r_Kg/0.jpg)](http://www.youtube.com/watch?v=x9ceI0_r_Kg "PoE+ NVMe beats Raspberry Pi to the punch")


#### Displays

Possible Displays

- [Waveshare - 1.69inch LCD Touch Display Module, 240×280](https://www.waveshare.com/product/1.69inch-touch-lcd-module.htm)
    - State: Tested
    - SKU: 27057 - 1.69inch Touch LCD Module

- [Waveshare - 1.69inch LCD Display Module, 240×280](https://www.waveshare.com/1.69inch-lcd-module.htm)
    - State: Tested
    - SKU: 24382 - 1.69inch LCD Module

- [Phoenix Contact]()
    - State: Tested

#### Cases

Possible Desktop Cases

- [Argon Neo 5](https://argon40.com/products/argon-neo-5-blck-case-for-raspberry-pi-5-with-built-in-fan)


Possible DIN Cases

- [Waveshare DIN RAIL CASE Pi 5](https://www.waveshare.com/pi5-case-din-rail-b.htm)
    - State: Tested
    - SKU: 26682 / PI5-CASE-DIN-RAIL-B
    - Use with: Raspberry Pi 5
    - Size: 4M


- [Italtronic MODULBOX XTS](https://eng.italtronic.com/accessori/25.0410000.RP5/)
    - State: Untested
    - SKU: 25.0410000.RP5
    - Use with: Raspberry Pi 5
    - Size: 4M

- [Italtronic MODULBOX XTS](https://eng.italtronic.com/accessori/25.0410000.RP4/)
    - State: Untested
    - SKU: 25.0410000.RP4
    - Use with: Raspberry Pi 4
    - Size: 4M

- [Phoenix Contact]()
    - State: Untested
    - SKU:
    - Use with: Raspberry Pi 4 / Raspberry Pi 4 (coming begin 2025)

- [eSc EDV SYSTEM - ESCPi5]()
    - State: Untested
    - SKU: ESCPi5
    - Use with: Raspberry Pi 5

#### Accessoires



### Software

## Requirements

## Get it working

### Display

### Installation

```shell
sudo apt-get install git
git clone https://github.com/araeubig/Raspberry-Pi-Dashboard
```

#### Run one time

```shell
cd Raspberry-Pi-Dashboard
./run.sh
```

#### Run as service on startup

```shell
cd Raspberry-Pi-Dashboard
sudo ./create_service.sh
```

#### Stopping the service:

```shell
sudo systemctl stop rpidashboard.service
```

#### Removing the service:

```shell
cd Raspberry-Pi-Dashboard
sudo ./remove_service.sh
```

#### Customizing

If you want to use the 1.69" display without touch funcionality, you have to comment out the import of the touch function:

```python
from display.LCD_TOUCH_Waveshare_1inch69 import LCD_1inch69
# from display.LCD_TOUCH_Waveshare_1inch69 import Touch_1inch69
```

## 3D Models

### Printing services

### Print yourself

## To Do's

## Contribution

## Credits

## Disclaimer



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
  - State: Untested
    - SKU: 2202874
    - Use with: Raspberry Pi 5
    - Size: 6M



- [Argon Neo 5 M.2 NVME](https://argon40.com/products/argon-neo-5-m-2-nvme-for-raspberry-pi-5)
  - State: Untested
- SKU: N/A
- Use with: Raspberry Pi 5
- Size: standard


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

- [Phoenix Contact BC 107.6 DKL](https://www.phoenixcontact.com/en-pc/products/electronics-housings/bc-modular-electronics-housings)
  - State: Untested
    - SKU: 1335865
    - Resolution: 320x240
    - Use with: Phoenix Contact DIN case


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
    - State: Untested
    - SKU: EP-0240
    - Use with: Raspberry Pi 5, DIN case
    - Supported form factors: 2230, 2242

A great review about combined HATs was made by Jeff Geerling om YouTube:

[![PoE+ NVMe beats Raspberry Pi to the punch](http://img.youtube.com/vi/x9ceI0_r_Kg/0.jpg)](http://www.youtube.com/watch?v=x9ceI0_r_Kg "PoE+ NVMe beats Raspberry Pi to the punch")

