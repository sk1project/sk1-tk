# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from sk1.tkext import ToolbarButton
from app.conf.const import CHANGED
from Tkinter import LEFT, DoubleVar, StringVar, RIGHT
from subpanel import CtxSubPanel
from app import  _, config, PolyBezier, CreatePath, Point
from sk1sdk.libttk import tooltips
from sk1.widgets.lengthvar import LengthVar
from app.conf.const import SELECTION

class ImagePanel(CtxSubPanel):
	
	name='ImagePanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.builded=0
		self.ReSubscribe()
		
	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.update)
		
	def build_dlg(self):
		if not self.builded:
			cmds = self.mw.commands		
			
			b = ToolbarButton(self.panel, command=cmds.Convert_to_CMYK, style='Toolbutton', image='context_image_cmyk')
			tooltips.AddDescription(b, _('Convert to CMYK'))
			b.pack(side = LEFT)
			
			b = ToolbarButton(self.panel, command=cmds.Convert_to_RGB, style='Toolbutton', image='context_image_rgb')
			tooltips.AddDescription(b, _('Convert to RGB'))
			b.pack(side = LEFT)			
			
			b = ToolbarButton(self.panel, command=cmds.Convert_to_Grayscale, style='Toolbutton', image='context_image_gray')
			tooltips.AddDescription(b, _('Convert to Grayscale'))
			b.pack(side = LEFT)
			
			b = ToolbarButton(self.panel, command=cmds.Convert_to_BW, style='Toolbutton', image='context_image_bw')
			tooltips.AddDescription(b, _('Convert to B&W'))
			b.pack(side = LEFT)					

			self.builded=1
		
	def update(self,*arg):
		if not self.mw.canvas is None:
			self.build_dlg()


