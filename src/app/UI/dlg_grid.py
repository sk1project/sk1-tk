# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998 by Bernhard Herzog 
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
#	Dialog for grid settings
#

from Tkinter import Frame, Label
from Ttk import LabelFrame, TFrame, TLabel
from Tkinter import RIGHT, BOTTOM, BOTH, TOP, X, E, LEFT

from app.conf.const import GRID
from app.conf import const
from app import _

from sketchdlg import SketchPanel
from lengthvar import create_length_entry


class GridPanel(SketchPanel):

	title = _("GRID")
	receivers = SketchPanel.receivers[:]

	def __init__(self, master, canvas, doc):
		SketchPanel.__init__(self, master, canvas, doc)

	def build_dlg(self):
		top = self.top

		grid_top = TFrame(top, borderwidth=2, style='FlatFrame')
		grid_top.pack(side = TOP, expand = 1, fill = X)

		button_frame = self.create_std_buttons(top)
		button_frame.pack(side = BOTTOM, fill = BOTH, expand = 1)
# ===========================================================
		do_apply = self.do_apply

		frame=LabelFrame(top, text='Grid origin', borderwidth=2, relief='groove', pady=4, padx=4)
		
		frame.pack(side = TOP, fill=X, pady=4, padx=2)
		
		f = TFrame(frame, style='FlatFrame')	
		self.var_xorig = create_length_entry(top, f, do_apply)
		label = TLabel(f, text = "X: ", anchor = E)
		label.pack(side = RIGHT, fill=X)		
		f.pack(side = TOP, fill=X, pady=2)
	
			
		f = TFrame(frame, style='FlatFrame')
		self.var_yorig = create_length_entry(top, f, do_apply)
		label = TLabel(f, text = "Y: ", anchor = E)
		label.pack(side = RIGHT, fill=X)		
		f.pack(side = TOP, fill=X, pady=2)

# ===========================================================

		frame=LabelFrame(top, text='Grid size', borderwidth=2, relief='groove', pady=4, padx=4)
		frame.pack(side = TOP, fill=X, pady=4, padx=2)

		f = TFrame(frame, style='FlatFrame')	
		self.var_xwidth = create_length_entry(top, f, do_apply)
		label = TLabel(f, text = "ΔX: ", anchor = E)
		label.pack(side = RIGHT, fill=X)	
		f.pack(side = TOP, fill=X, pady=2)
		
		
		f = TFrame(frame, style='FlatFrame')
		self.var_ywidth = create_length_entry(top, f, do_apply)
		label = TLabel(f, text = "ΔY: ")
		label.pack(side = RIGHT, fill=X)
		f.pack(side = TOP, fill=X, pady=2)
		
		top.resizable (width=0, height=0)
		
	def init_from_doc(self):
		xorig, yorig, xwidth, ywidth = self.document.Grid().Geometry()
		self.var_xorig.set(xorig)
		self.var_yorig.set(yorig)
		self.var_xwidth.set(xwidth)
		self.var_ywidth.set(ywidth)

	receivers.append((GRID, 'init_from_doc'))

	def do_apply(self, *rest):
		self.document.SetGridGeometry((self.var_xorig.get(),
								self.var_yorig.get(),
								self.var_xwidth.get(),
								self.var_ywidth.get()))


