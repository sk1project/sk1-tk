# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TCombobox, TLabel
from sk1.tkext import UpdatedRadiobutton
from app.conf.const import SELECTION, EDITED
from Tkinter import LEFT, StringVar
from subpanel import CtxSubPanel
from app import  _
from app.Graphics import text
from uc import libpango
from sk1sdk.libttk import tooltips
from string import atof

class FontPanel(CtxSubPanel):

	name = 'FontPanel'
	family_to_fonts = {}
	families = []
	styles = []
	bold = 0
	italic = 0


	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)

		self.var_font_name = StringVar(self.mw.root, ' ')
		self.var_style_name = StringVar(self.mw.root, ' ')
		self.var_font_size = StringVar(self.mw.root, ' ')

		label = TLabel(self.panel, image='context_font_name')
		label.pack(side=LEFT, padx=2)
		tooltips.AddDescription(label, _('Font name'))
		self.font_name = TCombobox(self.panel, state='readonly', postcommand=self.name_changed,
									 values=self.make_families(), width=25, style='PseudoActive',
									 textvariable=self.var_font_name)
		self.font_name.pack(side=LEFT, padx=2)

		label = TLabel(self.panel, text=' ')
		label.pack(side=LEFT)

		label = TLabel(self.panel, image='context_font_style')
		label.pack(side=LEFT)
		tooltips.AddDescription(label, _('Font style'))
		self.style_name = TCombobox(self.panel, state='readonly', postcommand=self.style_changed,
									 values=(), width=18, style='PseudoActive',
									 textvariable=self.var_style_name)
		self.style_name.pack(side=LEFT, padx=2)

		label = TLabel(self.panel, text=' ')
		label.pack(side=LEFT)

		label = TLabel(self.panel, image='context_font_size')
		label.pack(side=LEFT)
		tooltips.AddDescription(label, _('Font size'))
		self.font_size = TCombobox(self.panel, state='normal', postcommand=self.apply_changes,
									 values=self.make_sizes(), width=5, style='ComboNormal',
									 textvariable=self.var_font_size)
		self.font_size.pack(side=LEFT, padx=2)

		######################################
		self.var_bold = StringVar(self.mw.root, '')
		self.var_italic = StringVar(self.mw.root, '')
		self.var_underline = StringVar(self.mw.root, '')

		self.bold_check = UpdatedRadiobutton(self.panel, value='bold', image='context_text_bold',
								command=self.bold_action, variable=self.var_bold, style='ToolbarRadiobutton')
		self.bold_check.pack(side=LEFT, padx=2)
		tooltips.AddDescription(self.bold_check, _('Bold'))

		self.italic_check = UpdatedRadiobutton(self.panel, value='italic', image='context_text_italic',
								command=self.italic_action, variable=self.var_italic, style='ToolbarRadiobutton')
		self.italic_check.pack(side=LEFT, padx=2)
		tooltips.AddDescription(self.italic_check, _('Italic'))

#		self.underline_check = UpdatedRadiobutton(self.panel, value = 'under', image='context_text_under_disabled', state='disabled',
#								command=self.action, variable = self.var_underline, style='ToolbarRadiobutton')
#		self.underline_check.pack(side=LEFT, padx=2)
#		tooltips.AddDescription(self.underline_check, _('Underline'))

		self.ReSubscribe()

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.Update)
		self.doc.Subscribe(EDITED, self.Update)


	def Update(self, *arg):
		object = self.mw.document.CurrentObject()
		if object is not None and object.is_Text:
			_font = object.Font()
			self.var_font_name.set(_font.familyname)
			self.var_style_name.set(_font.facename)
			self.style_name['values'] = self.make_styles()
			self.var_font_size.set(object.FontSize())
