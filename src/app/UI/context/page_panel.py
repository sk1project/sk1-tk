# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TCombobox, TLabel,TCheckbutton
from app.UI.ttk_ext import TSpinbox
from app.conf.const import CHANGED
from Tkinter import LEFT, RIGHT, DoubleVar, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from math import floor, ceil
from app.Graphics.papersize import Papersize, PapersizesList
from app.UI.lengthvar import LengthVar
from app.Graphics.pagelayout import PageLayout

USER_SPECIFIC = '<Custom Size>'

class PagePanel(CtxSubPanel):
	
	name='PagePanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)		
		self.my_changes=0
		
		root=self.parent.mainwindow.root
		self.var_format_name = StringVar(root)
		self.var_format_name.set(config.preferences.default_paper_format)
		self.page_orientation=config.preferences.default_page_orientation
		
		label = TLabel(self.panel, text=_("Page: "))
		label.pack(side = LEFT)
		self.page_formats = TCombobox(self.panel, state='readonly', postcommand = self.set_format, 
									 values=self.make_formats(), width=17, style='ComboNormal',
									 textvariable=self.var_format_name)
		self.page_formats.pack(side = LEFT)
		
		
		var_width_number = DoubleVar(root)
		var_height_number = DoubleVar(root)
		var_width_unit = StringVar(root)
		var_height_unit = StringVar(root)
		unit = config.preferences.default_unit
		self.var_width = LengthVar(10, unit, var_width_number, var_width_unit)
		self.var_height = LengthVar(10, unit,var_height_number,var_height_unit)
		jump=config.preferences.default_unit_jump
		
		label = TLabel(self.panel, text=_("  H: "))
		label.pack(side = LEFT)
		self.widthentry = TSpinbox(self.panel, textvariable = var_width_number, command = self.update_size,
								vartype=1, min = 5, max = 50000, step = jump, width = 7)
		self.widthentry.pack(side = LEFT)
		
		label = TLabel(self.panel, text=_("  V: "))
		label.pack(side = LEFT)		
		self.heightentry = TSpinbox(self.panel, textvariable =var_height_number, command = self.update_size,
		 						vartype=1, min = 5, max = 50000, step = jump, width = 7)
		self.heightentry.pack(side = LEFT)
		
		self.portrait_val= StringVar(root)
		self.landscape_val = StringVar(root)
		
		label = TLabel(self.panel, text=' ')
		label.pack(side = LEFT)			
		self.portrait=TCheckbutton(self.panel, image='context_portrait', variable =self.portrait_val, 
								   command = self.set_portrait, style='ToolBarCheckButton')
		self.portrait.pack(side = LEFT)
		label = TLabel(self.panel, text=' ')
		label.pack(side = LEFT)	
		self.landscape=TCheckbutton(self.panel, image='context_landscape', variable =self.landscape_val, 
									command = self.set_landscape, style='ToolBarCheckButton')	
		self.landscape.pack(side = LEFT)
		self.update()
		config.preferences.Subscribe(CHANGED, self.update_pref)
		
		
	def make_formats(self):
		formats=()
		for format in PapersizesList:
			formats+=(format[0],)
		formats+=(USER_SPECIFIC,)
		return formats
	
	def set_portrait(self):
		self.page_orientation=0
		formatname = self.var_format_name.get()
		if formatname == USER_SPECIFIC:
			height, width=self.var_width.get(),self.var_height.get()
			self.var_width.set(width)
			self.var_height.set(height)
		self.set_size()
		
	def set_landscape(self):
		self.page_orientation=1
		formatname = self.var_format_name.get()
		if formatname == USER_SPECIFIC:
			height, width=self.var_width.get(),self.var_height.get()
			self.var_width.set(width)
			self.var_height.set(height)
		self.set_size()
			
	def set_size(self):
		self.var_width.UpdateNumber()
		self.var_height.UpdateNumber()
		self.my_changes=1		
		self.update()
				
	def set_format(self):		
		self.update()
		self.set_size()

	def update_pref(self, arg1, arg2):
		self.var_width.unit=config.preferences.default_unit
		self.var_height.unit=config.preferences.default_unit
		self.update()
		
	def update(self):		
		self.set_entry_sensitivity()
		if self.page_orientation:
			self.portrait_val.set('')
			self.landscape_val.set('1')
		else:
			self.portrait_val.set('1')
			self.landscape_val.set('')
		self.update_size_from_name(self.var_format_name.get())
		if self.my_changes:
			self.apply_settings()
			self.my_changes=0		
		
	def set_entry_sensitivity(self):
		formatname = self.var_format_name.get()
		if formatname != USER_SPECIFIC:
			self.widthentry.set_state("disabled")
			self.heightentry.set_state("disabled")
		else:
			self.widthentry.set_state("enabled")
			self.heightentry.set_state("enabled")
			
	def update_size(self, width, height):
		self.var_width.set(width)
		self.var_height.set(height)
			
	def update_size_from_name(self, formatname):
		if not formatname == USER_SPECIFIC:
			width, height = Papersize[formatname]
			if self.page_orientation:
				width, height = height, width
		else:
			width=self.var_width.get()
			height=self.var_height.get()
		self.update_size(width, height)
		
	def apply_settings(self):
		formatname = self.var_format_name.get()
		if formatname == USER_SPECIFIC:
			layout = PageLayout(width = self.var_width.get(),
								height = self.var_height.get(),
								orientation = 0)
		else:
			layout = PageLayout(formatname,
								orientation = self.page_orientation)
		self.parent.mainwindow.canvas.bitmap_buffer=None
		self.parent.mainwindow.document.SetLayout(layout)