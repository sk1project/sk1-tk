# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TButton
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
import app

class PluginPanel(TFrame,Publisher):
	
	receivers = [(SELECTION, 'issue', SELECTION)]
	
	name=''
	category=''
	title=''
	icon='strip_dialog'
	activated=0
	collapsed=0
	visible=0
	packed=0
	
	def init(self, master):
		self.master=master
		self.mw=app.mw
		self.document=self.mw.document
		TFrame.__init__(self, self.master, style='FlatFrame', borderwidth=0)
		self.top=TFrame(self, style='PWinHead', borderwidth=3)
		self.panel=TFrame(self, style='PWinBody', borderwidth=3)
		self.activated=1
		self.visible=1
		self.packed=1
		self.pack(side=TOP, fill=X)
		self.top.pack(side=TOP, fill=X)
		self.panel.pack(side=TOP, fill=BOTH, expand=1)
		
		font=app.config.preferences.normal_font+' bold'
		self.iconlabel=TLabel(self.top, style='PWLabel', image=self.icon)
		self.textlabel=TLabel(self.top, style='PWLabel', text=self.title, anchor=W, font=font)
		self.closebut=TButton(self.top, style='PWButton', image='close_pw', command=self.close_panel)
		self.collapsebut=TButton(self.top, style='PWButton', image='minimize_pw', command=self.collapse_panel)
		self.iconlabel.pack(side=LEFT, padx=2)
		self.textlabel.pack(side=LEFT, fill=BOTH, expand=1, padx=3)
		self.closebut.pack(side=RIGHT)
		self.collapsebut.pack(side=RIGHT)
		self.textlabel.bind("<Double-1>", self.collapse_panel)
		
		self.init_from_doc()
		self.subscribe_receivers()
		self.mw.Subscribe(DOCUMENT, self.doc_changed)
		
	def close_panel(self):
		self.forget()
		
	def collapse_panel(self, *arg):
		if self.collapsed:
			self.panel.pack(side=TOP, fill=BOTH, expand=1)
			self.collapsebut['image']='minimize_pw'
			self.collapsed=0
			self.textlabel['foreground']=app.uimanager.currentColorTheme.foreground
		else:
			self.panel.forget()
			self.collapsebut['image']='restore_pw'
			self.collapsed=1
			self.textlabel['foreground']=app.uimanager.currentColorTheme.menudisabledforeground
					
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
			