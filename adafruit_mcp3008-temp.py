#!/usr/bin/env python

import sys

import spiutil

# 10k trim pot connected to adc #0
potentiometer_adc = 2;
tolerance = 5   # to keep from being jittery we'll only change
		# photo when the pot has moved more than # 'counts'
v_outmax = 3.3
adc_quanta = 1024.0

def pot_changed(trim_pot):
	# convert 10bit adc (0-1024) level into a degC level
	set_level = trim_pot * ((v_outmax * 1000.0) / adc_quanta)
	temp_level = (set_level - 500.0) / 10.0  # Calibration: adafruit.com/tmp36-temperature-sensor
	# Convert to degF
	temp_level = (temp_level * 1.8) + 32.0
	temp_level = round(temp_level)  # round out decimal value of degF
	temp_level = int(temp_level)	# cast level as integer

	print 'Temp = {level} F \r'.format(level=temp_level),
	sys.stdout.flush()

	if spiutil.DEBUG:
		print "set_level", temp_level

spiutil.pot_watch(potentiometer_adc, tolerance, pot_changed)
