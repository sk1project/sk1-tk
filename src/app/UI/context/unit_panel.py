# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TLabel, TCombobox
from app.conf.const import CHANGED
from Tkinter import LEFT, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from app.UI import tooltips
from app.Lib.units import unit_names

class UnitPanel(CtxSubPanel):
	
	name='UnitPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.my_changes=0
		
		self.var_unit = StringVar(self.parent.mainwindow.root)
		self.var_unit.set(config.preferences.default_unit)
		
		label = TLabel(self.panel, text=_("Units: "))
		label.pack(side = LEFT)
		self.entry_width = TCombobox(self.panel, state='readonly', postcommand = self.applyUnits, 
									 values=self.make_units(), width=3, style='ComboNormal', textvariable=self.var_unit)
		self.entry_width.pack(side = LEFT)
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
			