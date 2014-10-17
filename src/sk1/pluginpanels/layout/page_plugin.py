# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _, config
from app.conf import const
from app.conf.const import LAYOUT, DOCUMENT
from app.Graphics.papersize import Papersize, PapersizesList
from app.Graphics.pagelayout import PageLayout, Portrait, Landscape

from Tkinter import Frame, Label, StringVar, IntVar, DoubleVar
from sk1.tkext import UpdatedButton, MyEntry, MyOptionMenu, UpdatedRadiobutton

from sk1sdk.libttk import TLabel, TFrame, TLabelframe
from sk1.ttk_ext import TSpinbox, TComboSmall

from Tkinter import RIGHT, BOTTOM, X, BOTH, LEFT, TOP, W, E, NW, SW, DISABLED, NORMAL
from ppanel import PluginPanel

from sk1.widgets.lengthvar import LengthVar, create_unit_menu

import app



class PagePlugin(PluginPanel):
	
	name='Page'
	title = _("Page")
	
	def init(self, master):
		PluginPanel.init(self, master)
		self.top = self.panel
		root = self.top
		
		self.USER_SPECIFIC = _("<Custom Size>")
		
		top_root = TFrame(root, borderwidth=2, style='FlatFrame')
		top_root.pack(side = TOP, expand = 1, fill = X)
		
		top=TLabelframe(top_root, text='Page format')
		top.pack(side = TOP, fill=X, pady=2)

		
		var_width_number = DoubleVar(root)
		var_height_number = DoubleVar(root)
		var_width_unit = StringVar(root)
		var_height_unit = StringVar(root)
		unit = config.preferences.default_unit
		self.var_width = LengthVar(10, unit, var_width_number, var_width_unit)
		self.var_height = LengthVar(10, unit,var_height_number,var_height_unit)


# ===========================================================
		format_frame = TFrame(top, borderwidth=0, style='FlatFrame')
		format_frame.pack(side = TOP, expand = 1, fill = X, pady = 4)

		format_names = map(lambda t: t[0], PapersizesList)
		format_names.append(self.USER_SPECIFIC)
		self.var_format_name = StringVar(root)
		
		format_menu =TComboSmall(format_frame, format_names, command = self.choose_format,
								 variable = self.var_format_name, width=17)
		format_menu.configure(width = max(map(len, format_names)))
		format_menu.pack(side = RIGHT, expand = 1, fill = X)

# =====================		
		size_frame = TFrame(top, borderwidth=0, style='FlatFrame')
		size_frame.pack(side = TOP, fill = X, expand = 1, padx = 4, pady = 4)		
		label = TLabel(size_frame, text ="H: ", style='FlatLabel')
		
		self.widthentry = TSpinbox(size_frame, textvariable = var_width_number, command = self.var_width.UpdateNumber,
								vartype=1, min = 5, max = 50000, step = 1, width = 7)
		self.widthentry.pack(side = RIGHT, anchor = E, padx = 5)
		label.pack(side = RIGHT, anchor = E)
		
		size_frame = TFrame(top, borderwidth=0, style='FlatFrame')
		size_frame.pack(side = TOP, fill = X, expand = 1, padx = 4, pady = 4)
		label = TLabel(size_frame, text = "V: ", style='FlatLabel')
			
		self.heightentry = TSpinbox(size_frame, textvariable =var_height_number, command = self.var_height.UpdateNumber,
		 						vartype=1, min = 5, max = 50000, step = 1, width = 7)
		self.heightentry.pack(side = RIGHT, anchor = E, padx = 5)
		label.pack(side = RIGHT, anchor = E)
		
		size_frame = TFrame(top, borderwidth=0, style='FlatFrame')
		size_frame.pack(side = TOP, fill = X, expand = 1, padx = 4, pady = 4)

		def CallBoth(arg, x = self.var_width, y = self.var_height):
			x.UpdateUnit(arg)
			y.UpdateUnit(arg)

		optmenu = create_unit_menu(size_frame, CallBoth, variable = var_width_unit, width = 3)
		optmenu.pack(side = RIGHT, padx = 5)

		label = TLabel(size_frame, text = "Units: ", style='FlatLabel')
		label.pack(side = RIGHT)
