
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