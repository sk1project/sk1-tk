# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TButton, TLabel
from sk1.ttk_ext import TSpinbox
from app.conf.const import SELECTION, CHANGED, EDITED
from Tkinter import LEFT, RIGHT, DoubleVar, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from math import floor, ceil
from sk1.widgets.lengthvar import LengthVar
from app.Graphics import text
from sk1sdk.libttk import tooltips

class TextPropPanel(CtxSubPanel):
	
	name='TextPropPanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.my_changes=0
		self.text_linegap=StringVar(self.mw.root,'100.0')
		self.text_wordgap=StringVar(self.mw.root,'100.0')
		self.text_chargap=StringVar(self.mw.root,'100.0')

		
		label = TLabel(self.panel, image='context_between_word')
		label.pack(side = LEFT)
		tooltips.AddDescription(label, _('Distance between words'))
		self.entry_word = TSpinbox(self.panel, var=100.0, vartype=1, textvariable = self.text_wordgap,
						min = 0, max = 5000, step = 10, width = 6, command = self.applyProperties)
		self.entry_word.pack(side = LEFT, padx=2)

		label = TLabel(self.panel, text='% ')
		label.pack(side = LEFT)
		label = TLabel(self.panel, image='context_between_line')
		label.pack(side = LEFT)
		tooltips.AddDescription(label, _('Distance between lines'))
		self.entry_line = TSpinbox(self.panel, var=100.0, vartype=1, textvariable = self.text_linegap,
						min = 0, max = 5000, step = 10, width = 6, command = self.applyProperties)
		self.entry_line.pack(side = LEFT, padx=2)

		label = TLabel(self.panel, text='% ')
		label.pack(side = LEFT)	
		label = TLabel(self.panel, image='context_between_char')
		label.pack(side = LEFT)
		tooltips.AddDescription(label, _('Distance between characters'))
		self.entry_char = TSpinbox(self.panel, var=100.0, vartype=1, textvariable = self.text_chargap,
						min = 0, max = 5000, step = 10, width = 6, command = self.applyProperties)
		self.entry_char.pack(side = LEFT, padx=2)
		label = TLabel(self.panel, text='% ')
		label.pack(side = LEFT)	
				
		self.ReSubscribe()

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.Update)	
		self.doc.Subscribe(EDITED, self.Update)
						
	def applyProperties(self, *arg):
		char=self.entry_char.get_value()/100
		word=self.entry_word.get_value()/100
		line=self.entry_line.get_value()/100		
		self.mw.document.CallObjectMethod(text.CommonText, _("Set Text properties"),
											'SetGap', char, word, line)
	
	def Update(self, *arg):
		obj=self.mw.document.CurrentObject()		
		if obj and obj.is_Text:
			self.entry_word.set_value(obj.properties.wordgap*100)
			self.entry_line.set_value(obj.properties.linegap*100)
			self.entry_char.set_value(obj.properties.chargap*100)
			