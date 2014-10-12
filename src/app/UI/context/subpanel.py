# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel
from app.conf.const import DOCUMENT
from Tkinter import LEFT, RIGHT

class CtxSubPanel:
	
	def __init__(self, parent):
		self.receivers={}
		self.parent=parent
		self.mw=self.parent.mainwindow
		self.doc=self.parent.mainwindow.document
		self.panel=TFrame(parent.panel, style='FlatFrame', borderwidth=0)
		self.separator = TLabel(self.panel, image = "toolbar_sep")
		self.mw.Subscribe(DOCUMENT, self.doc_changed)
		self.setNormal()
		
	def ReSubscribe(self):
		pass

	def doc_changed(self, doc):
		self.doc=doc
		self.ReSubscribe()
		
	def setLast(self):
		self.separator.forget()
		
	def setNormal(self):
		self.separator.pack(side = RIGHT, padx=2)