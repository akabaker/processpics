#!/usr/bin/python
import asyncore
import pyinotify
import os
from SimpleCV import Image, Color

wm = pyinotify.WatchManager()  # Watch Manager

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
		extension = event.name.split('.')[1]
		if extension:	
			try:
				print "Processing:", event.name
				img = Image(event.pathname)
				result = img.colorDistance(Color.WHITE)
				result_file = os.path.join('/var/lib/owncloud/data/beor/files/', event.name)
				result.save(result_file)
				print "Output:", result_file
			except IOError as e:
				print "Can't open this file {0}: {1}".format(e.errno, e.strerror)
		else:
			print "Skipping this file.."

handler = EventHandler()
notifier = pyinotify.AsyncNotifier(wm, handler)
wdd = wm.add_watch('/home/beor/Pictures/eye-fi', pyinotify.IN_CREATE, rec=True)

asyncore.loop()
