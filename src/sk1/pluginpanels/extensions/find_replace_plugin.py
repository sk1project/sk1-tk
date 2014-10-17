# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
# Copyright (C) 2008 by Darya Shumilina
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import re

from sk1.pluginpanels.ppanel import PluginPanel

from app import _
import app
from app.Graphics import document, text

from sk1sdk.libttk import TLabelframe, TFrame, TLabel, TCheckbutton, TButton
from sk1.ttk_ext import TEntryExt
from Tkinter import RIGHT, BOTTOM, BOTH, TOP, X, E, W, Y, LEFT, StringVar, BooleanVar, DISABLED, NORMAL

from sk1.widgets.lengthvar import create_length_entry

class FindReplacePanel(PluginPanel):
	name='Text Find & Replace'
	title = _("Text Find & Replace")
	
	def init(self, master):
		PluginPanel.init(self, master)
		top = self.panel

		top = TFrame(top, borderwidth=2, style='FlatFrame')
		top.pack(side = TOP, expand = 1, fill = X)

		button_frame = TFrame(top, borderwidth=2, style='FlatFrame')
		button_frame.pack(side = BOTTOM, fill = BOTH, expand = 1)
		
		button=TButton(button_frame,text=_('Apply'), command=self.replace)
		button.pack(side = TOP)
		
		#----------------------------------------------------------
		main_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		main_frame.pack(side = TOP, fill=X)

		self.find_var = StringVar(top);
		self.find_var.set('')
		findField = TEntryExt(main_frame, textvariable=self.find_var)
		findField.pack(side = RIGHT)
			   
		label = TLabel(main_frame, style='FlatLabel', text = _("Find:")+" ")
		label.pack(side = RIGHT, anchor = E)
		#---------------------------------------------------------
		main_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		main_frame.pack(side = TOP, fill=X)


		self.replace_var = StringVar(top);
		self.replace_var.set('')
		replaceField = TEntryExt(main_frame, textvariable=self.replace_var)
		replaceField.pack(side = RIGHT)
		
		label = TLabel(main_frame, style='FlatLabel', text = _("Replace to:")+" ")
		label.pack(side = RIGHT, anchor = E)
		
		main_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		main_frame.pack(side = TOP)
		#---------------------------------------------------------
		label=TLabel(top, text=" "+_("Parameters")+" ", style="FlatLabel")
		label.pack()
		
		parametersFrameLabel=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)

		parametersFrameLabel.pack(side = TOP, fill=X, pady=4, padx=4)
		
		parametersFrame = TFrame(parametersFrameLabel, style='FlatFrame')  
		
		self.var_case_sensitive = BooleanVar(top)
		self.var_case_sensitive.set(False)
		self.case_sensitive_check = TCheckbutton(parametersFrame, text = _("Case sensitive"), variable = self.var_case_sensitive)
		self.case_sensitive_check.pack(side = TOP, anchor=W, padx=5)
	   
		self.var_whole_word = BooleanVar(top)
		self.var_whole_word.set(False)
		self.whole_word_check = TCheckbutton(parametersFrame, text = _("Whole word"), variable = self.var_whole_word)
		self.whole_word_check.pack(side = TOP, anchor=W, padx=5)
		
		self.var_regexp = BooleanVar(top)
		self.var_regexp.set(False)
		self.regexpCheck = TCheckbutton(parametersFrame, text = _("RegExp search"), variable = self.var_regexp, command=self.disable_enable_action)
		self.regexpCheck.pack(side = TOP, anchor=W, padx=5)
		
		parametersFrame.pack(side=TOP, fill=X, pady=2)
################################################################
	def replace_text(self,objects, toReplace, replaceTo):		
		for object in objects:
			if object.is_Text:
				
				if self.var_regexp.get():
					if self.var_case_sensitive.get():
						p=re.compile(toReplace)
					else:
						p=re.compile(toReplace, re.I)
					text=p.sub(replaceTo, object.text)
					app.mw.document.SelectObject(object)
					app.mw.document.CallObjectMethod(object.__class__,_('Text Replace'),'SetText',text)
					continue
				
				if self.var_whole_word.get():
					if not self.var_case_sensitive.get():
						if object.text.lower()==toReplace.lower():
							text=replaceTo
							app.mw.document.SelectObject(object)
							app.mw.document.CallObjectMethod(object.__class__,_('Text Replace'),'SetText',text)
					else:
						if object.text==toReplace:
							text=replaceTo
							app.mw.document.SelectObject(object)
							app.mw.document.CallObjectMethod(object.__class__,_('Text Replace'),'SetText',text)
							
				else:
					if object.text.lower().find(toReplace.lower(), 0, len(object.text)) != -1:
						if not self.var_case_sensitive.get():
							text=object.text.lower().replace(toReplace.lower(), replaceTo)
						else:
							text=object.text.replace(toReplace, replaceTo)
						app.mw.document.SelectObject(object)
						app.mw.document.CallObjectMethod(object.__class__,_('Text Replace'),'SetText',text)

			if object.is_Group:
				self.replace_text(object.objects)
################################################################
	def replace(self):
		textObjects=[]
		textToReplace=self.find_var.get().decode('utf-8')
		replaceTo=self.replace_var.get().decode('utf-8')

		for layer in app.mw.document.layers:
			self.replace_text(layer.objects, textToReplace, replaceTo)
		app.mw.canvas.ForceRedraw()
################################################################
	def disable_enable_action(self):
		if self.var_regexp.get():	
			self.whole_word_check['state'] = DISABLED
		else:
			self.whole_word_check['state'] = NORMAL
################################################################
	def whole_word_action(self):
		pass
################################################################

instance=FindReplacePanel()
app.extentions_plugins.append(instance)
