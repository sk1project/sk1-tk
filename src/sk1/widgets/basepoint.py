# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TRadiobutton, TLabelframe
from Tkinter import BOTH, LEFT, TOP, W
from sk1.tkext import UpdatedRadiobutton
from app import _



class BasePointSelector(TFrame):
	
	def __init__(self, parent, anchor='C', command = None, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.command = command
		self.anchor = anchor
		#---------------------------------------------------------
		# Basepoint check
		# NW -- N -- NE
		# |     |     |
		# W  -- C --  E
		# |     |     |
		# SW -- S -- SE
		#
		# USER - basepoint
		
		frame=TFrame(self, style='FlatFrame')
		frame.pack(side = TOP, fill = BOTH)
		
		radio = UpdatedRadiobutton(frame, value = 'NW',variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		radio = UpdatedRadiobutton(frame, value = 'N', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		radio = UpdatedRadiobutton(frame, value = 'NE', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		
		frame=TFrame(self, style='FlatFrame')
		frame.pack(side = TOP, fill = BOTH)
		
		radio = UpdatedRadiobutton(frame, value = 'W', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		radio = UpdatedRadiobutton(frame, value = 'C', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		radio = UpdatedRadiobutton(frame, value = 'E', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		
		frame=TFrame(self, style='FlatFrame')
		frame.pack(side = TOP, fill = BOTH)
		
		radio = UpdatedRadiobutton(frame, value = 'SW', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		radio = UpdatedRadiobutton(frame, value = 'S',  variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		radio = UpdatedRadiobutton(frame, value = 'SE', variable = self.anchor, command = self.command)
		radio.pack(side=LEFT, anchor=W)
		
		
###############################################################################

	def get_basepoint(self,hor_sel,ver_sel,left,bottom, anchor=None):
		# NW -- N -- NE
		# |     |     |
		# W  -- C --  E
		# |     |     |
		# SW -- S -- SE
		if anchor is None:
			anchor=self.anchor.get()
		
		if anchor == 'NW':
			cnt_x=left
			cnt_y=ver_sel+bottom
		elif anchor == 'N':
			cnt_x=hor_sel/2.0+left
			cnt_y=ver_sel+bottom
		elif anchor == 'NE':
			cnt_x=hor_sel+left
			cnt_y=ver_sel+bottom
		elif anchor == 'W':
			cnt_x=left
			cnt_y=ver_sel/2.0+bottom
		elif anchor == 'E':
			cnt_x=hor_sel+left
			cnt_y=ver_sel/2.0+bottom
		elif anchor == 'SW':
			cnt_x=left
			cnt_y=bottom
		elif anchor == 'S':
			cnt_x=hor_sel/2.0+left
			cnt_y=bottom
		elif anchor == 'SE':
			cnt_x=hor_sel+left
			cnt_y=bottom
		elif anchor == 'C':
			cnt_x=hor_sel/2.0+left
			cnt_y=ver_sel/2.0+bottom
		else:
			cnt_x=None
			cnt_y=None
		
		return cnt_x, cnt_y


