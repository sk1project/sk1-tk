# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TButton
from Tkinter import LEFT, RIGHT, TOP, X, Y, BOTH, BOTTOM
from tkext import MenuCommand, UpdatedMenu, MakeCommand
from app import _

LEFT_CORNER='DocTabsLeft'
LEFT_CORNER_ACTIVE='DocTabsLeftActive'
RIGHT_CORNER='DocTabsRight'

class TabsPanel(TFrame):

	content=[]
	stub=1
	
	def __init__(self, parent, mainwindow):
		self.parent=parent
		self.mainwindow=mainwindow
		self.doc=self.mainwindow.document
		TFrame.__init__(self, self.parent, name = 'tabsPanel', style='FlatFrame', borderwidth=0)
		self.test()
#		self.stub_label=TLabel(self.panel, style='DrawingAreaTop', image='space_5')
#		self.stub_label.pack(side = TOP, fill = X)

	def refresh(self):
		self.stub_label.foget()
		for item in self.content:
			item.forget()
			
		if len(self.content)<2:
			self.stub_label.pack(side = TOP, fill = X)
		else:			
			for item in self.content:
				item.pack(side = LEFT)			

	def test(self):
		self.left_label=TLabel(self, style=LEFT_CORNER, image='space_3')
		self.left_label.pack(side = LEFT, fill = Y)
		for name in ('1','2','3','4'):
			name='New Document '+name
			label=DocTab(self,name)
			label.pack(side = LEFT, fill = Y)
			self.content.append(label)
		self.content[2].setActive()
				
		self.right_label=TLabel(self, style=RIGHT_CORNER, image='space_3')
		self.right_label.pack(side = BOTTOM, fill = X)
		
	def stub(self):
		pass
	
	def setActive(self,tab):
		for item in self.content:
			item.setNonActive()
		tab.setActive()
		if self.content[0].is_Active:
			self.left_label["style"]=LEFT_CORNER_ACTIVE
		else:
			self.left_label["style"]=LEFT_CORNER


NORMAL_TAB='DocTabNormal'
ACTIVE_TAB='DocTabActive'

DOC_ICON='icon_sk1_14'		

class DocTab(TButton):
	
	is_Active=0
	context_menu = None	
	
	def __init__(self, parent, name, state=0):
		self.parent=parent
		self.name=name
		if state:
			self.isActive=1
			self.style='DocTabActive'		
		TButton.__init__(self, self.parent, style=NORMAL_TAB, image=DOC_ICON, 
						text=' '+self.name+' ', command=self.action)
		self.bind('<ButtonPress-3>', self.popup_context_menu)
	
	def action(self):	
		self.parent.setActive(self)
		
	def setActive(self):
		self["style"]=ACTIVE_TAB
		self.is_Active=1
		
	def setNonActive(self):
		self["style"]=NORMAL_TAB
		self.is_Active=0

	def popup_context_menu(self, event):
		if self.context_menu is None:
			self.context_menu = UpdatedMenu(self, [], tearoff = 0, auto_rebuild = self.build_context_menu)
		self.context_menu.Popup(event.x_root, event.y_root)
		
	def build_context_menu(self):
		entries = [
			(_("New Tab"), self.stub,(),None,None,'menu_tab_new'),
			(_("Refresh Tab"), self.stub,(),self.can_be_refreshed,None,'menu_tab_reload'),
			(_("Save Document"), self.stub,(),self.can_be_saved,None,'menu_file_save'),
			None,
			(_("Close Other Tabs"), self.stub,(),self.can_be_closed_other,None,'menu_tab_remove_other'),
			None,
			(_("Close Tab"), self.stub,(),None,None,'menu_file_close')
			]
		return map(MakeCommand, entries)		

	def can_be_saved(self):
		return 0
	
	def can_be_refreshed(self):
		return self.is_Active
	
	def can_be_closed_other(self):
		if len(self.parent.content)>1:
			return 1
		else:
			return 0
		
	def stub(self):
		pass		
		
		
				
		