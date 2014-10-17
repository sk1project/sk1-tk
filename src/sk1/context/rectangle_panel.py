# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from math import hypot

from Tkinter import LEFT, DoubleVar

from app import  _
from app.Graphics import rectangle
from app.conf.const import SELECTION, EDITED

from sk1sdk.libttk import TLabel
from sk1sdk.libttk import tooltips

from sk1.ttk_ext import TSpinbox
from sk1.tkext import FlatFrame

from subpanel import CtxSubPanel

class RectanglePanel(CtxSubPanel):

	name = 'RectanglePanel'

	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.radius1 = DoubleVar(self.mw.root, 0)
		self.radius2 = DoubleVar(self.mw.root, 0)
		label = TLabel(self.panel, image='context_rect_rx')
		label.pack(side=LEFT, padx=2)
		self.entry_radius1 = TSpinbox(self.panel, var=0, vartype=1, textvariable=self.radius1,
						min=0, max=100, step=1, width=6, command=self.applyRadius1)
		self.entry_radius1.pack(side=LEFT, padx=2)
		tooltips.AddDescription(self.entry_radius1, _('Horizontal radius of rounded corners'))

		#--------------
		sep = FlatFrame(self.panel, width=4, height=2)
		sep.pack(side=LEFT)
		#--------------

		label = TLabel(self.panel, image='context_rect_ry')
		label.pack(side=LEFT, padx=2)
		self.entry_radius2 = TSpinbox(self.panel, var=0, vartype=1, textvariable=self.radius2,
						min=0, max=100, step=1, width=6, command=self.applyRadius1)
		self.entry_radius2.pack(side=LEFT, padx=2)
		tooltips.AddDescription(self.entry_radius2, _('Vertical radius of rounded corners'))

		self.ReSubscribe()

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.Update)
		self.doc.Subscribe(EDITED, self.Update)

	def Update(self, *arg):
		obj = self.mw.document.CurrentObject()
		if obj and obj.is_Rectangle:
			self.entry_radius1.set_value(round(obj.radius1 * 200., 2))
			self.entry_radius2.set_value(round(obj.radius2 * 200., 2))

	def applyRadius1(self, *arg):
		trafo = self.mw.document.CurrentObject().trafo
		w = hypot(trafo.m11, trafo.m21)
		h = hypot(trafo.m12, trafo.m22)
		#print w, h
		radius1 = self.entry_radius1.get_value() / 200.
		radius2 = self.entry_radius2.get_value() / 200.

		if radius2 == 0:
			radius2 = min(w / h * radius1, 0.5)

		if radius1 == 0:
			radius1 = min(h / w * radius2, 0.5)

		self.mw.document.CallObjectMethod(rectangle.Rectangle, _("Edit Object"),
								'SetTrafoAndRadii', trafo, radius1, radius2)


