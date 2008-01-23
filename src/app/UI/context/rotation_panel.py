# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TLabel, TButton
from app.UI.ttk_ext import TSpinbox
from app.conf.const import SELECTION
from Tkinter import LEFT, RIGHT, DoubleVar
from subpanel import CtxSubPanel
from app import  _
from app.UI import tooltips

class RotatePanel(CtxSubPanel):
	
	name='RotatePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.angle=DoubleVar(self.mw.root)
		self.angle.set(0)
		
		label = TLabel(self.panel, text=_(" Rotate: "))
		label.pack(side = LEFT)
		self.entry_width = TSpinbox(self.panel,  var=0, vartype=1, textvariable = self.angle,
						min = -360, max = 360, step = 1, width = 6, command = self.applyRotate)
		self.entry_width.pack(side = LEFT)
		b = TButton(self.panel, command=self.rotLeft, style='Toolbutton', image='context_rotate_ccw')
		tooltips.AddDescription(b, 'Rotate -90°')
		b.pack(side = LEFT)
		b = TButton(self.panel,  command=self.rot180, style='Toolbutton', image='context_rotate')
		tooltips.AddDescription(b, 'Rotate 180°')
		b.pack(side = LEFT)
		b = TButton(self.panel,  command=self.rotRight, style='Toolbutton', image='context_rotate_cw')
		tooltips.AddDescription(b, 'Rotate 90°')
		b.pack(side = LEFT)

	def rot180(self):
		self.rotation(180)
		
	def rotLeft(self):
		self.rotation(90)
		
	def rotRight(self):
		self.rotation(-90)
		
	def applyRotate(self, event):
		self.rotation(self.angle.get())
		
	def rotation(self, angle):
		self.doc.RotateSelected(angle)