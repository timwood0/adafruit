#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import sys
import RPi.GPIO as GPIO
import spidev
import pdb

spi = spidev.SpiDev()
#spi = SPI.SPI("/dev/spidev0.0")
#spi.mode = spi.MODE_0
#spi.speed = 500000
spi.open(0, 0)
DEBUG = 0
IS_TEST = 0

# Negative test cases; all should report wrmsg_ messages from spidev_module.c and continue
try:
	r = spi.xfer2([])
except Exception as exc:
	print exc

try:
	ta = []
	for i in range(4097): 
		ta.append(i)

	r = spi.xfer2(ta)
except Exception as exc:
	print exc

try:
	r = spi.xfer2([ "0x1234567892345678901218195739184" ])
except Exception as exc:
	print exc

spi.close()
sys.exit(0)
