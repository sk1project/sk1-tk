# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Tkinter import Frame, Radiobutton, IntVar, StringVar, Label
from Ttk import TLabel, TFrame, TRadiobutton, TLabelframe
from Tkinter import BOTH, LEFT, RIGHT, TOP, X, Y, BOTTOM, W

from app.conf.const import SELECTION
from app.conf import const
from app import _

from app.UI.tkext import UpdatedButton, UpdatedCheckbutton, UpdatedRadiobutton

import app
from app.UI.pluginpanels.ppanel import PluginPanel

def make_button(*args, **kw):
	kw['style'] ='FineRadiobutton'
	return apply(TRadiobutton, args, kw)

class AlignPlugin(PluginPanel):
	
	name='Alignment'
	title = _("Alignment")
	
	def init(self, master):
		PluginPanel.init(self, master)
		top = self.panel
		
		frame_bot = TFrame(top, borderwidth=3, style='FlatFrame')
		frame_bot.pack(side = BOTTOM, expand = 0, fill = X)
		apply_button = UpdatedButton(frame_bot, text = _("Apply"), command = self.apply, sensitivecb = self.can_apply, width=15)
		apply_button.pack(side = BOTTOM)
		self.Subscribe(SELECTION, apply_button.Update)

		label=TLabel(top, text=_(" Alignment type "), style="FlatLabel")
		label.pack()
		framec=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		framec.pack(side = TOP, fill=X, padx=2, pady=2)
		
		framex = TFrame(framec, style='FlatFrame')
		framex.pack(side = TOP, expand = 0, padx = 5, pady = 5)
		
		framey = TFrame(framec, style='FlatFrame')
		framey.pack(side = TOP, expand = 0, padx = 5, pady = 5)


		x_pixmaps = ['aoleft', 'aocenterh', 'aoright']
		y_pixmaps = ['aotop', 'aocenterv', 'aobottom']
		self.var_x = IntVar(top)
		self.var_x.set(0)
		self.value_x = 0
		self.var_y = IntVar(top)
		self.var_y.set(0)
		self.value_y = 0

		for i in range(1, 4):
			button = make_button(framex, image = x_pixmaps[i - 1], value = i, variable = self.var_x, command = self.set_x)
			button.pack(side = LEFT, padx = 3)
			button = make_button(framey, image = y_pixmaps[i - 1], value = i, variable = self.var_y, command = self.set_y)
			button.pack(side = LEFT, padx = 3)
		
		label=TLabel(top, text=_(" Relative to "), style="FlatLabel")
		label.pack()
		rel_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		rel_frame.pack(side = TOP, fill=X, padx=2, pady=2)
		
		button_frame=TFrame(rel_frame, style='FlatFrame')
		button_frame.pack(side = TOP)

		self.var_reference = StringVar(top)
		self.var_reference.set('selection')
		radio = UpdatedRadiobutton(button_frame, value = 'selection', text = _("Selection"), variable = self.var_reference, command = apply_button.Update)
		radio.pack(side=TOP, anchor=W)
		radio = UpdatedRadiobutton(button_frame, value = 'lowermost', text = _("Lowermost "), variable = self.var_reference, command = apply_button.Update)
		radio.pack(side=TOP, anchor=W)
		radio = UpdatedRadiobutton(button_frame, value = 'page', text = _("Page"), variable = self.var_reference, command = apply_button.Update)
		radio.pack(side=TOP, anchor=W)

	def init_from_doc(self):
		self.issue(SELECTION)

	def set_x(self):
		value = self.var_x.get()
		if value == self.value_x:
			self.var_x.set(0)
			self.value_x = 0
		else:
			self.value_x = value
			
	def set_y(self):
		value = self.var_y.get()
		if value == self.value_y:
			self.var_y.set(0)
			self.value_y = 0
		else:
			self.value_y = value

	def apply(self):
		x = self.var_x.get()
		y = self.var_y.get()
		reference = self.var_reference.get()
		self.document.AlignSelection(x, y, reference = reference)

	def reset(self):
		self.var_x.set(0)
		self.var_y.set(0)

	def can_apply(self):
		if self.document.CountSelected() > 1:
			return 1
		reference = self.var_reference.get()
		return reference == 'page' and self.doc_has_selection()
	
instance=AlignPlugin()
app.effects_plugins.append(instance)

