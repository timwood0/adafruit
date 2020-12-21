#!/usr/bin/python

import subprocess
import sys

import spiutil

# 10k trim pot connected to ADC #0
potentiometer_adc = 0;
tolerance = 2   # to keep from being jittery we'll only change
				# volume when the pot has moved more than # 'counts'

# Start helper process to set volume
amixer_proc = subprocess.Popen(("/usr/bin/amixer", "--stdin"),
								stdin=subprocess.PIPE,
								stdout=open("/dev/null", "w"))

def pot_changed(trim_pot):
	set_volume = trim_pot / 10.24   # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
	set_volume = round(set_volume)  # round out decimal value
	set_volume = int(set_volume)  # cast volume as integer

	print '{cctl}Volume = {volume}%  {eol}'.format(cctl=spiutil.CCTL, volume=set_volume, eol=spiutil.EOL),
	sys.stdout.flush()
	amixer_proc.stdin.write('cset numid=1 -- {volume}%\n'.format(volume=set_volume))

	if spiutil.DEBUG:
		print "set_volume", set_volume

try:
	spiutil.pot_watch(potentiometer_adc, tolerance, pot_changed)
finally:
	# Close down helper proc.
	amixer_proc.stdin.close()
	amixer_proc.wait()
