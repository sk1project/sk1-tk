# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel
from Tkinter import TOP, LEFT, RIGHT, BOTTOM, X, Y, BOTH, W, S, N, E, NORMAL, DISABLED, END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
from sk1.widgets.resframe import ResizableTFrame
import app

from pbrowser import PluginBrowser

class PluginContainer(ResizableTFrame):

	visible = 0
	loaded = []
	activated = []

	def __init__(self, master, root, mw, cnf={}, **kw):
		self.mw = mw
		self.root = root
		self.master = master
		ResizableTFrame.__init__(self, master, root, size=240, orient=LEFT,
								min=240, max=400)

		b = TLabel(self.panel, style='HLine')
		b.pack(side=BOTTOM, fill=X)

		self.pbrowser = PluginBrowser()

		self.plugins = app.objprop_plugins + app.layout_plugins
		self.plugins += app.transform_plugins + app.extentions_plugins
		self.plugins += app.effects_plugins + app.shaping_plugins
		self.plugins += [self.pbrowser]

	def showHide(self):
		if not self.visible:
			self.visible = 1
			self.pack(side=RIGHT, fill=Y)
			if not self.loaded:
				self.loadByName('PluginBrowser')
		else:
			self.visible = 0
			self.forget()
			self.master['width'] = 1

	def loadByName(self, name):
		plugin = None
		for item in self.plugins:
			if item.name == name:
				plugin = item
		if plugin is not None:
			if plugin.activated:
				if not plugin.packed:
					plugin.restore_panel()
				if plugin.collapsed:
					plugin.decollapse_panel()
			else:
				plugin.init(self.panel)
			if not plugin in self.loaded:
				self.loaded.append(plugin)

	def remove_plugin(self, plugin):
		self.loaded.remove(plugin)
		if not self.loaded: self.showHide()
