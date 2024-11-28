import os
import sys
import time
import datetime
import psutil
import socket
import threading
import netifaces
import logging
from collections import deque
from PIL import Image, ImageDraw, ImageFont
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError

# from display import LCD_1inch69,Touch_1inch69

# Raspberry Pi pin configuration:
RST    = 27
DC     = 25
BL     = 18
TP_INT = 4
TP_RST = 17