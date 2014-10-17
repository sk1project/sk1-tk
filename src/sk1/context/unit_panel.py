# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TLabel, TCombobox
from app.conf.const import CHANGED
from Tkinter import LEFT, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from sk1sdk.libttk import tooltips
from app.Lib.units import unit_names

class UnitPanel(CtxSubPanel):
	
	name='UnitPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.my_changes=0
		
		self.var_unit = StringVar(self.mw.root)
		self.var_unit.set(config.preferences.default_unit)
		
		label = TLabel(self.panel, text=_("Units:"))
		label.pack(side = LEFT, padx=2)
		self.entry_width = TCombobox(self.panel, state='readonly', postcommand = self.applyUnits, 
									 values=self.make_units(), width=4, style='ComboNormal', textvariable=self.var_unit)
		self.entry_width.pack(side = LEFT, padx=2)
		
		config.preferences.Subscribe(CHANGED, self.update)
		
	def applyUnits(self):
		self.my_changes=1
		config.preferences.default_unit=self.var_unit.get()
	
	def update(self,event, event2):	
		if self.my_changes:
			self.my_changes=0
		else:
			self.var_unit.set(config.preferences.default_unit)
	
	def make_units(self):
		units_tuple=()
		for unit in unit_names:
			units_tuple+=(unit,)		
		return units_tuple
			