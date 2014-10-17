# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCombobox
from sk1.ttk_ext import TSpinbox, TEntrybox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, CENTER, TOP, W, E, N, DISABLED, NORMAL
from Tkinter import StringVar, DoubleVar, IntVar
from PIL import Image

from app.Graphics.color import CreateRGBAColor, CreateCMYKAColor

from app.conf.const import CHANGED, ConstraintMask

from app.Graphics import color
from app import _

import string

class ColorDigitizer(TFrame):
	
	current_digitizer = None
	
	def __init__(self, parent, callback, color=None, **kw):
		self.color = color
		self.parent = parent
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.rgb_digitizer = RGBDigitizer(self, callback)
		self.cmyk_digitizer = CMYKDigitizer(self, callback)
		self.spot_digitizer = SPOTDigitizer(self)
		self.empty_digitizer = EmptyDigitizer(self)
		self.current_digitizer = self.empty_digitizer
		self.current_digitizer.pack(side=LEFT)
		self.set_color(color)
		
		
	def set_color(self, color):
		self.color = color	
		if color is None:
			if not self.current_digitizer.__class__ == EmptyDigitizer:
				self.set_digitizer(self.empty_digitizer)
		elif color.model == 'RGB':
			if not self.current_digitizer.__class__ == RGBDigitizer:
				self.set_digitizer(self.rgb_digitizer)
		elif color.model == 'CMYK':
			if not self.current_digitizer.__class__ == CMYKDigitizer:
				self.set_digitizer(self.cmyk_digitizer)
		elif color.model == 'SPOT':
			if not self.current_digitizer.__class__ == SPOTDigitizer:
				self.set_digitizer(self.spot_digitizer)		
		self.current_digitizer.set_color(color)
		
	def set_digitizer(self, widget):
		self.current_digitizer.forget()
		self.current_digitizer = widget
		self.current_digitizer.pack(side=TOP, fill=X)
		

