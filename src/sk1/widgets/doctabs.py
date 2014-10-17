# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TButton
from Tkinter import LEFT, TOP, X, Y, BOTTOM
from sk1.tkext import UpdatedMenu, MakeCommand
from app.conf.const import UNDO
from app import _, Publisher
from sk1.dialogs import msgdialog
import os


LEFT_CORNER = 'DocTabsLeft'
LEFT_CORNER_ACTIVE = 'DocTabsLeftActive'
RIGHT_CORNER = 'DocTabsRight'

class TabsPanel(TFrame, Publisher):

	content = []
	stub = 1
	docmanager = None

	def __init__(self, parent, mainwindow):
		self.parent = parent
		self.mainwindow = mainwindow
		TFrame.__init__(self, self.parent, name='tabsPanel', style='FlatFrame',
					borderwidth=0)
		self.left_label = TLabel(self, style=LEFT_CORNER, image='space_3')
		self.right_label = TLabel(self, style=RIGHT_CORNER, image='space_3')
		self.stub_label = TLabel(self, style='DrawingAreaTop', image='space_5')
		self.stub_label.pack(side=TOP, fill=X)

	def ReSubscribe(self):
		self.docmanager.activedoc.Subscribe(UNDO, self.check_save_status)
		self.check_save_status()

	def check_save_status(self):
		for item in self.content:
			if item.is_Active:
				if self.docmanager.activedoc.WasEdited():
					item.setNotSaved()
				else:
					item.setNotSaved(1)
		self.updateTabNames()

	def refresh(self):
		self.stub_label.foget()
		for item in self.content:
			item.forget()

		if len(self.content) < 2:
			self.stub_label.pack(side=TOP, fill=X)
		else:
			for item in self.content:
				item.pack(side=LEFT)

	def check_state(self):
		if len(self.content) > 1 and self.stub:
			self.stub_label.forget()
			self.left_label.pack(side=LEFT, fill=Y)
			for item in self.content:
				item.pack(side=LEFT)
			self.right_label.pack(side=BOTTOM, fill=X)
			self.stub = 0
			return 0
		if len(self.content) < 2 and self.stub == 0:
			self.left_label.forget()
			for item in self.content:
				item.forget()
			self.right_label.forget()
			self.stub_label.pack(side=TOP, fill=X)
			self.stub = 1
			return 0
		return 1

	def stub(self):
		pass

	def setActive(self, tab):
		if not tab.is_Active:
			for item in self.content:
				item.setNonActive()
			tab.setActive()
			self.docmanager.SetActiveDocument(tab.document)
			self.ReSubscribe()
			if self.content[0].is_Active:
				self.left_label["style"] = LEFT_CORNER_ACTIVE
			else:
				self.left_label["style"] = LEFT_CORNER

	def addNewTab(self, doc):
		if doc.meta.fullpathname:
			name = doc.meta.filename
		else:
			name = os.path.splitext(doc.meta.filename)[0]
		tab = DocTab(self, name, document=doc)
		self.content.append(tab)
		if self.check_state() and self.stub == 0:
			self.right_label.forget()
			tab.pack(side=LEFT, fill=Y)
			self.right_label.pack(side=BOTTOM, fill=X)
		self.setActive(tab)
		return tab

	def closeTab(self, tab, exit_state=False):
		result = self.docmanager.save_doc_if_edited(tab.document)
		index = self.content.index(tab)
		if not result == msgdialog.Cancel:
			self.content.remove(tab)
			if not len(self.content):
				if not exit_state:
					self.docmanager.NewDocument()
			else:
				if tab.is_Active:
					if index == len(self.content):
						self.setActive(self.content[index - 1])
					else:
						self.setActive(self.content[index])
			if not exit_state:
				self.docmanager.CloseDocument(tab.document)
			tab.forget()
			self.check_state()
		return result

	def saveAll(self):
		for item in self.content:
			item.saveTab()

	def closeActiveTab(self):
		for item in self.content:
			if item.is_Active:
				self.closeTab(item)

	def updateTabNames(self):
		for item in self.content:
			item.updateTabName()

	def closeAllButThis(self, tab):
		self.setActive(tab)
		for item in [] + self.content:
			if not item.is_Active:
				if self.closeTab(item) == msgdialog.Cancel:
					return
		self.check_state()

	def closeAll(self, exit_state=False):
		for item in [] + self.content:
			self.setActive(item)
			if self.closeTab(item, exit_state) == msgdialog.Cancel:
				self.check_state()
				return msgdialog.Cancel
		return msgdialog.Yes



NORMAL_TAB = 'DocTabNormal'
ACTIVE_TAB = 'DocTabActive'

DOC_ICON = 'icon_sk1_14'
DOC_NOTSAVED = 'tab_tab_save'

class DocTab(TButton):

	is_Active = 0
	is_Saved = 1
	context_menu = None

	def __init__(self, parent, name, document=None, state=0):
		self.parent = parent
		self.name = name
		self.document = document
		if state:
			self.isActive = 1
			self.style = 'DocTabActive'
		TButton.__init__(self, self.parent, style=NORMAL_TAB, image=DOC_ICON,
						text=self.name.ljust(20), command=self.action)
		self.bind('<ButtonPress-3>', self.popup_context_menu)

	def action(self):
		self.parent.setActive(self)

	def setActive(self):
		self["style"] = ACTIVE_TAB
		self.is_Active = 1

	def setNonActive(self):
		self["style"] = NORMAL_TAB
		self.is_Active = 0

	def setNotSaved(self, value=0):
		if value:
			self['image'] = DOC_ICON
			self.is_Saved = 1
		else:
			self['image'] = DOC_NOTSAVED
			self.is_Saved = 0

	def popup_context_menu(self, event):
		self.context_menu = UpdatedMenu(self, [], tearoff=0, auto_rebuild=self.build_context_menu)
		self.context_menu.Popup(event.x_root, event.y_root)

	def build_context_menu(self):
		entries = [(_("New Document"), self.parent.docmanager.NewDocument, (), None, None, 'menu_tab_new')]
		if self.can_be_refreshed():
			entries += [(_("Refresh Document"), self.refreshTab, (), None, None, 'menu_tab_reload')]
		if self.can_be_saved():
			entries += [(_("Save Document"), self.saveTab, (), None, None, 'menu_file_save')]
		if self.can_be_closed_other():
			entries += [None, (_("Close Other Documents"), self.parent.closeAllButThis, (self), None, None, 'menu_tab_remove_other')]

		base_entries = [None,
			(_("Close Document"), self.parent.closeTab, (self), None, None, 'menu_file_close')]
		return map(MakeCommand, entries + base_entries)

	def can_be_saved(self):
		return self.document.WasEdited()

	def can_be_refreshed(self):
		return self.is_Active

	def can_be_closed_other(self):
		if len(self.parent.content) > 1:
			return 1
		else:
			return 0

	def refreshTab(self):
		self.parent.mainwindow.canvas.ForceRedraw()

	def saveTab(self):
		self.parent.docmanager.SaveDocument(self.document)
		self.updateTabName()
		self.setNotSaved(abs(self.can_be_saved() - 1))

	def updateTabName(self):
		self.name = os.path.splitext(self.document.meta.filename)[0]
		self['text'] = self.name.ljust(20)

	def stub(self):
		pass



