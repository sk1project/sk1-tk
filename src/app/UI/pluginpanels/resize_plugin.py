# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel
from Tkinter import DoubleVar, Spinbox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, GROOVE, E, DISABLED, NORMAL
from app.UI.tkext import UpdatedButton
from app.UI.ttk_ext import TSpinbox

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect
from app.conf import const
import app

from ppanel import PluginPanel

from math import floor, ceil

class ResizePanel(PluginPanel):
	name='Resize'
	title = _("Resize")


	def init(self, master):
		PluginPanel.init(self, master)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)


		steps_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		steps_frame.pack(side = TOP)
		label = TLabel(steps_frame, style='FlatLabel', text = _("  H (mm): "))
		label.pack(side = LEFT, anchor = E)

		self.var_width=DoubleVar(top)
		self.var_height=DoubleVar(top)
		self.var_width.set(0)
		self.var_height.set(0)

		self.entry_width = TSpinbox(steps_frame,  var=0, vartype=1, textvariable = self.var_width, 
									min = -50000, max = 50000, step = .1, width = 6)
								
		self.entry_width.pack(side = LEFT, anchor = E)

		steps_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		steps_frame.pack(side = TOP)
		label = TLabel(steps_frame, style='FlatLabel', text = _("  V (mm): "))
		label.pack(side = LEFT, anchor = E)
		
		self.entry_height = TSpinbox(steps_frame,  var=0, vartype=1, textvariable = self.var_height, 
									min = -50000, max = 50000, step = .1, width = 6)
								
		self.entry_height.pack(side = LEFT, anchor = E)


		button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		button_frame.pack(side = BOTTOM, fill = BOTH)
		

		self.update_buttons = []
		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_resize,
								sensitivecb = self.doc_can_move)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X, pady=5)
		self.Subscribe(SELECTION, button.Update)
		
		button = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy,
								sensitivecb = self.doc_can_move)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)
				
		self.document.Subscribe(SELECTION, self.init_from_doc)	
		self.document.Subscribe(EDITED, self.init_from_doc)
		self.init_from_doc()

###############################################################################
	def doc_can_move(self):
		return (len(self.document.selection) > 0)


	def init_from_doc(self, *arg):
		self.Update()
		self.issue(SELECTION)

	def Update(self):
		try:
				br=app.mw.canvas.SelectionSizeData()
				hor_sel=ceil(floor(10**3*(br.right - br.left)/2.83465)/10)/100
				ver_sel=ceil(floor(10**3*(br.top - br.bottom)/2.83465)/10)/100
				self.var_width.set(hor_sel)
				self.var_height.set(ver_sel)
		except:
				self.var_width.set(0)
				self.var_height.set(0)


	def apply_resize(self):
		try:
			x=self.var_width.get()
			y=self.var_height.get()
			br=app.mw.canvas.SelectionSizeData()
			hor_sel=ceil(floor(10**3*(br.right - br.left)/2.83465)/10)/100
			ver_sel=ceil(floor(10**3*(br.top - br.bottom)/2.83465)/10)/100
		except:
			return

		self.document.ScaleSelected(x/hor_sel, y/ver_sel)


	def apply_to_copy(self):
		try:
			x=self.var_width.get()
			y=self.var_height.get()
			br=app.mw.canvas.SelectionSizeData()
			hor_sel=ceil(floor(10**3*(br.right - br.left)/2.83465)/10)/100
			ver_sel=ceil(floor(10**3*(br.top - br.bottom)/2.83465)/10)/100
		except:
			return

		self.document.ApplyToDuplicate()
		self.document.ScaleSelected(x/hor_sel, y/ver_sel)

instance=ResizePanel()
app.transform_plugins.append(instance)
