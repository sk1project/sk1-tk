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

class TrimPanel(PluginPanel):
	name='Trim'
	title = _("Trim")

	def init(self, master):
		PluginPanel.init(self, master)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)

		sign = TFrame(top, style='RoundedFrame', borderwidth=5)
		sign.pack(side = TOP)

		self.sign=TLabel(sign, image='shaping_trim')
		self.sign.pack(side=TOP)

		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_action,
								sensitivecb = self.is_correct_selection)
		button.pack(side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=1)
		button_frame.pack(side = BOTTOM, fill=X, pady=5)
				
		self.var_originals = IntVar(top)
		self.var_originals.set(0)
		
		self.autoupdate_check = TCheckbutton(button_frame, text = _("Leave originals"), 
											variable = self.var_originals)
		self.autoupdate_check.pack(side = LEFT, anchor=W, padx=10)

		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################
	def is_correct_selection(self):
		return (len(self.document.selection) > 1)
	
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
		for i in range(len(objects)-1):
			for j in range(i+1, len(objects)):
				objects[i] = self.minus([objects[i], objects[j]])
		if not self.var_originals.get():
			self.document.RemoveSelected()
		for i in range(len(objects)):
			self.document.Insert(objects[i])
		
	def minus(self, objects):
		assert len(objects) == 2
		new_paths, untouched_paths = base.intersect_objects(objects)
		buffer = []
		for i, paths in new_paths:
			if i == 0:
				container = objects[1]
				condition = 0
			else:
				container = objects[0]
				condition = 1
			for cp1, path, cp2 in paths:
				if base.contained(path, container) == condition:
					buffer.append((cp1, path, cp2))
		paths = base.join(buffer)
		for i, path in untouched_paths:
			if i == 0:
				container = objects[1]
				condition = 0
			else:
				container = objects[0]
				condition = 1
			if base.contained(path, container) == condition:
				paths.append(path)
		object = objects[0].Duplicate()
		object.SetPaths(paths)
		return object
		
instance=TrimPanel()
app.shaping_plugins.append(instance)


