# Raspberry-Pi-Dashboard
A configurable LCD dashboard with touch functionality for headless Raspberry Pi servers. (Optional without touch / mounting in distribution cabinet)

<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Faraeubig%2FRaspberry-Pi-Dashboard&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<a href="/LICENSE"><img src="https://img.shields.io/badge/license-GPL-blue.svg" alt="license" /></a>


> QUOTE This repository is in progress for the first running version - please be patient and visit again in some days. By searching for a solution to fulfill all important steps i found a repository as a very good starting point. I didn't create a fork because there are to many changes and enhancements. Therefore i started with this new repository. In the final README you will find all informations about the original repo, this repo and the changed parts.

## About the project

As the Raspberry is to be operated as a server in the distribution cabinet, it not only needs a DIN housing, but also a display to show the most important system information. Another requirement was to be able to restart and shut down the Raspberry using buttons or a touch display. Last but not least, the Raspberry should not only be supplied with power via PoE, but also offer an M.2 slot for an NVMe SSD - because this is the only way to ensure long-term operation without possible SD card failures.

The search for the necessary components turned out to be more difficult than expected. The market offers only a few DIN housings for the Raspberry Pi 5, and there are only a few displays with a touch option that are small enough to fit into the housing. The range of combined PoE-M.2 HATS is manageable, but more than sufficient.

While testing the possible components, I decided to document two variants for mounting on a DIN rail and another variant for desktop use:

1. configuration with 4M wide housing for exclusive power supply via PoE
2. configuration with 6M wide housing for optional power supply via 24V or 220V
3. Configuration with standard housing for power supply via USB plug-in power supply unit without touch functionality

## Requirements

- Raspberry Pi 5
- Touch display that fits into the DIN housing / desktop case (preferably with ST7789V2 driver)
- 3D printed model of DIN Case top / desktop case cover
- DIN case / standard case
- Python >= 3.9

### Hardware

#### Cases

#### Displays

#### HAT's