class EmptyDigitizer(TFrame):
	
	def __init__(self, parent, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		
	def set_color(self, color):
		pass
	
class RGBDigitizer(TFrame):
	
	def __init__(self, parent, callback, **kw):
		self.callback = callback
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.R_value = IntVar(0)
		self.G_value = IntVar(0)
		self.B_value = IntVar(0)
		self.A_value = IntVar(0)
		
		self.HTML_value = StringVar('')
		
			
		b = TLabel(self, style='HLine')
		b.pack(side=BOTTOM, fill=X)	
		
		frame = TFrame(self, borderwidth=0, style='FlatFrame')
		frame.pack(side=BOTTOM)
		label = TLabel(frame, text=_("Alpha channel: "))
		label.pack(side=LEFT)
		self.A_spin = TSpinbox(frame, min=0, max=255, step=1, vartype=0, width=7,
							textvariable=self.A_value, command=self.rgb_component_changed)
		self.A_spin.pack(side=RIGHT)
		
		b = TLabel(self, style='HLine')
		b.pack(side=BOTTOM, fill=X)
		
		
		html_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		html_frame.pack(side=BOTTOM)
		

		self.HTML_entry = TEntrybox(html_frame, text='#000000', width=10,
								textvariable=self.HTML_value, command=self.html_component_changed)
		self.HTML_entry.pack(side=RIGHT)
		
		label = TLabel(html_frame, text="HTML: ")
		label.pack(side=RIGHT)
		
		rgb_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		rgb_frame.pack(side=LEFT, padx=10)
		
		frame = TFrame(rgb_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="R: ")
		label.pack(side=LEFT)
		self.R_spin = TSpinbox(frame, min=0, max=255, step=1, vartype=0, width=7,
							textvariable=self.R_value, command=self.rgb_component_changed)
		self.R_spin.pack(side=RIGHT)

		frame = TFrame(rgb_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="G: ")
		label.pack(side=LEFT)
		self.G_spin = TSpinbox(frame, min=0, max=255, step=1, vartype=0, width=7,
							textvariable=self.G_value, command=self.rgb_component_changed)
		self.G_spin.pack(side=RIGHT)

		frame = TFrame(rgb_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="B: ")
		label.pack(side=LEFT)
		self.B_spin = TSpinbox(frame, min=0, max=255, step=1, vartype=0, width=7,
							textvariable=self.B_value, command=self.rgb_component_changed)
		self.B_spin.pack(side=RIGHT)
		
		cmyk_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		cmyk_frame.pack(side=LEFT)
		
		self.CMYK_label = TLabel(cmyk_frame, text='C:\nM:\nY:\nK:', justify=LEFT)
		self.CMYK_label.pack(side=LEFT)
		
		
		
	def set_color(self, color):
		self.color = color
		self.R_value.set(int(round(color.red * 255)))
		self.G_value.set(int(round(color.green * 255)))
		self.B_value.set(int(round(color.blue * 255)))
		self.A_value.set(int(round(color.alpha * 255)))
		c, m, y, k = color.getCMYK()
		self.CMYK_label['text'] = 'C: %.2f\nM: %.2f\nY: %.2f\nK: %.2f' % (round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2))
		int_color = (round(color.red * 255), round(color.green * 255), round(color.blue * 255))
		self.HTML_value.set('#%02X%02X%02X' % int_color)
		
		
		
	def rgb_component_changed(self, *arg):
		r = self.R_value.get() / 255.0
		g = self.G_value.get() / 255.0
		b = self.B_value.get() / 255.0
		a = self.A_value.get() / 255.0
		self.callback(CreateRGBAColor(r, g, b, a))
	
	def html_component_changed(self, *arg):
		html = self.HTML_value.get()
		try:     
			r = int(string.atoi(html[1:3], 0x10)) / 255.0
			g = int(string.atoi(html[3:5], 0x10)) / 255.0 
			b = int(string.atoi(html[5:], 0x10)) / 255.0
		except:
			r = round(self.color.red * 255, 2)
			g = round(self.color.green * 255, 2)
			b = round(self.color.blue * 255, 2)		
		self.callback(CreateRGBAColor(r, g, b, self.A_value.get() / 255.0))
	
	
