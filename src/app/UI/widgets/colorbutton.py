# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.
#
# The color sample size is 31x20 px

from Ttk import TButton
import Image, ImageTk

class TColorButton(TButton):
	
	def __init__(self, master=None, color=None, cnf={}, **kw):
		TButton.__init__(self, master, kw)
		self['style']='ColorButton'
		self.set_color(color)
		
	def set_color(self, color):
		if color is None:
			self['image']='empty_pattern_colorbutton'
		else:
			#the color should be a rgb tuple like (10,20,30)
			self.bitmap=Image.new("RGB",(31,20),color)
			self.image=ImageTk.PhotoImage(self.bitmap)
			self['image']=self.image
			