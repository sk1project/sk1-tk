# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _, config
from app.conf import const
from app.conf.const import LAYOUT, SELECTION, DOCUMENT, EDITED, PAGE, LAYER
from app.Graphics.papersize import Papersize, PapersizesList
from app.Graphics.pagelayout import PageLayout, Portrait, Landscape

from sk1sdk.libtk.Tkinter import Frame, Label, StringVar, IntVar, DoubleVar
from app.UI.tkext import UpdatedButton, MyEntry, MyOptionMenu, UpdatedRadiobutton

from sk1sdk.libttk import TLabel, TFrame, TLabelframe
from app.UI.ttk_ext import TSpinbox, TComboSmall

from sk1sdk.libtk.Tkinter import RIGHT, BOTTOM, X, BOTH, LEFT, TOP, W, E, NW, SW, DISABLED, NORMAL
from app.UI.pluginpanels.ppanel import PluginPanel

import app
import os 
from app.UI.widgets.resframe import ResizableTFrame

from app.UI.widgets.scrolledcanvas import ScrolledCanvas
from app.UI.widgets.treewidget import TreeItem, TreeNode
from app.UI.widgets.resframe import ResizableTFrame

class LayerPlugin(PluginPanel):
	
	name='Layers'
	title = _("Layers")
	
	def init(self, master):
		PluginPanel.init(self, master)
		self.panel.forget()
		self.forget()
		self.pack(side=TOP, fill=X, padx=1, pady=1)
		self.panel =ResizableTFrame(self, master, size=150, orient=BOTTOM, min=10, max=500)
		self.panel.pack(side=BOTTOM, fill=BOTH, expand=1)
		top = TFrame(self.panel, style='RoundedFrame', borderwidth=5)
		top.pack(side=TOP, fill=BOTH, expand=1)

		
		self.ctheme=app.uimanager.currentColorTheme
		self.scanvas=ScrolledCanvas(top, bg=self.ctheme.editfieldbackground, height=150, width=170)
		self.scanvas.frame.pack(side=TOP, fill=BOTH, expand=1)
#		self.closebut.forget()
		tree = self.build_tree()
		item = DocTreeItem(tree, self)
		self.node = TreeNode(self.scanvas.canvas, None, item, self.ctheme)
		self.node.expand()
		
		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################

	def init_from_doc(self):
		self.Update()
#		self.issue(SELECTION)
	
	def subscribe_receivers(self):
#		self.document.Subscribe(SELECTION, self.Update)
		self.document.Subscribe(LAYOUT, self.Update)
		self.document.Subscribe(PAGE, self.Update)
		self.document.Subscribe(LAYER, self.Update)

	def unsubscribe_receivers(self):
#		self.document.Unsubscribe(SELECTION, self.Update)
		self.document.Unsubscribe(LAYOUT, self.Update)
		self.document.Unsubscribe(PAGE, self.Update)
		self.document.Unsubscribe(LAYER, self.Update)
		


	def Update(self, *arg):
		print os.path.splitext(self.document.meta.filename)[0]
		tree = self.build_tree()
		item = DocTreeItem(tree, self)
		#self.node.destroy()
		
		#self.node = TreeNode(self.scanvas.canvas, None, item, self.ctheme)
		self.node.item = item
		#self.node.lastvisiblechild()
		#self.node.expand()
		
		pass

	def build_tree(self):
		name = os.path.splitext(self.document.meta.filename)[0]
		tree=Doc('ROOT', name)
		#tree.contents=[]
		for page_idx in range(len(self.document.pages)):
			pages = Page('Page', _("Page %s" % (page_idx+1)), page_idx)
#			for layer in self.document.pages[page_idx]:
#				layers = Layer('Layer', layer.name)
#				pages.contents += [layers]
			tree.contents+=[pages]
		return tree










class Doc:
	
	name=''
	title=''
	icon='menu_doc_icon'
	
	def __init__(self, name,title):
		self.name=name
		self.title=title
		self.contents=[]
		self.IsEditable=False


class Page:
	
	name=''
	title=''
	icon='menu_doc_icon2'
	
	def __init__(self,name,title,index):
		self.name=name
		self.title=title
		self.contents=[]
		self.IsEditable=False
		self.index = index
		
	def setpage(self, index):
		pass
		#self.document.setActivePage(index)

class Layer:
	
	name=''
	title=''
	icon='strip_category'
	
	def __init__(self,name,title):
		self.name=name
		self.title=title
		self.contents=[]
		self.IsEditable=True













class DocTreeItem(TreeItem):

	def __init__(self, objects, container):
		self.objects = objects
		self.container = container

	def GetText(self):
		return self.objects.title

	def IsEditable(self):
		return self.objects.IsEditable

	def SetText(self, text):
		pass
	
	#def GetSelectedIconName(self):
		#print self.item.GetSelectedIconName()
		

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
			item = DocTreeItem(name, self.container)
			sublist.append(item)
		return sublist
	
	def addComment(self):
		pass
	
	def OnClick(self):
		#if not self.IsExpandable():
		#	print self.container.name
		#if isinstance(self.objects, Page):
		#	print "Страница"
		#	self.objects.setpage(self.objects.index)
		#print self.objects
		pass

		
		
		
		

instance=LayerPlugin()
app.layout_plugins.append(instance)