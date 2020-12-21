#!/usr/bin/python

import sys

import spiutil

# Photocell on ADC #1
potentiometer_adc = 1;
tolerance = 5   # to keep from being jittery we'll only change
		# photo when the pot has moved more than # 'counts'

def pot_changed(trim_pot):
	set_photo = trim_pot / 1.024   # convert 10bit adc0 (0-1024) trim pot read into 0-100 photo level
	set_photo = round(set_photo)  # round out decimal
	set_photo /= 10.0

	print '{cctl}Photo = {photo}%  {eol}'.format(cctl=spiutil.CCTL, photo=set_photo, eol=spiutil.EOL),
	sys.stdout.flush()

	if spiutil.DEBUG:
		print "set_photo", set_photo

spiutil.pot_watch(potentiometer_adc, tolerance, pot_changed)

