# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TLabel, TButton
from sk1.ttk_ext import TSpinbox
from app.conf.const import CHANGED
from Tkinter import LEFT, DoubleVar, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from sk1sdk.libttk import tooltips
from sk1.widgets.lengthvar import LengthVar

class JumpPanel(CtxSubPanel):
	
	name='JumpPanel'	
	
	def __init__(self, parent):
		self.my_changes=0
		
		CtxSubPanel.__init__(self, parent)
		self.var_jump_number=DoubleVar(self.mw.root)
		
		unit = config.preferences.default_unit
		var_jump_unit = StringVar(self.mw.root)
		self.var_jump = LengthVar(10, unit, self.var_jump_number, var_jump_unit)
		
		label = TLabel(self.panel, text=_("Jump:"))
		label.pack(side = LEFT, padx=2)
		self.entry_jump = TSpinbox(self.panel,  var=0, 
						vartype=1, textvariable = self.var_jump_number,
						min = 0, max = 1000, step = .1, width = 6, command = self.applyJump)
		self.entry_jump.pack(side = LEFT, padx=2)
		config.preferences.Subscribe(CHANGED, self.update)		
		self.var_jump.set(config.preferences.handle_jump)
		self.update(0, 0)	

	def update(self,*arg):
		if self.my_changes:
			self.my_changes=0
		else:
			self.var_jump.unit=config.preferences.default_unit
			self.var_jump.set(config.preferences.handle_jump)

		
	def applyJump(self,*arg):
		self.my_changes=1
		self.var_jump.unit=config.preferences.default_unit
		config.preferences.handle_jump=self.var_jump.get()
		self.var_jump.set(config.preferences.handle_jump)
