# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TButton
from Tkinter import LEFT
from subpanel import CtxSubPanel
from app import  _
from sk1sdk.libttk import tooltips

class FlipPanel(CtxSubPanel):
	
	name='FlipPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		
		b = TButton(self.panel, command=self.flip, style='Toolbutton', image='context_hflip')
		tooltips.AddDescription(b, _('Flip Horizontal'))
		b.pack(side = LEFT)
		b = TButton(self.panel,  command=self.flop, style='Toolbutton', image='context_vflip')
		tooltips.AddDescription(b, _('Flip Vertical'))
		b.pack(side = LEFT)
		
	def flip(self):
		self.doc.FlipSelected(1,0)
	
	def flop(self):
		self.doc.FlipSelected(0,1)
		
		