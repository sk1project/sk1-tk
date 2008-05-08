# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TFrame, TLabel
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
import app
from ppanel import PluginPanel

class TestPlugin(PluginPanel):
	
	name='Test Panel'
	category='Test'
	
	def init(self, master):
		PluginPanel.init(self, master)
		label=TLabel(self.top, style='FlatLabel',text='PROBA')
		label.pack()
		
instance=TestPlugin()
app.ppdict[instance.name]=instance
