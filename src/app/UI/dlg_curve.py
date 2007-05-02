# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import sketchdlg
from Tkinter import Frame, Label
from Tkinter import BOTTOM, X, BOTH, TOP, CENTER
from tkext import UpdatedButton, CommandButton

from app import _

from sketchdlg import CommandPanel


class CurvePanel(CommandPanel):

	title = _("Curve")

	def __init__(self, master, main_window, doc):
		CommandPanel.__init__(self, master, main_window, doc,
								name = 'curvedlg')

	def build_dlg(self):
		names = (('ContAngle', 'CloseNodes', 'OpenNodes'),
					('ContSmooth', 'InsertNodes', 'DeleteNodes'),
					('ContSymmetrical', 'SegmentsToLines', 'SegmentsToCurve'))

		top = self.top
		
		
		format_label = Label(top, image = 'messagebox_construct', borderwidth=6)
		format_label.pack(side = TOP)
		
		frame = Frame(top)
		frame.pack(side = TOP, expand = 1, fill = BOTH)

		# XXX This dialog should have its own ObjectCommand objects
		cmds = self.main_window.canvas.commands.PolyBezierEditor
		for i in range(len(names)):
			for j in range(len(names[i])):
				button = CommandButton(frame, getattr(cmds, names[i][j]),
										highlightthickness = 0)
				button.grid(column = j, row = i)

		frame = Frame(top)
		frame.pack(side = BOTTOM, expand = 0, fill = X)

		button = UpdatedButton(frame, text = _("Close"),
								command = self.close_dlg)
		button.pack(anchor = CENTER)


