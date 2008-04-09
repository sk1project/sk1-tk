# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel
from Tkinter import LEFT, RIGHT, TOP, X

class TabsPanel:

	content=[]
	stub=1
	
	def __init__(self, parent, mainwindow):
		self.parent=parent
		self.mainwindow=mainwindow
		self.doc=self.mainwindow.document
		self.panel=TFrame(self.parent, name = 'tabsPanel', style='FlatFrame', borderwidth=0)
		self.stub_label=TLabel(self.panel, style='DrawingAreaTop', image='space_5')
		self.stub_label.pack(side = TOP, fill = X)

	def refresh(self):
		self.stub_label.foget()
		for item in self.content:
			item.forget()
			
		if len(self.content)<2:
			self.stub_label.pack(side = TOP, fill = X)
		else:			
			for item in self.content:
				item.pack(side = LEFT)			