#---------------------------------------------------------------------------------------------------------------------
		middle=TLabelframe(top_root, text='Page orientation')
		middle.pack(side = TOP, fill=X, pady=2)
		
		self.label = TLabel(middle, image = 'portrait', style='FlatLabel')
		self.label.pack(side = LEFT, padx=4)

		orientation_frame = TFrame(middle, borderwidth=0, style='FlatFrame')
		orientation_frame.pack(side = LEFT, expand = 1, fill = X)
		
		self.var_orientation = IntVar(root)
		radio = UpdatedRadiobutton(orientation_frame, text = _("Portrait"),
									variable = self.var_orientation,
									value = Portrait,
									command = self.choose_orientation)
		radio.pack(side = TOP, anchor=W)
		
		radio = UpdatedRadiobutton(orientation_frame, text = _("Landscape"),
									variable = self.var_orientation,
									value = Landscape,
									command = self.choose_orientation)
		radio.pack(side = TOP, anchor=W)

#---------------------------------------------------------------------------------------------------------------------
		button_frame = TFrame(top_root, borderwidth=1, style='FlatFrame')
		button_frame.pack(side = BOTTOM, fill = BOTH, pady=2)
		button = UpdatedButton(button_frame, text = _("Apply"), command = self.apply_settings, width=15)
		button.pack(side = BOTTOM)
		
		app.mw.docmanager.activedoc.Subscribe(LAYOUT, self.init_from_doc)
		app.mw.Subscribe(DOCUMENT, self.init_from_doc)
		

	def init_from_doc(self, *arg):
		self.Update()

	def update_size_from_name(self, formatname):
		width, height = Papersize[formatname]
		if self.var_orientation.get() == Landscape:
			width, height = height, width
		self.update_size(width, height)

	def update_size(self, width, height):
		self.var_width.set(width)
		self.var_height.set(height)

	def Update(self):
		layout = self.document.Layout()
		formatname = layout.FormatName()
		self.var_orientation.set(layout.Orientation())
		if self.var_orientation.get() == Landscape:
			self.label["image"] = 'landscape'
		else:
			self.label["image"] = 'portrait'
		if formatname and formatname != self.USER_SPECIFIC:
			self.update_size_from_name(formatname)
		else:
			formatname = self.USER_SPECIFIC
			self.update_size(layout.Width(), layout.Height())
		self.var_format_name.set(formatname)
		self.set_entry_sensitivity()

	def set_entry_sensitivity(self):
		formatname = self.var_format_name.get()
		if formatname != self.USER_SPECIFIC:
			self.widthentry.set_state("disabled")
			self.heightentry.set_state("disabled")
		else:
			self.widthentry.set_state("enabled")
			self.heightentry.set_state("enabled")

	def choose_format(self, formatname):
		self.var_format_name.set(formatname)
		if formatname != self.USER_SPECIFIC:
			self.update_size_from_name(formatname)
		self.set_entry_sensitivity()

	def choose_orientation(self):
		name = self.var_format_name.get()
		if name != self.USER_SPECIFIC:
			self.update_size_from_name(name)
		if self.var_orientation.get() == Landscape:
			self.label["image"] = 'landscape'
		else:
			self.label["image"] = 'portrait'	

	def apply_settings(self):
		formatname = self.var_format_name.get()
		if formatname == self.USER_SPECIFIC:
			layout = PageLayout(width = self.var_width.get(),
								height = self.var_height.get(),
								orientation = self.var_orientation.get())
		else:
			layout = PageLayout(formatname,
								orientation = self.var_orientation.get())
		self.document.SetLayout(layout)

instance=PagePlugin()
app.layout_plugins.append(instance)