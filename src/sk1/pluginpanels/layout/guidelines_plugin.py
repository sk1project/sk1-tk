# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1.pluginpanels.ppanel import PluginPanel

from string import atoi

from Tkinter import DoubleVar, StringVar
from sk1.tkext import UpdatedButton, UpdatedListbox, UnitLabel

from sk1sdk.libttk import TScrollbar, TFrame, TLabel
from sk1.ttk_ext import TSpinbox

from Tkinter import BOTH, RIGHT, TOP, X, Y, E, W

from app.conf.const import GUIDE_LINES, SELECTION, DOCUMENT
from app import _, Point, config
import app

from sk1.widgets.lengthvar import LengthVar, create_unit_menu


class GuidelinesPanel(PluginPanel):
	name = 'Guidelines'
	title = _("Guides")


	def init(self, master):
		PluginPanel.init(self, master)
		top = self.panel

		grid_top = TFrame(top, borderwidth=2, style='FlatFrame')
		grid_top.pack(side=TOP, expand=1, fill=X)

		var_number = DoubleVar(top)
		var_unit = StringVar(top)
		self.var_pos = LengthVar(1.0, config.preferences.default_unit, var_number, var_unit, command=self.set_pos)

		top1 = TFrame(top, style='FlatFrame')
		top1.pack(side=TOP, expand=0, fill=BOTH)

		list_frame = TFrame(top1, style="RoundedFrame", borderwidth=5)
		list_frame.pack(side=TOP, expand=1, fill=BOTH)

		sb_vert = TScrollbar(list_frame)
		sb_vert.pack(side=RIGHT, fill=Y)
		guides = UpdatedListbox(list_frame, bg='white', borderwidth=0, selectborderwidth=0, width=20, height=8)
		guides.pack(expand=1, fill=BOTH)
		guides.Subscribe(SELECTION, self.select_guide)
		sb_vert['command'] = (guides, 'yview')
		guides['yscrollcommand'] = (sb_vert, 'set')
		self.guides = guides
		self.selected = None

		pos_frame = TFrame(top1, style='FlatFrame')
		pos_frame.pack(side=TOP, expand=0)

		top2 = TFrame(pos_frame, height=15, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		self.var_label = StringVar(top)
		self.var_label.set('X: ')

		labelunit = UnitLabel(pos_frame)
		labelunit.pack(side=RIGHT, expand=0, anchor=W)

		label = TLabel(pos_frame, image='space_6', style='FlatLabel')
		label.pack(side=RIGHT)

		self.entry = TSpinbox(pos_frame, var=0, vartype=1,
						min=-50000, max=50000, step=.1, width=6, command=self.pos_changed)
		self.entry.pack(side=RIGHT, expand=0, anchor=E)

		label = TLabel(pos_frame, textvariable=self.var_label, style='FlatLabel')
		label.pack(side=RIGHT, expand=0, anchor=E)

		frame = TFrame(top1, style='FlatFrame')
		frame.pack(side=TOP, fill=X)
		top2 = TFrame(frame, height=15, width=120, style='FlatFrame')
		top2.pack(side=TOP)

		button = UpdatedButton(frame, text=_("Add Horizontal Guide"), command=self.add_guide, args=1)
		button.pack(side=TOP)

		top2 = TFrame(frame, height=3, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		button = UpdatedButton(frame, text=_("Add Vertical Guide"), command=self.add_guide, args=0)
		button.pack(side=TOP)

		top2 = TFrame(frame, height=3, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		button = UpdatedButton(frame, text=_("Delete Guide"), command=self.del_guide)
		button.pack(side=TOP)

		top2 = TFrame(frame, height=5, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		app.mw.docmanager.activedoc.Subscribe(GUIDE_LINES, self.init_from_doc)
		app.mw.Subscribe(DOCUMENT, self.init_from_doc)
		self.init_from_doc()

	def set_unit(self, *rest):
		apply(self.var_pos.UpdateUnit, rest)
		self.update_list()

	def init_from_doc(self, *rest):
		self.guide_lines = self.document.GuideLines()
		self.guide_lines.reverse()
		self.update_list()

	def update_list(self):
		strings = []
		factor = self.var_pos.Factor()
		unit = self.var_pos.UnitName()
		if unit in ('in', 'cm'):
			prec = 2
		else:
			prec = 1
		for line in self.guide_lines:
			pos, horizontal = line.Coordinates()
			if horizontal:
				format = _("% 6.*f %s    horizontal")
			else:
				format = _("% 6.*f %s    vertical")
			strings.append(format % (prec, pos / factor, unit))
		self.guides.SetList(strings)
		self.select_index(self.selected)

	def select_index(self, index):
		if index is not None and index < len(self.guide_lines):
			self.guides.Select(index)
			self.select_guide()
		else:
			self.selected = None

	def set_pos(self, *rest):
		if self.selected is not None:
			self.document.MoveGuideLine(self.guide_lines[self.selected],
										self.var_pos.get())

	def select_guide(self, *rest):
		sel = self.guides.curselection()
		if sel:
			self.selected = atoi(sel[0])
			pos, horizontal = self.guide_lines[self.selected].Coordinates()
			self.var_pos.set(pos)
			self.entry.set_value(round(pos * 100 / self.var_pos.Factor()) / 100)
			if horizontal:
				self.var_label.set("Y: ")
			else:
				self.var_label.set("X: ")
		else:
			self.selected = None

	def del_guide(self, *rest):
		if self.selected is not None:
			line = self.guide_lines[self.selected]
			self.document.RemoveGuideLine(line)

	def add_guide(self, horizontal):
		length = len(self.guide_lines)
		self.document.AddGuideLine(Point(0, 0), horizontal)
		self.select_index(length)

	def pos_changed(self, *rest):
		self.var_pos.set(self.entry.get_value() * self.var_pos.Factor())
		self.set_pos()
		self.update_list()

instance = GuidelinesPanel()
app.layout_plugins.append(instance)
