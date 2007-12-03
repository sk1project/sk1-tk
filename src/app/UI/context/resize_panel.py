# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TButton, TLabel
from app.UI.ttk_ext import TSpinbox
from app.conf.const import SELECTION, CHANGED, EDITED
from Tkinter import LEFT, RIGHT, DoubleVar, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from math import floor, ceil
from app.UI.lengthvar import LengthVar

class ResizePanel(CtxSubPanel):
	
	name='ResizePanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.my_changes=0
		self.var_width_number=DoubleVar(self.parent.mainwindow.root)
		self.var_height_number=DoubleVar(self.parent.mainwindow.root)

		var_width_unit = StringVar(self.parent.mainwindow.root)
		var_height_unit = StringVar(self.parent.mainwindow.root)
		
		unit = config.preferences.default_unit
		self.var_width = LengthVar(10, unit, self.var_width_number, var_width_unit)
		self.var_height = LengthVar(10, unit,self.var_height_number,var_height_unit)
		
		jump=config.preferences.default_unit_jump
		self.var_width.set(0)
		self.var_height.set(0)
		
		label = TLabel(self.panel, text=_("H: "))
		label.pack(side = LEFT)
		self.entry_width = TSpinbox(self.panel,  var=0, vartype=1, textvariable = self.var_width_number,
						min = 0, max = 50000, step = jump, width = 6, command = self.applyResize)
		self.entry_width.pack(side = LEFT)

		label = TLabel(self.panel, text=_("  V: "))
		label.pack(side = LEFT)
		self.entry_height = TSpinbox(self.panel,  var=0, vartype=1, textvariable = self.var_height_number,
						min = 0, max = 50000, step = jump, width = 6, command = self.applyResize)
		self.entry_height.pack(side = LEFT)
		
		self.parent.mainwindow.document.Subscribe(SELECTION, self.Update)	
		self.parent.mainwindow.document.Subscribe(EDITED, self.update)
		config.preferences.Subscribe(CHANGED, self.update_pref)
		
	def applyResize(self, event):
		try:
			x=self.var_width.get()
			y=self.var_height.get()
			br=self.parent.mainwindow.document.selection.coord_rect
			hor_sel=br.right - br.left
			ver_sel=br.top - br.bottom
		except:
			return
		self.parent.mainwindow.document.ScaleSelected(x/hor_sel, y/ver_sel)
		self.update_size()
		
	def update(self, issue):
		self.Update()
		
	def Update(self):
		mw=self.parent.mainwindow
		if len(mw.document.selection.GetInfo()):
			self.update_size()
			
	def update_size(self):	
		self.var_width.unit=config.preferences.default_unit
		self.var_height.unit=config.preferences.default_unit
		br=self.parent.mainwindow.document.selection.coord_rect
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
			mw=self.parent.mainwindow
			if len(mw.document.selection.GetInfo()):
				self.update_size()
		
		
		
		