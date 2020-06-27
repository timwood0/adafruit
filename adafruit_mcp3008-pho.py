#!/usr/bin/env python

import spiutil

# 10k trim pot connected to adc #0
potentiometer_adc = 1;
tolerance = 5   # to keep from being jittery we'll only change
		# photo when the pot has moved more than # 'counts'

def pot_changed(trim_pot):
	set_photo = trim_pot / 1.024   # convert 10bit adc0 (0-1024) trim pot read into 0-100 photo level
	set_photo = round(set_photo)  # round out decimal
	set_photo /= 10.0

	print 'Photo = {photo}%  \r'.format(photo = set_photo),
	sys.stdout.flush()

	if DEBUG:
		print "set_photo", set_photo

spiutil.pot_watch(potentiometer_adc, tolerance, pot_changed)

