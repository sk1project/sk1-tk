# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TFrame, TLabel
from Tkinter import LEFT, RIGHT

class CtxSubPanel:
	
	def __init__(self, parent):
		self.parent=parent
		self.panel=TFrame(parent.panel, style='FlatFrame', borderwidth=0)
		self.separator = TLabel(self.panel, image = "toolbar_sep")
		self.setNormal()
		
	def setLast(self):
		self.separator.forget()
		
	def setNormal(self):
		self.separator.pack(side = RIGHT)