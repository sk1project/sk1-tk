# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2003 by Bernhard Herzog 
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
#	Pixmap/Bitmap handling stuff
#

import os

from app import config
from app.events.warn import warn, USER


_canvas = ['TurnTL', 'TurnTR', 'TurnBL', 'TurnBR', 'Center', 'ShearLR', 'ShearUD']
_canvas_dir=''


class SketchPixmaps:

	def InitFromWidget(self, widget, files, basedir):
		for name in files:
			file_base = os.path.join(basedir, name)
			try:
				pixmap = widget.ReadBitmapFile(file_base + '.xbm')[2]
				setattr(self, name, pixmap)
			except IOError, info:
				warn(USER, "Warning: Can't load Pixmap from %s: %s",
						file_base + '.xbm', info)


class PixmapTk:

	_cache = {}

	def load_image(self, name):
		import Tkinter
		if name[0] == '*':
			if config.preferences.color_icons:
				image = self._cache.get(name)
				if image is None:
					image = Tkinter.PhotoImage(file = name[1:], format = 'GIF')
					self._cache[name] = image
			else:
				image = '@' + name[1:-3] + 'xbm'
		else:
			image = name
		return image

	def clear_cache(self):
		self._cache.clear()

PixmapTk = PixmapTk()


def make_file_names(filenames, subdir = ''):
	default = 'error'	# a standard Tk bitmap
	for name in filenames:
		fullname = os.path.join(config.pixmap_dir, subdir, name)
		if os.path.exists(fullname + '.png'):
			setattr(PixmapTk, name, '*' + fullname + '.png')
		elif os.path.exists(fullname + '.gif'):
			setattr(PixmapTk, name, '*' + fullname + '.gif')
		elif os.path.exists(fullname + '.ppm'):
			setattr(PixmapTk, name, '@' + fullname + '.ppm')
		elif os.path.exists(fullname + '.xbm'):
			setattr(PixmapTk, name, '@' + fullname + '.xbm')
		else:
			warn(USER, "Warning: no file %s substituting '%s'",
					fullname, default)
			setattr(PixmapTk, name, default)


pixmaps = SketchPixmaps()


_init_done = 0
def InitFromWidget(widget):
	global _init_done
	if not _init_done:
		pixmaps.InitFromWidget(widget, _canvas, config.pixmap_dir + _canvas_dir)
