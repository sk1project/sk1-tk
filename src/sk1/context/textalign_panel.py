# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.conf.const import SELECTION, CHANGED, EDITED
from app.conf import const
from Tkinter import LEFT, StringVar
from subpanel import CtxSubPanel
from app import  _, config
from sk1.tkext import UpdatedRadiobutton
from sk1sdk.libttk import tooltips
from app.Graphics import text

class TextAlignPanel(CtxSubPanel):
	
	name='TextAlignPanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.var_reference = StringVar(self.mw.root,'left')
		self.var_stub = StringVar(self.mw.root)
			
		radio = UpdatedRadiobutton(self.panel, value='left', image='context_text_left', 
								command=self.applyProperties, variable=self.var_reference, style='ToolbarRadiobutton')
		radio.pack(side=LEFT)
		tooltips.AddDescription(radio, _('Left alignment'))
		radio = UpdatedRadiobutton(self.panel, value = 'center', image='context_text_center', 
								command=self.applyProperties, variable = self.var_reference, style='ToolbarRadiobutton')
		radio.pack(side=LEFT)
		tooltips.AddDescription(radio, _('Center alignment'))
		radio = UpdatedRadiobutton(self.panel, value = 'right', image='context_text_right', 
								command=self.applyProperties, variable = self.var_reference, style='ToolbarRadiobutton')
		radio.pack(side=LEFT)
		tooltips.AddDescription(radio, _('Right alignment'))
#		radio = UpdatedRadiobutton(self.panel, value = 'justify', image='context_text_justify_disabled', 
#								command=self.applyProperties, variable = self.var_stub, style='ToolbarRadiobutton', state='disabled')
#		radio.pack(side=LEFT)
#		tooltips.AddDescription(radio, _('Justify'))
						
		self.ReSubscribe()

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.Update)	
		self.doc.Subscribe(EDITED, self.Update)
						
	def applyProperties(self, *arg):
		a=self.var_reference.get()
		if a=='left':
			align=const.ALIGN_LEFT
		if a=='center': 
			align=const.ALIGN_CENTER
		if a=='right': 
			align=const.ALIGN_RIGHT		
		self.mw.document.CallObjectMethod(text.CommonText, _("Set Text Alignment"),
											'SetAlign', align, 0)
	
	def Update(self, *arg):
		obj=self.mw.document.CurrentObject()		
		if obj and obj.is_Text:
			align=obj.properties.align
			if align==const.ALIGN_LEFT: 
				self.var_reference.set('left')
			if align==const.ALIGN_CENTER: 
				self.var_reference.set('center')
			if align==const.ALIGN_RIGHT: 
				self.var_reference.set('right')			
			
			
			
			
			
			