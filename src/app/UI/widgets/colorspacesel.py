# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCombobox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP,W, E, S, DISABLED, NORMAL, StringVar
from app import _
from app.Graphics.color import CreateRGBColor, CreateCMYKColor, CreateSPOTColor, Registration_Black, \
			 CreateRGBAColor, CreateCMYKAColor


EMPTY=_('Empty pattern')
RGB=_('RGB color')
CMYK=_('CMYK color')
SPOT=_('Spot color')
REGISTRATION=_('Registration Black')

class ColorSpaceSelector(TFrame):
	
	current_cs=''
	
	def __init__(self, parent, callback, color, sign, allow_emtpy=1, **kw):
		self.color=color
		self.callback=callback
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.cs_name = StringVar(self)
		self.set_cs_name(self.color)
		
		self.colorspaces = TCombobox(self, state='readonly', postcommand = self.set_cs, 
									 values=self.make_cs_list(allow_emtpy), width=17, style='ComboNormal',
									 textvariable=self.cs_name)
		self.colorspaces.pack(side = BOTTOM, fill=X, pady=3)
		
		label = TLabel(self, text=_("Colorspace:")+" ")
		label.pack(side = LEFT, anchor='sw')
		
		label = TLabel(self, image=sign)
		label.pack(side = RIGHT)
		
	def make_cs_list(self,allow_emtpy):
		cs=()
		if allow_emtpy:
			cs+=(EMPTY,)
		cs+=(RGB,CMYK,SPOT,REGISTRATION)
		return cs
	
	def set_cs(self):
		if self.check_changes():
			if self.cs_name.get()==RGB:
				if self.current_cs==EMPTY:
					self.callback(CreateRGBColor(0,0,0))
				else:
					r,g,b=self.color.getRGB()
					self.callback(CreateRGBAColor(r,g,b, self.color.alpha))
			elif self.cs_name.get()==CMYK:
				if self.current_cs==EMPTY:
					self.callback(CreateCMYKColor(0,0,0,1))
				else:
					c,m,y,k=self.color.getCMYK()
					self.callback(CreateCMYKAColor(c,m,y,k, self.color.alpha))
			elif self.cs_name.get()==REGISTRATION:
				self.callback(Registration_Black())
			elif self.cs_name.get()==SPOT:
				self.cs_name.set(self.current_cs)
			else:
				self.callback(None)
	
	def set_cs_name(self,color):
		if color is None:
			self.cs_name.set(EMPTY)
		elif color.model=='RGB':
			self.cs_name.set(RGB)
		elif color.model=='CMYK':
			self.cs_name.set(CMYK)
		elif color.model=='SPOT':
			if color.name=='All':
				self.cs_name.set(REGISTRATION)
			else:
				self.cs_name.set(SPOT)
		self.current_cs=self.cs_name.get()
				
				
	def set_color(self,color):
		self.color=color
		self.set_cs_name(self.color)
		
	def get_colorspace_name(self,value):
		if value==RGB:
			return 'RGB'
		elif value==CMYK:
			return 'CMYK'
		elif value==SPOT:
			return 'SPORT'
		elif value==REGISTRATION:
			return 'Registration color'
		else:
			return None
		
	def check_changes(self):
		if self.current_cs==self.cs_name.get():
			return False
		else:
			return True
				
	
		