#		else:
#			try:
#				default = ft2engine.GetFont(config.preferences.default_font)
#			except:
#				name = self.family_to_fonts.keys()[0]#[0]
#				fonts = self.family_to_fonts[name]
#				default = ft2engine.GetFont(fonts[1])
#			self.var_font_name.set(default.family)
#			self.var_style_name.set(default.font_attrs)
#			self.style_name['values'] = self.make_styles()
#			self.var_font_size.set(properties.default_text_style.font_size)
		self.checkBI()

	def make_families(self):
		result = ()
		self.families = libpango.FAMILIES_LIST
		for item in self.families:
			result += (item,)
		return result

	def make_styles(self):
		faces = libpango.FAMILIES_DICT[self.var_font_name.get()]
		attrs = ()
		self.styles = []
		for name in faces:
			self.styles.append(name)
			attrs += (name,)
		return attrs

	def make_sizes(self):
		sizes = ()
		for size in [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32,
					36, 40, 48, 56, 64, 72]:
			sizes += (size,)
		return sizes

	def name_changed(self):
		self.style_name['values'] = self.make_styles()
		if not self.var_style_name.get() in self.styles:
			self.setRegular()
		self.checkBI()
		self.apply_changes()

	def style_changed(self):
		self.checkBI()
		self.apply_changes()

	def apply_changes(self):
		familyname = self.var_font_name.get()
		facename = self.var_style_name.get()
		self.mw.document.CallObjectMethod(text.CommonText,
						_("Set Font Properties"), 'SetFont',
						 libpango.get_fontface(familyname, facename),
						 atof(self.var_font_size.get()))
		self.mw.canvas.ForceRedraw()

	def bold_action(self):
		if self.bold:
			self.bold = 0
			self.var_bold.set('')
		else:
			self.bold = 1
			self.var_bold.set('bold')

		if self.bold and self.italic:
			if 'Bold Italic' in self.styles:
				self.var_style_name.set('Bold Italic')
			elif 'Bold Oblique' in self.styles:
				self.var_style_name.set('Bold Oblique')
			else:
				self.bold = 0
				self.var_bold.set('')
		elif self.bold:
			self.var_style_name.set('Bold')
		elif self.italic:
			if 'Italic' in self.styles:
				self.var_style_name.set('Italic')
			if 'Oblique' in self.styles:
				self.var_style_name.set('Oblique')
		else:
			self.setRegular()
		self.style_changed()

	def italic_action(self):
		if self.italic:
			self.italic = 0
			self.var_italic.set('')
		else:
			self.italic = 1
			self.var_italic.set('italic')

		if self.bold and self.italic:
			if 'Bold Italic' in self.styles:
				self.var_style_name.set('Bold Italic')
			elif 'Bold Oblique' in self.styles:
				self.var_style_name.set('Bold Oblique')
			else:
				self.italic = 0
				self.var_italic.set('')
		elif self.italic:
			if 'Italic' in self.styles:
				self.var_style_name.set('Italic')
			if 'Oblique' in self.styles:
				self.var_style_name.set('Oblique')
		elif self.bold:
			self.var_style_name.set('Bold')
		else:
			self.setRegular()
		self.style_changed()

	def setRegular(self):
		normal = None
		for	item in ['Roman', 'Book', 'Normal', 'Regular']:
			if item in self.styles:
				normal = item
		if normal:
			self.var_style_name.set(normal)
		else:
			self.var_style_name.set(self.styles[0])

	def checkBI(self):
		if 'Bold' in self.styles:
			self.bold_check['state'] = 'normal'
		else:
			self.bold_check['state'] = 'disabled'
			self.bold = 0
			self.var_bold.set('')
		if 'Italic' in self.styles or 'Oblique' in self.styles:
			self.italic_check['state'] = 'normal'
		else:
			self.italic = 0
			self.italic_check['state'] = 'disabled'
			self.var_italic.set('')

		if self.var_style_name.get() == 'Bold':
			self.bold = 1
			self.italic = 0
			self.var_bold.set('bold')
			self.var_italic.set('')
		elif self.var_style_name.get() in ['Italic', 'Oblique']:
			self.bold = 0
			self.italic = 1
			self.var_italic.set('italic')
			self.var_bold.set('')
		elif self.var_style_name.get() in ['Bold Italic', 'Bold Oblique']:
			self.bold = 1
			self.italic = 1
			self.var_bold.set('bold')
			self.var_italic.set('italic')
		else:
			self.bold = 0
			self.italic = 0
			self.var_bold.set('')
			self.var_italic.set('')

	def action(self):
		pass





