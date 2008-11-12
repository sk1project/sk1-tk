# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TCombobox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP,W, E, DISABLED, NORMAL, StringVar
from app import _


class UniColorChooser(TFrame):
	
	def __init__(self, parent, color=None, **kw):
		self.refcolor=color
		self.color=color
		TFrame.__init__(self, parent, style='FlatFrame', **kw)

