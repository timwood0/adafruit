#!/usr/bin/env python

# Adapted from Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import sys
import RPi.GPIO as GPIO
import spidev
#import spi as SPI
import pdb

spi = spidev.SpiDev()
#spi = SPI.SPI("/dev/spidev0.0")
#spi.mode = spi.MODE_0
#spi.speed = 500000
spi.open(0, 0)
INTVL = 0.25 #sec
DEBUG = 0
IS_TEST = 0

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
	if ((adcnum > 7) or (adcnum < 0)):
		return -1

	#pdb.set_trace()
	commandout = [ 0, 0, 0 ]
	commandout[0] = 0x1 # start-bit
	commandout[1] = (0x8 | adcnum) << 4 # single-ended bit | A-channel#
	commandout[2] = 0   # we only need to send 5 bits here

	# Take in result as array of three bytes. 
	# Return the two lowest bits of the 2nd byte and
	# all of the third byte
	r = spi.xfer2(commandout)
	#r = spi.transfer(commandout)

	# read in 10 ADC bits
	adcout = ((r[1] & 3) << 8) | r[2]
	return adcout

# 10k trim pot connected to adc #0
potentiometer_adc = 2;

last_read = 0   # this keeps track of the last potentiometer value
tolerance = 5   # to keep from being jittery we'll only change
		# photo when the pot has moved more than # 'counts'
v_outmax = 3.3
adc_quanta = 1024.0

try:
	while True:
		# we'll assume that the pot didn't move
		trim_pot_changed = False

		# read the analog pin
		trim_pot = readadc(potentiometer_adc)
		# how much has it changed since the last read?
		pot_adjust = abs(trim_pot - last_read)

		if DEBUG:
			print "trim_pot:", trim_pot, "pot_adjust:", pot_adjust, "last_read", last_read,

		if ( pot_adjust > tolerance ):
		   trim_pot_changed = True

		if DEBUG:
			print "trim_pot_changed", trim_pot_changed

		if ( trim_pot_changed ):
			# convert 10bit adc (0-1024) level into a degC level
			set_level = trim_pot * ((v_outmax * 1000.0) / adc_quanta)
			temp_level = (set_level - 500.0) / 10.0 # Calibration: adafruit.com/tmp36-temperature-sensor
			# Convert to degF
			temp_level = (temp_level * 1.8) + 32.0
			temp_level = round(temp_level)  # round out decimal value of degF
			temp_level = int(temp_level)	# cast level as integer

			print 'Temp = {level} F'.format(level = temp_level)

			#if DEBUG:
			#	print "set_level", temp_level

			# save the potentiometer reading for the next loop
			last_read = trim_pot

		# hang out and do nothing for a spell
		time.sleep(INTVL)

except KeyboardInterrupt:
	spi.close()
	sys.exit(0)
