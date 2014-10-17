# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TButton
from Tkinter import TOP, LEFT, RIGHT, BOTTOM, X, Y, BOTH, W, S, N, E, NORMAL, DISABLED, END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
from sk1.tkext import UpdatedButton
from app import _
import app

class PluginPanel(TFrame, Publisher):

	receivers = [(SELECTION, 'issue', SELECTION)]

	name = ''
	category = ''
	title = ''
	icon = 'strip_dialog'
	contents = []
	category = ''
	category_title = ''

	activated = 0
	collapsed = 0
	visible = 0
	packed = 0
	fill = X
	expand = 0

	def init(self, master):
		self.master = master
		self.mw = app.mw
		self.pcontainer = self.master.master
		self.document = self.mw.document
		TFrame.__init__(self, self.master, style='FlatFrame', borderwidth=0)
		self.top = TFrame(self, style='PWinHead', borderwidth=3)
		self.panel = TFrame(self, style='PWinBody', borderwidth=3)
		self.activated = 1
		self.visible = 1
		self.packed = 1

		for item in self.pcontainer.loaded:
			if not item.collapsed:
				item.collapse_panel()

		self.pack(side=TOP, fill=self.fill, expand=self.expand, padx=1, pady=1)
		self.top.pack(side=TOP, fill=X)
		self.panel.pack(side=TOP, fill=BOTH, expand=1)

		self.iconlabel = TLabel(self.top, style='PWLabel', image=self.icon)
		self.textlabel = TLabel(self.top, style='PWLabel', text=self.title, anchor=W)
		if not 'bold' in self.textlabel['font'].split():
			self.textlabel['font'] += ' bold'
		self.closebut = TButton(self.top, style='PWButton', image='close_pw', command=self.close_panel)
		self.collapsebut = TButton(self.top, style='PWButton', image='minimize_pw', command=self.click)
		self.iconlabel.pack(side=LEFT, padx=2)
		self.textlabel.pack(side=LEFT, fill=BOTH, expand=1, padx=3)
		self.closebut.pack(side=RIGHT)
		self.collapsebut.pack(side=RIGHT)
		self.textlabel.bind("<Button-1>", self.click)
		self.mw.Subscribe(DOCUMENT, self.doc_changed)

	def click(self, *args):
		if self.collapsed:
			self.decollapse_panel()
		else:
			self.collapse_panel()

	def close_panel(self):
		self.packed = 0
		self.forget()
		self.pcontainer.remove_plugin(self)

	def restore_panel(self):
		for item in self.pcontainer.loaded:
			if not item.collapsed:
				item.collapse_panel()
		self.forget()
		self.packed = 1
		self.pack(side=TOP, fill=self.fill, expand=self.expand, padx=1, pady=1)
		self.decollapse_panel()

	def decollapse_panel(self, *arg):
		if self.collapsed:
			for item in self.pcontainer.loaded:
				if not item.collapsed:
					item.collapse_panel()
			self.forget()
			self.pack(side=TOP, fill=X, padx=1, pady=1)
			self.panel.pack(side=TOP, fill=BOTH, expand=1)
			self.collapsebut['image'] = 'minimize_pw'
			self.collapsed = 0
			self.textlabel['foreground'] = app.uimanager.currentColorTheme.foreground
			self.forget()
			self.pack(side=TOP, fill=self.fill, expand=self.expand, padx=1, pady=1)

	def collapse_panel(self, *arg):
		if not self.collapsed:
			self.panel.forget()
			self.collapsebut['image'] = 'restore_pw'
			self.collapsed = 1
			self.textlabel['foreground'] = app.uimanager.currentColorTheme.menudisabledforeground
			self.forget()
			self.pack(side=TOP, fill=X, expand=0, padx=1, pady=1)


	def doc_changed(self, *arg):
		self.SetDocument(self.mw.document)

	def doc_has_selection(self):
		return self.document.HasSelection()

	def subscribe_receivers(self):
		pass

	def unsubscribe_receivers(self):
		pass

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

	def create_std_buttons(self, master):
		frame = TFrame(master, style='FlatFrame', borderwidth=2)

		button = UpdatedButton(frame, text=_("Apply"), command=self.do_apply, sensitivecb=self.can_apply)
		button.pack(side=TOP)
		return frame
