# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TLabel, TButton
from app.UI.ttk_ext import TSpinbox
from app.conf.const import CHANGED
from Tkinter import LEFT, DoubleVar
from subpanel import CtxSubPanel
from app import  _, config
from app.UI import tooltips

class JumpPanel(CtxSubPanel):
	
	name='JumpPanel'	
	
	def __init__(self, parent):
		self.my_changes=0
		
		CtxSubPanel.__init__(self, parent)
		self.var_jump=DoubleVar(self.parent.mainwindow.root)
		self.var_jump.set(config.preferences.handle_jump)
		
		label = TLabel(self.panel, text=_(" Jump: "))
		label.pack(side = LEFT)
		self.entry_jump = TSpinbox(self.panel,  var=config.preferences.handle_jump, 
						vartype=1, textvariable = self.var_jump,
						min = 0, max = 1000, step = .1, width = 6, command = self.applyJump)
		self.entry_jump.pack(side = LEFT)
		config.preferences.Subscribe(CHANGED, self.update)		

	def update(self,event, event2):	
		if self.my_changes:
			self.my_changes=0
		else:
			self.var_jump.set(config.preferences.handle_jump)

		
	def applyJump(self,  event):
		config.preferences.handle_jump=self.var_jump.get()
