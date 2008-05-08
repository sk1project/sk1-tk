# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TFrame, TLabel
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
import app

class PluginPanel(TFrame,Publisher):
	
	receivers = [(SELECTION, 'issue', SELECTION)]
	
	name=''
	category=''
	title=''
	activated=0
	collapsed=0
	
	def init(self, master):
		self.master=master
		self.mw=app.mw
		self.document=self.mw.document
		TFrame.__init__(self, self.master, style='RoundedFrame', borderwidth=5)
		self.top=TFrame(self, style='RoundedFrame', borderwidth=5)
		self.activated=1
		self.pack()
		self.top.pack()
		
		self.init_from_doc()
		self.subscribe_receivers()
		self.mw.Subscribe(DOCUMENT, self.doc_changed)
		
	def doc_changed(self, doc):
		self.document=self.mw.document
		self.SetDocument(self.document)

	def doc_has_selection(self):
		return self.document.HasSelection()
	
	def subscribe_receivers(self):
		for info in self.receivers:
			apply(self.document.Subscribe,
					(info[0], getattr(self, info[1])) + info[2:])

	def unsubscribe_receivers(self):
		for info in self.receivers:
			apply(self.document.Unsubscribe,
					(info[0], getattr(self, info[1])) + info[2:])
			

	def subscribe_receivers(self):
		for info in self.receivers:
			apply(self.document.Subscribe,
					(info[0], getattr(self, info[1])) + info[2:])

	def unsubscribe_receivers(self):
		for info in self.receivers:
			apply(self.document.Unsubscribe,
					(info[0], getattr(self, info[1])) + info[2:])

	def SetDocument(self, doc):
		if self.document:
			self.unsubscribe_receivers()
		self.document = doc
		self.init_from_doc()
		self.subscribe_receivers()
		
	def init_from_doc(self):
		# Called whenever the document changes and from __init__
		pass

	def Update(self):
		# Called when the selection changes.
		pass

	def do_apply(self):
		# called by the `Apply' standard button to apply the settings
		pass

	def can_apply(self):
		return 1
			