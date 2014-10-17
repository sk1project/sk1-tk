# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TLabel, TButton
from sk1.ttk_ext import TSpinbox
from app.conf.const import SELECTION
from Tkinter import LEFT, RIGHT, DoubleVar
from subpanel import CtxSubPanel
from app import  _
from sk1sdk.libttk import tooltips

class RotatePanel(CtxSubPanel):
	
	name='RotatePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.angle=DoubleVar(self.mw.root)
		self.angle.set(0)
		
		label = TLabel(self.panel, image='context_R')
		label.pack(side = LEFT)
		self.entry_width = TSpinbox(self.panel,  var=0, vartype=1, textvariable = self.angle,
						min = -360, max = 360, step = 1, width = 6, command = self.applyRotate)
		tooltips.AddDescription(self.entry_width, _('Rotation angle'))
		self.entry_width.pack(side = LEFT, padx=5)
		b = TButton(self.panel, command=self.rotLeft, style='Toolbutton', image='context_rotate_ccw')
		tooltips.AddDescription(b, _(u'Rotate -90°'))
		b.pack(side = LEFT)
		b = TButton(self.panel,  command=self.rot180, style='Toolbutton', image='context_rotate')
		tooltips.AddDescription(b, _(u'Rotate 180°'))
		b.pack(side = LEFT)
		b = TButton(self.panel,  command=self.rotRight, style='Toolbutton', image='context_rotate_cw')
		tooltips.AddDescription(b, _(u'Rotate 90°'))
		b.pack(side = LEFT)

	def rot180(self):
		self.rotation(180)
		
	def rotLeft(self):
		self.rotation(90)
		
	def rotRight(self):
		self.rotation(-90)
		
	def applyRotate(self, *arg):
		self.rotation(self.angle.get())
		
	def rotation(self, angle):
		if angle<0:
			if angle<-360:
				angle+=int(angle/360)*360
			angle+=360
		self.doc.RotateSelected(angle)