# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel
from sk1sdk.libtk.Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
from app.UI.widgets.resframe import ResizableTFrame
import app

from pbrowser import PluginBrowser

class PluginContainer(ResizableTFrame):
	
	visible=0
	loaded=[]
	activated=[]
	rborder=None
	
	def __init__(self, master, root, mw, cnf={}, **kw):
		self.mw=mw
		self.root=root
		self.master=master
		ResizableTFrame.__init__(self, master, root, size=200, orient=LEFT, min=100, max=300)
		self.browserframe=ResizableTFrame(self.panel, root, size=10, orient=BOTTOM, min=10, max=500)
		self.browserframe.pack(side=TOP, fill=X)
		self.plugins=app.objprop_plugins+app.layout_plugins+app.transform_plugins
		self.plugins+=app.effects_plugins+app.extentions_plugins+app.shaping_plugins
		
		self.pbrowser=PluginBrowser()		
		
	def showHide(self):
		if not self.pbrowser.activated:
			self.pbrowser.init(self.browserframe.panel, self)
			self.pbrowser.forget()
			self.pbrowser.pack(side=TOP, fill=BOTH, expand=1)
			
		if not self.visible:
			self.visible=1
			self.rborder.pack(side=RIGHT, fill=Y)
			self.pack(side=RIGHT, fill=Y)						
		else:
			self.visible=0
			self.rborder.forget()
			self.forget()
			self.mw.canvas.clear_buffer_bitmap()

	def loadByName(self,name):
		plugin=None
		for item in self.plugins:
			if item.name==name:
				plugin=item
		if plugin is not None:
			if plugin.activated:
				if not plugin.packed:
					plugin.restore_panel()
				if plugin.collapsed:
					plugin.collapse_panel()
			else:
				plugin.init(self.panel)
		