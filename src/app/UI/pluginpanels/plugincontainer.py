# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
from app.UI.widgets.resframe import ResizableTFrame
import app

class PluginContainer(ResizableTFrame):
	
	visible=0
	loaded=[]
	activated=[]
	rborder=None
	
	def __init__(self, master, mw, cnf={}, **kw):
		self.mw=mw
		self.master=master
		ResizableTFrame.__init__(self, master, mw, size=180, orient=LEFT, min=100, max=300)
		self.browserframe=ResizableTFrame(self.panel, mw, size=250, orient=BOTTOM, min=100, max=500)
		self.browserframe.pack(side=TOP, fill=X)
		from align_plugin import AlignPlugin
		self.testpw=AlignPlugin()		
		
		
	def showHide(self):
		if not self.testpw.activated:
			self.testpw.init(self.browserframe.panel)
			
		if not self.visible:
			self.visible=1
			self.rborder.pack(side=RIGHT, fill=Y)
			self.pack(side=RIGHT, fill=Y)
#			if len(self.loaded)==0:
#				inst=app.ppdict['Test Panel']
#				loaded.append(inst)
#				inst.init(self)
							
		else:
			self.visible=0
			self.rborder.forget()
			self.forget()
			
		