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


class MovePanel(PropertyPanel):

	title = _("MOVE")
	def __init__(self, master, main_window, doc):
		PropertyPanel.__init__(self, master, main_window, doc,
								name = 'movedlg')

	def build_dlg(self):
		top = self.top

		
		format_label = Label(top, image = 'messagebox_construct', borderwidth=6)
		format_label.pack(side = TOP)

		sep_frame = Frame(top, relief = 'sunken', height= 5)
		sep_frame.pack(side = TOP, fill=X)

		steps_frame = Frame(top, relief = 'flat', bd = 3)
		steps_frame.pack(side = TOP)
		label = Label(steps_frame, text = _("  H (mm): "))
		label.pack(side = LEFT, anchor = E)
		self.var_width = DoubleVar(top)
		self.var_height = DoubleVar(top)
		self.var_width.set(0)
		self.var_height.set(0)

		self.entry_width = Spinbox(steps_frame, name = 'width', width = 5,
								textvariable = self.var_width, background = '#FFFFFF', 
								selectbackground = '#21449C', selectforeground = '#FFFFFF',
								selectborderwidth=0, to=10000, increment = .1)
								
		self.entry_width['from'] = -10000		     
		self.entry_width.pack(side = LEFT, anchor = E)


		steps_frame = Frame(top, relief = 'flat', bd = 3)
		steps_frame.pack(side = TOP)
		label = Label(steps_frame, text = _("  V (mm): "))
		label.pack(side = LEFT, anchor = E)
		
		self.entry_height = Spinbox(steps_frame, name = 'height', width = 5,
								textvariable = self.var_height, background = '#FFFFFF', 
								selectbackground = '#21449C', selectborderwidth=0,
								to=10000, increment = .1)
		self.entry_height['from'] = -10000
		self.entry_height.pack(side = LEFT, anchor = E)


		button_frame = Frame(top)
		button_frame.pack(side = BOTTOM, fill = BOTH)

		self.update_buttons = []
		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_move, 
								sensitivecb = self.doc_can_move)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)

		button = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy,
								sensitivecb = self.doc_can_move)
		button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)

		sep_frame = Frame(top, height=10)
		sep_frame.pack(side = BOTTOM, fill = X)

		top.resizable (width=0, height=0)
###############################################################################
	def doc_can_move(self):
		return (len(self.document.selection) > 0)


	def init_from_doc(self):
		self.Update()
		self.issue(SELECTION)

	def Update(self):
		pass
		
	def apply_move(self):
		try:
				x=self.var_width.get()
		except:
				self.var_width.set(0)
		try:
				x=self.var_height.get()
		except:
				self.var_height.set(0)

		x=self.var_width.get()
		y=self.var_height.get()
		self.document.MoveSelected(x, y)


	def apply_to_copy(self):
		try:
				x = self.var_width.get()
		except:
				self.var_width.set(0)
				x = 0
		try:
				y = self.var_height.get()
		except:
				self.var_height.set(0)
				y = 0
				
		self.document.ApplyToDuplicate()
		self.document.MoveSelected(x, y)


