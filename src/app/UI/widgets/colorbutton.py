# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.
#
# The color sample size is 31x20 px

from Tkinter import Button

def rgb_to_tkcolor(color):
	"""
	Converts list of RGB float values to hex color string.
	For example: [1.0, 0.0, 1.0] => #ff00ff
	"""
	r, g, b = color
	return '#%04x%04x%04x' % (int(255 * r), int(255 * g), int(255 * b))

class TColorButton(Button):

	def __init__(self, master=None, color=None, cnf={}, **kw):
		Button.__init__(self, master, kw)
		self['border'] = 1
		self.bgc = self['bg']
		self.set_color(color)

	def set_color(self, color):
		if color is None:
			self['image'] = 'empty_pattern_colorbutton'
			self['bg'] = self.bgc
			self['activebackground'] = self.bgc
		else:
			self['image'] = 'pattern_colorbutton'
			self['bg'] = rgb_to_tkcolor(color)
			self['activebackground'] = rgb_to_tkcolor(color)

