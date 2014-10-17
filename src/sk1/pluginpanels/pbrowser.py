# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TLabel, TFrame, TRadiobutton, LabelFrame
from Tkinter import BOTH, LEFT, RIGHT, TOP, X, Y, BOTTOM, W
from sk1.widgets.scrolledcanvas import ScrolledCanvas
from sk1.widgets.treewidget import TreeItem, TreeNode

from app import _


import app
from ppanel import PluginPanel

class PluginBrowser(PluginPanel):

	name = 'PluginBrowser'
	title = _("Plugin Browser")
	icon = 'strip_pbrowser'

	built = 0
	fill = BOTH
	expand = 1

	def init(self, master):
		PluginPanel.init(self, master)
		top = self.panel
		ctheme = app.uimanager.currentColorTheme

		self.browserframe = TFrame(top, style='RoundedFrame', borderwidth=5)
		self.browserframe.pack(side=TOP, fill=BOTH, expand=1)
		self.scanvas = ScrolledCanvas(self.browserframe, bg=ctheme.editfieldbackground, height=150, width=170)
		self.scanvas.frame.pack(side=TOP, fill=BOTH, expand=1)
		self.after_idle(self.rebuild_pb)


	def rebuild_pb(self):
		self.build_plugins_tree()
		ctheme = app.uimanager.currentColorTheme
		item = PluginsTreeItem(self.ptree, self.pcontainer)
		node = TreeNode(self.scanvas.canvas, None, item, ctheme)
		node.expand()

	def build_plugins_tree(self):
		self.ptree = PluginCategory('ROOT', _("Plugins"))
		objprop_group = PluginCategory('ObjProp', _("Object properties"))
		layout_group = PluginCategory('Layout', _("Layout"))
		transform_group = PluginCategory('Transform', _("Transformation"))
		shaping_group = PluginCategory('Shaping', _("Shaping"))
		effects_group = PluginCategory('Effects', _("Effects"))
		extentions_group = PluginCategory('Extentions', _("Extensions"))

		objprop_group.contents = app.objprop_plugins
		layout_group.contents = app.layout_plugins
		transform_group.contents = app.transform_plugins
		shaping_group.contents = app.shaping_plugins
		effects_group.contents = app.effects_plugins
		extentions_group.contents = app.extentions_plugins

		self.ptree.contents += [objprop_group, layout_group, transform_group,
							shaping_group, effects_group, extentions_group]



class PluginCategory:

	name = ''
	title = ''
	icon = 'strip_category'
	contents = []

	def __init__(self, name, title):
		self.name = name
		self.title = title


class PluginsTreeItem(TreeItem):

	"""The plugins tree browser """

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
			item = PluginsTreeItem(name, self.container)
			sublist.append(item)
		return sublist

	def addComment(self):
		pass

	def OnDoubleClick(self):
		if not self.IsExpandable():
			self.container.loadByName(self.objects.name)




