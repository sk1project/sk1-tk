# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from math import pi

from Tkinter import LEFT, DoubleVar

from app import  _
from app.Graphics import ellipse
from app.conf.const import SELECTION, EDITED

from sk1sdk.libttk import tooltips
from sk1sdk.libttk import TLabel, TButton

from sk1.tkext import FlatFrame
from sk1.ttk_ext import TSpinbox

from subpanel import CtxSubPanel

degrees = pi / 180.0

class EllipsePanel(CtxSubPanel):

	name = 'EllipsePanel'

	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.start = DoubleVar(self.mw.root, 0)
		self.end = DoubleVar(self.mw.root, 0)
		self.builded = 0
		self.ReSubscribe()

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.update)
		self.doc.Subscribe(EDITED, self.update)

	def update(self, *arg):
		if not self.mw.canvas is None:
			self.build_dlg()

	def applyAngle(self, *arg):
		start = self.entry_start.get_value() * degrees
		end = self.entry_end.get_value() * degrees
		self.mw.document.CallObjectMethod(ellipse.Ellipse, _("Edit Object"),
								'SetAngles', start, end)

	def SwapAngle(self):
		start = self.entry_start.get_value()
		end = self.entry_end.get_value()
		self.entry_start.set_value(end)
		self.entry_end.set_value(start)
		self.applyAngle()

	def ResetAngle(self):
		self.entry_start.set_value(0)
		self.entry_end.set_value(0)
		self.applyAngle()

	def build_dlg(self):
		if not self.builded:
			cmds = self.mw.canvas.commands.Ellipse

			label = TLabel(self.panel, text=_("Start:"))
			label.pack(side=LEFT, padx=2)
			self.entry_start = TSpinbox(self.panel, var=0, vartype=1, textvariable=self.start,
							min=-360, max=360, step=5, width=6, command=self.applyAngle)
			self.entry_start.pack(side=LEFT, padx=2)
			tooltips.AddDescription(self.entry_start, _('Arc start point angle'))

			#--------------
			sep = FlatFrame(self.panel, width=5, height=2)
			sep.pack(side=LEFT)
			#--------------

			label = TLabel(self.panel, text=_("End:"))
			label.pack(side=LEFT, padx=2)
			self.entry_end = TSpinbox(self.panel, var=0, vartype=1, textvariable=self.end,
							min=-360, max=360, step=5, width=6, command=self.applyAngle)
			self.entry_end.pack(side=LEFT, padx=2)
			tooltips.AddDescription(self.entry_end, _('Arc end point angle'))

			b = TButton(self.panel, command=self.ResetAngle, style='Toolbutton', image='context_arc_reset')
			tooltips.AddDescription(b, _('Reset angles'))
			b.pack(side=LEFT)

			b = TButton(self.panel, command=self.SwapAngle, style='Toolbutton', image='context_arc_swap')
			tooltips.AddDescription(b, _('Swap angles'))
			b.pack(side=LEFT)

			b = TLabel(self.panel, image="toolbar_sep")
			b.pack(side=LEFT)

			b = TButton(self.panel, command=cmds.EllipseArc.Invoke, style='Toolbutton', image='context_arc')
			tooltips.AddDescription(b, _('to Arc'))
			b.pack(side=LEFT)

			b = TButton(self.panel, command=cmds.EllipseChord.Invoke, style='Toolbutton', image='context_chord')
			tooltips.AddDescription(b, _('to Chord'))
			b.pack(side=LEFT)

			b = TButton(self.panel, command=cmds.EllipsePieSlice.Invoke, style='Toolbutton', image='context_pie')
			tooltips.AddDescription(b, _('to Pie'))
			b.pack(side=LEFT)
			self.builded = 1
		else:
			obj = self.mw.document.CurrentObject()
			if obj and obj.is_Ellipse:
				start_angle = round(obj.start_angle / degrees, 2)
				end_angle = round(obj.end_angle / degrees, 2)
				self.entry_start.set_value(start_angle)
				self.entry_end.set_value(end_angle)
