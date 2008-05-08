# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TFrame, TLabel
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE

class PluginContainer(TFrame):
	
	visible=0
	
	def __init__(self, master, mw, cnf={}, **kw):
		self.mw=mw
		self.master=master
		TFrame.__init__(self, master, kw)
		#############
		self.test=TLabel(self,text='   PROBE   ')
		self.test.pack(side=TOP)
		
	def showHide(self):
		if not self.visible:
			self.visible=1
			self.pack(side=RIGHT, fill=Y)
		else:
			self.visible=0
			self.forget()