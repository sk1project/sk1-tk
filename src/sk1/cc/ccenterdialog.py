# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
import app, os, string, sys
from sk1.dialogs.dialog import ModalDialog
from sk1.widgets.resframe import ResizableTFrame
from app import dialogman

from sk1sdk.libttk import TButton, TLabel, TFrame, TScrollbar
from sk1.ttk_ext import TSpinbox
from Tkinter import Canvas
from Tkinter import TOP, LEFT, RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END, NONE

from sk1.widgets.scrolledcanvas import ScrolledCanvas
from sk1.widgets.treewidget import TreeItem, TreeNode



class ControlCenterDialog(ModalDialog):

	class_name = 'ControlCenter'
	current_plugin=None
	
	def __init__(self, master, dlgname = '__dialog__'):
		self.master=master
		self.title = _("sK1 Preferences")
		ModalDialog.__init__(self, master, name = dlgname)
	
	def build_dlg(self):
		self.root = TFrame(self.top, style='FlatFrame', borderwidth = 10)
		self.root.pack(side = TOP, fill = BOTH, expand = 1)
		
		##### top panel #########################RoundedFrame
		
		toppanel = TFrame(self.root, style='FlatFrame')		
		toppanel.pack(side = TOP, fill = BOTH, expand = 1)
		
		rpanel = ResizableTFrame(toppanel, self.top, size=220, orient=RIGHT)		
		rpanel.pack(side = LEFT, fill = Y)
		
		panel = TFrame(rpanel.panel, style='RoundedFrame', borderwidth = 5)		
		panel.pack(side = LEFT, fill = BOTH, expand = 1)
		
		ctheme=app.uimanager.currentColorTheme	   

		self.scanvas=ScrolledCanvas(panel, bg=ctheme.editfieldbackground, height=420, width=200)
		self.scanvas.frame.pack(side=LEFT, fill=BOTH, expand=1)
		
		self.plugpanel = TFrame(toppanel, style='FlatFrame')		
		self.plugpanel.pack(side = RIGHT, fill = BOTH, expand = 1)
		
#		lab=TLabel(self.plugpanel, style='FlatLabel', text='Test label')
#		lab.pack(side = LEFT)
		
		##### line #########################
				
		line = TLabel(self.root, style='HLine2')
		line.pack(side = TOP, fill = X)				

		##### bottom panel #########################
		
		botpanel = TFrame(self.root, style='FlatFrame')		
		botpanel.pack(side = BOTTOM, fill = X, expand=0)

		
		cancel_bt = TButton(botpanel, text=_("Cancel"), command=self.cancel)
		cancel_bt.pack(side = RIGHT)
		
		apply_bt = TButton(botpanel, text=_("Apply"), command=self.do_apply)
		apply_bt.pack(side = RIGHT, padx=10)
		
		ok_bt = TButton(botpanel, text=_("OK"), command=self.ok)
		ok_bt.pack(side = RIGHT)
		
		help_bt = TButton(botpanel, text=_("Help"), state='disabled')
		help_bt.pack(side = LEFT)
		
		rdefs_bt = TButton(botpanel, text=_("Restore Defaults"), command=self.do_restore)
		rdefs_bt.pack(side = LEFT, padx=10)
		
		self.focus_widget = cancel_bt
		
		self.top.bind('<Escape>', self.cancel)
		self.top.protocol('WM_DELETE_WINDOW', self.cancel)
		self.width=700	
		self.height=500
		self.build_plugins_tree()
				
		item = PluginsTreeItem(self.root_cat, self)		
		node = TreeNode(self.scanvas.canvas, None, item, ctheme, 26)
		node.expand()
		self.loadByName('general')
		
	def ok(self, *arg):
		for plugin in self.plugins:
			plugin.apply()
		self.close_dlg()
		
	def do_apply(self, *arg):
		self.current_plugin.apply()
		
	def do_restore(self, *arg):
		self.current_plugin.restore()
	
	def cancel(self, *arg):
		self.close_dlg(None)
		
	def build_plugins_tree(self):
		self.plugins=app.pref_plugins		
		
		self.create_categories()
		for cat in self.pcats:
			for item in self.plugins:
				if item.category==cat.name:
					cat.contents.append(item)			
			
		for item in self.plugins:
			if item.category=='root':
				self.root_cat.contents.append(item)

		for cat in self.pcats:
			self.root_cat.contents.append(cat)			
				
		
	def create_categories(self):
		self.categories={}
		for item in self.plugins:
			item.activated=0
			if not item.category in self.categories:
				self.categories[item.category]=item.category_name
		self.pcats=[]
		for item in self.categories:
			if not item=='root':
				self.pcats.append(PluginCategory(item,self.categories[item]))		
		for item in self.pcats:
			item.contents=[]
		self.root_cat=PluginCategory('root',_('Preferences'))
		self.root_cat.contents=[]		
	
	def loadByName(self,name):		
		for item in self.plugins:
			if item.name==name:
				if self.current_plugin==item:
					return
				old_plugin=self.current_plugin
				self.current_plugin=item
		if not self.current_plugin.activated:
			self.current_plugin.init(self.plugpanel)
		if not old_plugin is None: 
			old_plugin.forget()
		self.current_plugin.pack(side=TOP, fill=BOTH)
	
	
	
class PluginCategory:
	
	name=''
	title=''
	icon=''
	contents=[]
	
	def __init__(self,name,title):
		self.name=name
		self.title=title
		self.icon='category_'+name		
		
		
class PluginsTreeItem(TreeItem):

	def __init__(self, objects, container):
		self.objects = objects
		self.container = container

	def GetText(self):
		return self.objects.title

	def IsEditable(self):
		return False

	def SetText(self, text):
		pass

	def GetIconName(self):
		return self.objects.icon
			
	def IsExpandable(self): 
		if(len(self.objects.contents)):
			return True
		else:
			return False

	def GetSubList(self):
		sublist = []
		for name in self.objects.contents:
			item = PluginsTreeItem(name,self.container)
			sublist.append(item)
		return sublist
	
	def addComment(self):
		pass
	
	def OnDoubleClick(self):
		if not self.IsExpandable():
			self.container.loadByName(self.objects.name)
			
	def OnClick(self):
		if not self.IsExpandable():
			self.container.loadByName(self.objects.name)
	
	
def ControlCenter(master):
	dlg = ControlCenterDialog(master)
	dlg.RunDialog()
	