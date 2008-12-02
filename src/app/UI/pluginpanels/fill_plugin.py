# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TCheckbutton
from Tkinter import IntVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL
from app.UI.widgets.unicolorsel import UniColorSelector
from app.UI.widgets.unicolorchooser import UniColorChooser

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect
from app.conf import const
import app
from app.UI.tkext import UpdatedButton

from ppanel import PluginPanel

from math import floor, ceil

class FillPanel(PluginPanel):
	name='Fill'
	title = _("Fill")


	def init(self, master):
		PluginPanel.init(self, master)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)

		self.selector=UniColorSelector(top)
		self.selector.pack(side=TOP, expand = 1, fill=X)
		
		self.picker=UniColorChooser(top)
		self.picker.pack(side=TOP, expand = 1, fill=X)		


		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_pattern,
								sensitivecb = self.is_selection)
		button.pack(side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)
		
		button = UpdatedButton(top, text = _("Copy From..."),
								command = self.copy_from,
								sensitivecb = self.is_selection)
		button.pack(side = BOTTOM, expand = 1, fill = X, pady=5)
		self.Subscribe(SELECTION, button.Update)
		
		self.var_autoupdate = IntVar(top)
		self.var_autoupdate.set(1)
		
		self.autoupdate_check = TCheckbutton(top, text = _("Auto Update"), 
												variable = self.var_autoupdate)
		self.autoupdate_check.pack(side = BOTTOM, anchor=W, padx=5, pady=5)
				
		self.document.Subscribe(SELECTION, self.init_from_doc)	
		self.document.Subscribe(EDITED, self.init_from_doc)
		self.init_from_doc()

###############################################################################
	def is_selection(self):
		return (len(self.document.selection) > 0)


	def init_from_doc(self, *arg):
		self.Update()
		self.issue(SELECTION)

	def Update(self):
		pass


	def apply_pattern(self):
		pass


	def copy_from(self):
		pass

instance=FillPanel()
app.objprop_plugins.append(instance)
