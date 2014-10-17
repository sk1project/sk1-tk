# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TButton, TLabel
from sk1.ttk_ext import TSpinbox
from app.conf.const import SELECTION, CHANGED, EDITED
from Tkinter import LEFT, RIGHT, DoubleVar, StringVar
from sk1sdk.libttk import tooltips
from subpanel import CtxSubPanel
from app import  _, config
from math import floor, ceil
from sk1.widgets.lengthvar import LengthVar

class ResizePanel(CtxSubPanel):
	
	name='ResizePanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.my_changes=0
		self.var_width_number=DoubleVar(self.mw.root)
		self.var_height_number=DoubleVar(self.mw.root)

		var_width_unit = StringVar(self.mw.root)
		var_height_unit = StringVar(self.mw.root)
		
		unit = config.preferences.default_unit
		self.var_width = LengthVar(10, unit, self.var_width_number, var_width_unit)
		self.var_height = LengthVar(10, unit,self.var_height_number,var_height_unit)
		
		jump=config.preferences.default_unit_jump
		self.var_width.set(0)
		self.var_height.set(0)
		
		label = TLabel(self.panel, image='size_h')
		label.pack(side = LEFT)
		
		self.entry_width = TSpinbox(self.panel,  var=0, vartype=1, textvariable = self.var_width_number,
						min = 0, max = 50000, step = jump, width = 6, command = self.applyResize)
		tooltips.AddDescription(self.entry_width, _("Width of selection"))
		self.entry_width.pack(side = LEFT, padx=5)


		label = TLabel(self.panel, image='size_v')
		label.pack(side = LEFT)
		
		self.entry_height = TSpinbox(self.panel,  var=0, vartype=1, textvariable = self.var_height_number,
						min = 0, max = 50000, step = jump, width = 6, command = self.applyResize)
		tooltips.AddDescription(self.entry_height, _("Height of selection"))
		self.entry_height.pack(side = LEFT, padx=5)
		
		self.ReSubscribe()
		config.preferences.Subscribe(CHANGED, self.update_pref)

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.Update)	
		self.doc.Subscribe(EDITED, self.update)
		self.Update()
						
	def applyResize(self, event):
		try:
			x=self.var_width.get()
			y=self.var_height.get()
			br=self.doc.selection.coord_rect
			hor_sel=br.right - br.left
			ver_sel=br.top - br.bottom
		except:
			return
		
		if hor_sel:
			xx=x / hor_sel
		else:
			xx = 1
		
		if ver_sel:
			yy = y / ver_sel
		else:
			yy = 1
		
		self.doc.ScaleSelected(xx, yy)
		self.update_size()
		
	def update(self, issue):
		self.Update()
		
	def Update(self):
		if len(self.doc.selection.GetInfo()):
			self.update_size()
			
	def update_size(self):	
		self.var_width.unit=config.preferences.default_unit
		self.var_height.unit=config.preferences.default_unit
		br=self.doc.selection.coord_rect
		width=br.right - br.left
		height=br.top - br.bottom
		self.var_width.set(width)
		self.var_height.set(height)
		self.entry_width.step=config.preferences.default_unit_jump
		self.entry_height.step=config.preferences.default_unit_jump
		
	def update_pref(self, arg1, arg2):
		if self.my_changes:
			self.my_changes=0
		else:
			if len(self.doc.selection.GetInfo()):
				self.update_size()
		
		
		
		