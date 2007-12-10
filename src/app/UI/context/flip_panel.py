# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TButton
from Tkinter import LEFT
from subpanel import CtxSubPanel
from app import  _
from app.UI import tooltips

class FlipPanel(CtxSubPanel):
	
	name='FlipPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		
		b = TButton(self.panel, command=self.flip, style='Toolbutton', image='context_hflip')
		tooltips.AddDescription(b, 'Flip Horizontal')
		b.pack(side = LEFT)
		b = TButton(self.panel,  command=self.flop, style='Toolbutton', image='context_vflip')
		tooltips.AddDescription(b, 'Flip Vertical')
		b.pack(side = LEFT)
		
	def flip(self):
		self.parent.mainwindow.document.FlipSelected(1,0)
	
	def flop(self):
		self.parent.mainwindow.document.FlipSelected(0,1)
		
		