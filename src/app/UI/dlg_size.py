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

from app import _, config, Rect
from app.conf import const
import skpixmaps
pixmaps = skpixmaps.PixmapTk

from canvas import SketchCanvas
from math import floor, ceil

class SizePanel(PropertyPanel):

	title = _("SIZE")
	def __init__(self, master, main_window, doc):
		PropertyPanel.__init__(self, master, main_window, doc,
								name = 'sizedlg')

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

		self.var_width=DoubleVar(top)
		self.var_height=DoubleVar(top)
		self.var_width.set(0)
		self.var_height.set(0)

		self.entry_width = Spinbox(steps_frame, name = 'width', width = 7,
								textvariable = self.var_width, background = '#FFFFFF', 
								selectbackground = '#21449C', selectforeground = '#FFFFFF', 
								selectborderwidth=0, to=10000, increment = 1.0)
								
		self.entry_width.pack(side = LEFT, anchor = E)

		steps_frame = Frame(top, relief = 'flat', bd = 3)
		steps_frame.pack(side = TOP)
		label = Label(steps_frame, text = _("  V (mm): "))
		label.pack(side = LEFT, anchor = E)
		
		self.entry_height = Spinbox(steps_frame, name = 'height', width = 7,
								textvariable = self.var_height, background = '#FFFFFF', 
								selectbackground = '#21449C', selectforeground = '#FFFFFF', 
								selectborderwidth=0, to=10000, increment = 1.0)

								
		self.entry_height.pack(side = LEFT, anchor = E)


		button_frame = Frame(top)
		button_frame.pack(side = BOTTOM, fill = BOTH)

		self.update_buttons = []
		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_resize,
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
		try:
				br=self.main_window.canvas.SelectionSizeData()
				hor_sel=ceil(floor(10**3*(br.right - br.left)/2.83465)/10)/100
				ver_sel=ceil(floor(10**3*(br.top - br.bottom)/2.83465)/10)/100
				self.var_width.set(hor_sel)
				self.var_height.set(ver_sel)
		except:
				self.var_width.set(0)
				self.var_height.set(0)


	def apply_resize(self):
		try:
			x=self.var_width.get()
			y=self.var_height.get()
			br=self.main_window.canvas.SelectionSizeData()
			hor_sel=ceil(floor(10**3*(br.right - br.left)/2.83465)/10)/100
			ver_sel=ceil(floor(10**3*(br.top - br.bottom)/2.83465)/10)/100
		except:
			return

		self.document.ScaleSelected(x/hor_sel, y/ver_sel)


	def apply_to_copy(self):
		try:
			x=self.var_width.get()
			y=self.var_height.get()
			br=self.main_window.canvas.SelectionSizeData()
			hor_sel=ceil(floor(10**3*(br.right - br.left)/2.83465)/10)/100
			ver_sel=ceil(floor(10**3*(br.top - br.bottom)/2.83465)/10)/100
		except:
			return

		self.document.ApplyToDuplicate()
		self.document.ScaleSelected(x/hor_sel, y/ver_sel)


