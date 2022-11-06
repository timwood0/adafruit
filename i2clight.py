#!/usr/bin/python

# Vary an LED brightness up and down via a 4725 DAC

import time
import os
import sys
import Adafruit_MCP4725 as MCP4725

# "Voltages" are unitless parts of 4096 multiplied by Vdd on-board the device
lowV = 3168 # Approx. firing threshold of LED
highV = 4095
i2cAddr = 0x62
mcp4725 = MCP4725.MCP4725(address=i2cAddr)

outV = lowV
period = 0.04 #sec
delta = 50
while True:
	mcp4725.set_voltage(outV)
	time.sleep(period)

	if delta > 0:
		if outV >= highV:
			delta = -delta
	else:
		if outV <= lowV:
			delta = -delta

	outV += delta