class CMYKDigitizer(TFrame):
	
	def __init__(self, parent, callback, **kw):
		self.callback = callback
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.C_value = DoubleVar(0)
		self.M_value = DoubleVar(0)
		self.Y_value = DoubleVar(0)
		self.K_value = DoubleVar(0)
		self.A_value = DoubleVar(0)
		
		b = TLabel(self, style='HLine')
		b.pack(side=BOTTOM, fill=X)
		
		frame = TFrame(self, borderwidth=0, style='FlatFrame')
		frame.pack(side=BOTTOM)
		label = TLabel(frame, text=_("Opacity: "))
		label.pack(side=LEFT)
		self.A_spin = TSpinbox(frame, min=0, max=255, step=1, vartype=0, width=7,
							textvariable=self.A_value, command=self.cmyk_component_changed)
		self.A_spin.pack(side=RIGHT)
		
		b = TLabel(self, style='HLine')
		b.pack(side=BOTTOM, fill=X)
		
		cmyk_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		cmyk_frame.pack(side=LEFT, padx=10)
		
		frame = TFrame(cmyk_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="C: ")
		label.pack(side=LEFT)
		self.C_spin = TSpinbox(frame, min=0, max=100, step=1, vartype=1, width=7,
							textvariable=self.C_value, command=self.cmyk_component_changed)
		self.C_spin.pack(side=RIGHT)

		frame = TFrame(cmyk_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="M: ")
		label.pack(side=LEFT)
		self.M_spin = TSpinbox(frame, min=0, max=100, step=1, vartype=1, width=7,
							textvariable=self.M_value, command=self.cmyk_component_changed)
		self.M_spin.pack(side=RIGHT)

		frame = TFrame(cmyk_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="Y: ")
		label.pack(side=LEFT)
		self.Y_spin = TSpinbox(frame, min=0, max=100, step=1, vartype=1, width=7,
							textvariable=self.Y_value, command=self.cmyk_component_changed)
		self.Y_spin.pack(side=RIGHT)		

		frame = TFrame(cmyk_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="K: ")
		label.pack(side=LEFT)
		self.K_spin = TSpinbox(frame, min=0, max=100, step=1, vartype=1, width=7,
							textvariable=self.K_value, command=self.cmyk_component_changed)
		self.K_spin.pack(side=RIGHT)
		
		rgb_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		rgb_frame.pack(side=LEFT)
		
		self.RGB_label = TLabel(rgb_frame, text='R:\nG:\nB:', justify=LEFT)
		self.RGB_label.pack(side=LEFT)		
		
		
	def set_color(self, color):
		self.color = color
		c, m, y, k = color.getCMYK()
		self.C_value.set(round(c * 100, 2))
		self.M_value.set(round(m * 100, 2))
		self.Y_value.set(round(y * 100, 2))
		self.K_value.set(round(k * 100, 2))
		self.A_value.set(int(round(color.alpha * 100)))
		r, g, b = color.getRGB()
		text = 'R: %d\nG: %d\nB: %d' % (round(r * 255, 2), round(g * 255, 2), round(b * 255, 2))
		int_color = (round(r * 255), round(g * 255), round(b * 255))
		text += '\n\n#%02X%02X%02X' % int_color		
		self.RGB_label['text'] = text	
		
		
	def cmyk_component_changed(self, *arg):
		c = self.C_value.get() / 100.0
		m = self.M_value.get() / 100.0
		y = self.Y_value.get() / 100.0
		k = self.K_value.get() / 100.0		
		a = self.A_value.get() / 100.0
		self.callback(CreateCMYKAColor(c, m, y, k, a))
	
class SPOTDigitizer(TFrame):
	
	def __init__(self, parent, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)	
			
		spot_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		spot_frame.pack(side=TOP)
		
		label = TLabel(spot_frame, text=_('Color name:'), justify=LEFT)
		label.pack(side=TOP)
		
		self.colorname_value = StringVar('')
		
		self.colorname = TEntrybox(spot_frame, text='', width=25, textvariable=self.colorname_value)
		self.colorname.set_state('readonly')
		self.colorname.pack(side=BOTTOM, fill=X)
		
		cmyk_frame = TFrame(self, borderwidth=2, style='FlatFrame')
		cmyk_frame.pack(side=TOP)
		
		self.CMYK_label = TLabel(cmyk_frame, text='C:\nM:\nY:\nK:', justify=LEFT)
		self.CMYK_label.pack(side=LEFT, padx=10)
		
		self.RGB_label = TLabel(cmyk_frame, text='R:\nG:\nB:', justify=LEFT)
		self.RGB_label.pack(side=LEFT, padx=10)
		
		self.HTML_label = TLabel(self, text='HTML:', justify=LEFT)
		self.HTML_label.pack(side=BOTTOM, pady=5)		
		
	def set_color(self, color):
		self.color = color
		c, m, y, k = color.getCMYK()
		self.CMYK_label['text'] = 'C: %d\nM: %d\nY: %d\nK: %d' % (round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2))
				
		r, g, b = color.getRGB()
		text = 'R: %d\nG: %d\nB: %d' % (round(r * 255, 2), round(g * 255, 2), round(b * 255, 2))
		self.RGB_label['text'] = text	
		
		int_color = (round(r * 255), round(g * 255), round(b * 255))
		text = 'HTML: #%02X%02X%02X' % int_color
		self.HTML_label['text'] = text	
		
		if color.name == 'All':
			self.colorname_value.set(color.toString())
		else:
			self.colorname_value.set(color.name)		



		
