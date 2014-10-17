# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCheckbutton, TButton
from Tkinter import IntVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL
from sk1.widgets.colorspacesel import ColorSpaceSelector
from sk1.widgets.colorchooser import ColorChooserWidget
from sk1.widgets.colordigitizer import ColorDigitizer
from sk1sdk.libttk import tooltips

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect, mw
from app.conf import const
import app, copy
from sk1.tkext import UpdatedButton

from sk1.pluginpanels.ppanel import PluginPanel

from math import floor, ceil
from app.Graphics import color
from app.Graphics.pattern import SolidPattern, EmptyPattern_

BLACK_COLOR = color.CreateCMYKColor(0, 0, 0, 1)

class FillPanel(PluginPanel):
	name = 'SolidFill'
	title = _("Solid Fill")
	initial_color = None
	current_color = None
	default_color = BLACK_COLOR
	sign = 'tools_color_fill'


	def init(self, master):
		PluginPanel.init(self, master)
		
		self.initial_color = self.default_color
		self.current_color = copy.copy(self.initial_color)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side=TOP, fill=BOTH)

		self.selector = ColorSpaceSelector(top, self.refresh_widgets, self.current_color, self.sign)
		self.selector.pack(side=TOP, expand=1, fill=X)
		
		self.picker = ColorChooserWidget(top, self.refresh_widgets, self.current_color)
		self.picker.pack(side=TOP, expand=1, fill=X)	
		
		self.digitizer = ColorDigitizer(top, self.refresh_widgets, self.current_color)
		self.digitizer.pack(side=TOP, expand=1, fill=X)


		button = UpdatedButton(top, text=_("Apply"),
								command=self.apply_pattern,
								sensitivecb=self.is_selection)
		button.pack(side=BOTTOM, expand=1, fill=X)
		self.Subscribe(SELECTION, button.Update)
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=1)
		button_frame.pack(side=BOTTOM, fill=X, pady=5)
		
		button = TButton(button_frame, style='TSmallbutton', text=' ', image='small_colorpicker', command=self.copy_from)
		button.pack(side=LEFT)
		tooltips.AddDescription(button, _("Copy From..."))
		
		button = TButton(button_frame, style='TSmallbutton', text=' ', image='restore_color', command=self.restore_color)
		button.pack(side=LEFT, padx=5)
		tooltips.AddDescription(button, _("Restore color"))
		
		self.var_autoupdate = IntVar(top)
		self.var_autoupdate.set(1)
		
		self.autoupdate_check = TCheckbutton(button_frame, text=_("Auto Update"), variable=self.var_autoupdate,
											command=self.init_from_doc)
		self.autoupdate_check.pack(side=RIGHT, anchor=W, padx=10)

		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################
	def is_selection(self):
		return (len(self.document.selection) > 0)
	
	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.init_from_doc)	
		self.document.Subscribe(EDITED, self.init_from_doc)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.init_from_doc)	
		self.document.Unsubscribe(EDITED, self.init_from_doc)

	def init_from_doc(self, *arg):
		if self.var_autoupdate.get():
			self.Update()
		self.issue(SELECTION)

	def Update(self):		
		self.initial_color = self.get_object_color()
		self.current_color = copy.copy(self.initial_color)		
		self.refresh_widgets(self.current_color)
	
	def refresh_widgets(self, color):
		self.current_color = color
		self.selector.set_color(self.current_color)
		self.picker.set_color(self.current_color)
		self.digitizer.set_color(self.current_color)


	def apply_pattern(self):
		if self.current_color is None:
			self.mw.no_pattern('fill')
		else:
			self.mw.canvas.FillSolid(self.current_color)
		self.Update()

	def copy_from(self):
		self.mw.canvas.PickObject(self.update_from_object)
		
	def update_from_object(self, obj):
		if obj is not None:
			self.refresh_widgets(self.init_from_properties(obj.Properties()))
	
	def restore_color(self):
		self.refresh_widgets(copy.copy(self.initial_color))
	
	def get_object_color(self):
		if self.document.HasSelection():
			if len(self.document.selection) > 1:
				info, obj = self.document.selection.GetInfo()[0]
				properties = obj.Properties()
			else:
				properties = self.document.CurrentProperties()
			return self.init_from_properties(properties)
		else:
			return self.default_color
		
	def init_from_properties(self, properties):
		if properties and properties.HasFill() and properties.fill_pattern.__class__ == SolidPattern:
			return properties.fill_pattern.Color()
		else:
			return None

instance = FillPanel()
app.objprop_plugins.append(instance)
