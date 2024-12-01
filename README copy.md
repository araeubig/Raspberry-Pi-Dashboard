# Raspberry-Pi-Dashboard
A configurable LCD dashboard with touch functionality for headless Raspberry Pi servers. (Optional without touch)

<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Faraeubig%2FRaspberry-Pi-Dashboard&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<a href="/LICENSE"><img src="https://img.shields.io/badge/license-GPL-blue.svg" alt="license" /></a>


> QUOTE This repository is in progress for the first running version - please be patient and visit again in some days.
By searching for a solution to fulfill all important steps i found a repository as a very good starting point. I didn't create a fork because there are to many changes and enhancements. Therefore i started with this new repository. In the final README you will find all informations about the original repo, this repo and the changed parts. 

This repository contains all needed files to get a small LCD-Touch display running as dashboard for a headless Raspberry Pi. The focus of the project is not only the software for the display, it's the complete running system for mounting on a DIN rail.

## About the project

### Why and for what?

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