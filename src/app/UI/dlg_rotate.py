# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import sketchdlg
from Tkinter import Frame, Label, DoubleVar, Spinbox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, GROOVE, E,\
		DISABLED, NORMAL
from tkext import UpdatedButton


from sketchdlg import PropertyPanel
from app.conf.const import SELECTION

from app.Graphics.blendgroup import BlendGroup, BlendInterpolation, \
		SelectStart, SelectEnd

from app import _, config
from app.conf import const



class RotatePanel(PropertyPanel):

	title = _("ROTATE")
	def __init__(self, master, main_window, doc):
		PropertyPanel.__init__(self, master, main_window, doc,
								name = 'rotatedlg')

	def build_dlg(self):
		top = self.top
		
		format_label = Label(top, image = 'messagebox_construct', borderwidth=6)
		format_label.pack(side = TOP)


		steps_frame = Frame(top, relief = 'flat', bd = 3)
		steps_frame.pack(side = TOP)
		label = Label(steps_frame, text = _(" Angle: "))
		label.pack(side = LEFT, anchor = E)
		self.var_rot=DoubleVar(top)
		self.var_rot.set(0)

		self.entry_width = Spinbox(steps_frame, name = 'width', width = 5,
								textvariable = self.var_rot, background = '#FFFFFF', 
								selectbackground = '#21449C', selectforeground = '#FFFFFF', 
								selectborderwidth=0, to=10000, increment = 1.0)

		self.entry_width['from'] = -10000
		self.entry_width.pack(side = LEFT, anchor = E)

		button_frame = Frame(top)
		button_frame.pack(side = BOTTOM, fill = BOTH)

		self.update_buttons = []
		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_rotate,
								sensitivecb = self.doc_can_rotate)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)

		button = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy,
								sensitivecb = self.doc_can_rotate)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)

		sep_frame = Frame(top, height=15)
		sep_frame.pack(side = BOTTOM, fill = X)

		top.resizable (width=0, height=0)
###############################################################################
	def doc_can_rotate(self):
		return (len(self.document.selection) > 0)


	def init_from_doc(self):
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


