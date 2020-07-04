# Adapted from Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import sys
import subprocess

import RPi.GPIO as GPIO
import spidev
#import spi as SPI
import pdb

spi = spidev.SpiDev()
# For old SPI package
#spi = SPI.SPI("/dev/spidev0.0")
#spi.mode = spi.MODE_0
spi.open(0, 0)
spi.max_speed_hz = 100000
INTVL = 0.25 #sec
DEBUG = 0
TRACE = 0

# Display utils
# Home cursor before printing; suppress newline.  Support useful output re-dir to a file.
HOME_CURSOR = '\x1b[1;1f'  # Home cursor in xterm window XXX $TERM independence
if sys.stdout.isatty():
	CCTL = HOME_CURSOR
	EOL = '\r'
else:
	CCTL = ""
	EOL = '\n'


if DEBUG and TRACE:
	pdb.set_trace()


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
	if ((adcnum > 7) or (adcnum < 0)):
		return -1

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

def pot_watch(pot_adc, tolerance, pot_changed, intvl=INTVL):
	# Loop watching an SPI channel, and call the pot_changed callback
	# when significant change detected
	last_read = 0

	try:
		while True:
			# read the analog pin
			trim_pot = readadc(pot_adc)

			# Save difference from last sample
			pot_adjust = abs(trim_pot - last_read)

			if DEBUG:
				print "trim_pot:", trim_pot, "pot_adjust:", pot_adjust, "last_read", last_read,

			trim_pot_changed = (pot_adjust > tolerance)

			if DEBUG:
				print "trim_pot_changed", trim_pot_changed

			if trim_pot_changed:
				pot_changed(trim_pot)

			last_read = trim_pot

			# hang out and do nothing for a spell
			time.sleep(intvl)
	except KeyboardInterrupt:
		pass
	finally:
		spi.close()
