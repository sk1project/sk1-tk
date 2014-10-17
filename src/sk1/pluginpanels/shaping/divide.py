# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCheckbutton, TButton
from Tkinter import IntVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect, mw
from app.conf import const
import app
from sk1.tkext import UpdatedButton

from sk1.pluginpanels.ppanel import PluginPanel

import base

class DividePanel(PluginPanel):
	name='Divide'
	title = _("Divide")

	def init(self, master):
		PluginPanel.init(self, master)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)
		
		sign = TFrame(top, style='RoundedFrame', borderwidth=5)
		sign.pack(side = TOP)

		self.sign=TLabel(sign, image='shaping_divide')
		self.sign.pack(side=TOP)

		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_action,
								sensitivecb = self.is_correct_selection)
		button.pack(side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=1)
		button_frame.pack(side = BOTTOM, fill=X, pady=5)
				
		self.var_originals = IntVar(top)
		self.var_originals.set(1)
		
		self.autoupdate_check = TCheckbutton(button_frame, text = _("Leave originals"), 
											variable = self.var_originals)
		self.autoupdate_check.pack(side = LEFT, anchor=W, padx=10)

		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################
	def is_correct_selection(self):
		return (len(self.document.selection) == 2)
	
	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.init_from_doc)	
		self.document.Subscribe(EDITED, self.init_from_doc)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.init_from_doc)	
		self.document.Unsubscribe(EDITED, self.init_from_doc)

	def init_from_doc(self, *arg):
		self.issue(SELECTION)

	def apply_action(self):
		objects = base.get_selection(self.mw)
		if not objects:
			return
		objects[0:2] = self.divide(objects[0], objects[1])
		if not self.var_originals.get():
			self.document.RemoveSelected()
		for object in objects:
			self.document.Insert(object)
		
	def divide(self, object1, object2):
		buffer = []
		new_paths, untouched_paths = base.intersect_objects([object1, object2])
		if new_paths:
			common = []
			parts = ([], [])
			for i, paths in new_paths:
				if i == 0:
					container = object2
					parts2, parts1 = parts
				else:
					container = object1
					parts1, parts2 = parts
				for cp1, path, cp2 in paths:
					if base.contained(path, container):
						common.append((cp1, path, cp2))
						parts2.append((cp1, path, cp2))
					else:						 
						parts1.append((cp1, path, cp2))
			for path in base.join(parts1):
				object = object1.Duplicate()
				object.SetPaths([path])
				buffer.append(object)
			for path in base.join(parts2):
				object = object2.Duplicate()
				object.SetPaths([path])
				buffer.append(object)
			for path in base.join(common):
				object = object2.Duplicate()
				object.SetPaths([path])
				buffer.append(object)
			for i, path in untouched_paths:
				if i == 0:
					object = object1.Duplicate()
				else:
					object = object2.Duplicate()
				object.SetPaths([path])
				buffer.append(object)
		else:
			buffer.append(object1.Duplicate())
			buffer.append(object2.Duplicate())
		return buffer
		
instance=DividePanel()
app.shaping_plugins.append(instance)

