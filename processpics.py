#!/usr/bin/python
import asyncore
import pyinotify
import os
from SimpleCV import Image, Color

class EventHandler(pyinotify.ProcessEvent):

	def color_distance(self, img, output_file):
		result = img.colorDistance(Color.WHITE)
		result.save(output_file)
	
	def find_lines(self, img, output_file):
		lines = img.findLines(threshold=200, minlinelength=100, cannyth1=100, cannyth2=200)
		lines.draw(color=Color.RED)
		img.save(output_file)

	def process_IN_CREATE(self, event):
		extension = event.name.split('.')[1]
		if extension:	
			try:
				print "Processing:", event.name
				img = Image(event.pathname)
				output_file = os.path.join('/tmp/', event.name)
				self.find_lines(img, output_file)
				print "Output:", output_file
			except IOError as e:
				print "Can't open this file {0}: {1}".format(e.errno, e.strerror)
		else:
			print "Skipping this file.."

wm = pyinotify.WatchManager()  # Watch Manager
notifier = pyinotify.AsyncNotifier(wm, EventHandler())
wdd = wm.add_watch('/home/beor/Pictures/eye-fi', pyinotify.IN_CREATE, rec=True)

asyncore.loop()
