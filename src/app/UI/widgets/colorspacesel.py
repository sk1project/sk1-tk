# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TCombobox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP,W, E, DISABLED, NORMAL, StringVar
from app import _


EMPTY=_('Empty pattern')
RGB=_('RGB color')
CMYK=_('CMYK color')
SPOT=_('Spot color')
REGISTRATION=_('Registration Black')

class ColorSpaceSelector(TFrame):
	
	def __init__(self, parent, color=None, allow_emtpy=1, **kw):
		self.refcolor=color
		self.color=color
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.cs_name = StringVar(self)
		self.set_cs_name(self.refcolor)
		
		label = TLabel(self, text=_("Colorspace: "))
		label.pack(side = TOP, anchor=W)
		
		self.colorspaces = TCombobox(self, state='readonly', postcommand = self.set_cs, 
									 values=self.make_cs_list(allow_emtpy), width=17, style='ComboNormal',
									 textvariable=self.cs_name)
		self.colorspaces.pack(side = TOP, fill=X)
		
	def make_cs_list(self,allow_emtpy):
		cs=()
		if allow_emtpy:
			cs+=(EMPTY,)
		cs+=(RGB,CMYK,SPOT,REGISTRATION)
		return cs
	
	def set_cs(self):
		pass
	
	def set_cs_name(self,color):
		if color is None:
			self.cs_name.set(EMPTY)
			return
		if color.model=='RGB':
			self.cs_name.set(EMPTY)
			return
		if color.model=='CMYK':
			self.cs_name.set(CMYK)
			return
		if color.model=='SPOT':
			if color.name=='Registration color':
				self.cs_name.set(REGISTRATION)
			else:
				self.cs_name.set(SPOT)
		