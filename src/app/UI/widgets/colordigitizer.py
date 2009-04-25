# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TCombobox
from app.UI.ttk_ext import TSpinbox, TEntrybox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, CENTER, TOP,W, E,N, DISABLED, NORMAL
from Tkinter import StringVar, DoubleVar, IntVar
import PIL.Image

from app.conf.const import CHANGED, ConstraintMask

from app.Graphics import color

import string

class ColorDigitizer(TFrame):
	
	current_digitizer=None
	
	def __init__(self, parent, color=None, **kw):
		self.color=color
		self.parent=parent
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.rgb_digitizer=RGBDigitizer(self)
		self.cmyk_digitizer=CMYKDigitizer(self)
		self.empty_digitizer=EmptyDigitizer(self)
		self.current_digitizer=self.rgb_digitizer
		self.current_digitizer.pack(side=TOP)
		
		
	def set_color(self, color):
		self.color=color
		self.current_digitizer.forget()
		if color is None:
			self.current_digitizer=self.empty_digitizer
		elif color.model=='RGB':
			self.current_digitizer=self.rgb_digitizer
		elif color.model=='CMYK':
			self.current_digitizer=self.cmyk_digitizer
		elif color.model=='SPOT':
			if color.name=='Registration color':
				self.current_digitizer=self.rgb_digitizer
			else:
				self.current_chooser=self.rgb_digitizer
		self.current_digitizer.pack(side=TOP)
		self.current_digitizer.set_color(color)
		

class EmptyDigitizer(TFrame):
	
	def __init__(self, parent, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		
	def set_color(self, color):
		pass
	
class RGBDigitizer(TFrame):
	
	def __init__(self, parent, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.R_value=DoubleVar(0)
		self.G_value=DoubleVar(0)
		self.B_value=DoubleVar(0)
		
		self.HTML_value=StringVar('')
		
		
		html_frame = TFrame(self, borderwidth = 2, style='FlatFrame')
		html_frame.pack(side = BOTTOM)
		

		self.HTML_entry = TEntrybox(html_frame, text='#000000', width=10, 
								textvariable = self.HTML_value, command=self.html_component_changed)
		self.HTML_entry.pack(side = RIGHT)
		
		label = TLabel(html_frame, text = "HTML: ")
		label.pack(side = RIGHT)
		
		rgb_frame = TFrame(self, borderwidth = 2, style='FlatFrame')
		rgb_frame.pack(side = LEFT, padx=10)
		
		frame = TFrame(rgb_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "R: ")
		label.pack(side = LEFT)
		self.R_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.R_value, command=self.rgb_component_changed)
		self.R_spin.pack(side = RIGHT)

		frame = TFrame(rgb_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "G: ")
		label.pack(side = LEFT)
		self.G_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.G_value, command=self.rgb_component_changed)
		self.G_spin.pack(side = RIGHT)

		frame = TFrame(rgb_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "B: ")
		label.pack(side = LEFT)
		self.B_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.B_value, command=self.rgb_component_changed)
		self.B_spin.pack(side = RIGHT)
		
		cmyk_frame = TFrame(self, borderwidth = 2, style='FlatFrame')
		cmyk_frame.pack(side = LEFT)
		
		self.CMYK_label=TLabel(cmyk_frame, text='C:\nM:\nY:\nK:', justify=LEFT)
		self.CMYK_label.pack(side = LEFT)		
		
		
	def set_color(self, color):
		self.color=color
		r,g,b = color.getRGB()
		self.R_value.set(round(r*255, 2))
		self.G_value.set(round(g*255, 2))
		self.B_value.set(round(b*255, 2))
		c,m,y,k = color.getCMYK()
		self.CMYK_label['text']='C: %d\nM: %d\nY: %d\nK: %d'%(round(c*100, 2),round(m*100, 2),round(y*100, 2),round(k*100, 2))
		int_color=(round(r*255),round(g*255),round(b*255))
		self.HTML_value.set('#%02X%02X%02X'%int_color)
		
		
		
	def rgb_component_changed(self):
		pass
	
	def html_component_changed(self):
		pass
	
	
class CMYKDigitizer(TFrame):
	
	def __init__(self, parent, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.C_value=DoubleVar(0)
		self.M_value=DoubleVar(0)
		self.Y_value=DoubleVar(0)
		self.K_value=DoubleVar(0)
		
		cmyk_frame = TFrame(self, borderwidth = 2, style='FlatFrame')
		cmyk_frame.pack(side = LEFT, padx=10)
		
		frame = TFrame(cmyk_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "C: ")
		label.pack(side = LEFT)
		self.C_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.C_value, command=self.cmyk_component_changed)
		self.C_spin.pack(side = RIGHT)

		frame = TFrame(cmyk_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "M: ")
		label.pack(side = LEFT)
		self.M_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.M_value, command=self.cmyk_component_changed)
		self.M_spin.pack(side = RIGHT)

		frame = TFrame(cmyk_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "Y: ")
		label.pack(side = LEFT)
		self.Y_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.Y_value, command=self.cmyk_component_changed)
		self.Y_spin.pack(side = RIGHT)		

		frame = TFrame(cmyk_frame, borderwidth = 2, style='FlatFrame')
		frame.pack(side = TOP)
		label = TLabel(frame, text = "K: ")
		label.pack(side = LEFT)
		self.K_spin = TSpinbox(frame, min = 0, max = 255, step = 1, vartype = 0, width = 7, 
							textvariable = self.K_value, command=self.cmyk_component_changed)
		self.K_spin.pack(side = RIGHT)
		
		rgb_frame = TFrame(self, borderwidth = 2, style='FlatFrame')
		rgb_frame.pack(side = LEFT)
		
		self.RGB_label=TLabel(rgb_frame, text='R:\nG:\nB:', justify=LEFT)
		self.RGB_label.pack(side = LEFT)		
		
		
	def set_color(self, color):
		self.color=color
		c,m,y,k = color.getCMYK()
		self.C_value.set(round(c*100, 2))
		self.M_value.set(round(m*100, 2))
		self.Y_value.set(round(y*100, 2))
		self.K_value.set(round(k*100, 2))
		r,g,b = color.getRGB()
		text='R: %d\nG: %d\nB: %d'%(round(r*255, 2),round(g*255, 2),round(b*255, 2))
		int_color=(round(r*255),round(g*255),round(b*255))
		text+='\n\n#%02X%02X%02X'%int_color		
		self.RGB_label['text']=text	
		
		
	def cmyk_component_changed(self):
		pass

		