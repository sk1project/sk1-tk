# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TButton
from Tkinter import TOP
from subpanel import CtxSubPanel
from app import  _
from app.UI import tooltips

class FlipPanel(CtxSubPanel):
	
	name='FlipPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		
		b = TButton(self.panel, command=self.flip, style='TSmallbutton', image='context_flip')
		tooltips.AddDescription(b, 'Flip Horizontal')
		b.pack(side = TOP)
		b = TButton(self.panel,  command=self.flop, style='TSmallbutton', image='context_flop')
		tooltips.AddDescription(b, 'Flip Vertical')
		b.pack(side = TOP)
		
	def flip(self):
		self.parent.mainwindow.document.FlipSelected(1,0)
	
	def flop(self):
		self.parent.mainwindow.document.FlipSelected(0,1)
		
		