# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel
from Tkinter import DoubleVar, Spinbox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, GROOVE, E, DISABLED, NORMAL
from app.UI.tkext import UpdatedButton
from app.UI.ttk_ext import TSpinbox

from app.conf.const import SELECTION, EDITED

from ppanel import PluginPanel

from app import _, config
from app.conf import const
import app



class RotatePanel(PluginPanel):
	name='Rotate'
	title = _("Rotate")


	def init(self, master):
		PluginPanel.init(self, master)
		
		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)

		steps_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		steps_frame.pack(side = TOP)
		label = TLabel(steps_frame, style='FlatLabel', text = _(" Angle: "))
		label.pack(side = LEFT, anchor = E)
		self.var_rot=DoubleVar(top)
		self.var_rot.set(0)

		
		self.entry_width = TSpinbox(steps_frame,  var=0, vartype=1, textvariable = self.var_rot, 
									min = -5000, max = 5000, step = .1, width = 6)
		self.entry_width.pack(side = LEFT, anchor = E)

		button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		button_frame.pack(side = BOTTOM, fill = BOTH)

		self.update_buttons = []
		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_rotate,
								sensitivecb = self.doc_can_rotate)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X, pady=3)
		self.Subscribe(SELECTION, button.Update)

		button = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy,
								sensitivecb = self.doc_can_rotate)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)
		
		self.document.Subscribe(SELECTION, self.init_from_doc)	
		self.document.Subscribe(EDITED, self.init_from_doc)
		self.init_from_doc()

###############################################################################
	def doc_can_rotate(self):
		return (len(self.document.selection) > 0)


	def init_from_doc(self, *arg):
		self.Update()
		self.issue(SELECTION)

	def Update(self):
		pass

#	if self.document.selection:
#		self.var_width.set(self.entry_width)
#		self.var_height.set(self.entry_height)

	def apply_rotate(self):
		try:
			x=self.var_rot.get()
		except:
				self.var_rot.set(0)

		x=self.var_rot.get()
		self.document.RotateSelected(x)


	def apply_to_copy(self):
		try:
			x=self.var_rot.get()
		except:
				self.var_rot.set(0)

		x=self.var_rot.get()
		self.document.ApplyToDuplicate()
		self.document.RotateSelected(x)

instance=RotatePanel()
app.transform_plugins.append(instance)
