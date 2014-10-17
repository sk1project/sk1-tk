# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from Tkinter import TOP, LEFT, X, END, WORD
from Tkinter import Label, StringVar, Text

import app
from app import _, config
from app.conf.configurator import Preferences

from sk1sdk.libttk import TLabel, TCombobox
from sk1.cc.prefpanel import PrefPanel
from sk1.tkext import FlatFrame

class GeneralOptionsPanel(PrefPanel):

	name = 'general'
	title = _('General Options')
	category = 'root'
	category_name = _('root')

	def build(self):
		label = TLabel(self, text=self.__class__.name, font=config.preferences.large_font, justify=LEFT)
		label.pack(side=TOP, fill=X)

	def init_vars(self):
		pass

	def apply(self):
		pass

	def restore(self):
#		defaults = Preferences.__dict__
#		items = self.__dict__.items()
		pass



instance = GeneralOptionsPanel()
app.pref_plugins.append(instance)

class GridGuidesPanel(PrefPanel):

	name = 'grid_guides'
	title = _('Grid and Guides')
	icon = 'context_add_centered_guides'
	category = 'root'
	category_name = _('root')

	def build(self):
		label = TLabel(self, text=self.__class__.name, font=config.preferences.large_font, justify=LEFT)
		label.pack(side=TOP, fill=X)

	def init_vars(self):
		pass

	def apply(self):
		pass

	def restore(self):
#		defaults = Preferences.__dict__
#		items = self.__dict__.items()
		pass



instance = GridGuidesPanel()
app.pref_plugins.append(instance)

class FontsPanel(PrefPanel):

	name = 'fonts'
	title = _('Application fonts')
	icon = 'context_font_name'
	category = 'root'
	category_name = _('root')

	def build(self):
		label = TLabel(self, text=self.__class__.name, font=config.preferences.large_font, justify=LEFT)
		label.pack(side=TOP, fill=X)

	def init_vars(self):
		pass

	def apply(self):
		pass

	def restore(self):
#		defaults = Preferences.__dict__
#		items = self.__dict__.items()
		pass



instance = FontsPanel()
app.pref_plugins.append(instance)

class ColorManagementPanel(PrefPanel):

	name = 'color_management'
	title = _('Color Management')
	icon = 'enable_cms'
	category = 'root'
	category_name = _('root')

	def build(self):
		label = TLabel(self, text=self.__class__.name, font=config.preferences.large_font, justify=LEFT)
		label.pack(side=TOP, fill=X)

	def init_vars(self):
		pass

	def apply(self):
		pass

	def restore(self):
#		defaults = Preferences.__dict__
#		items = self.__dict__.items()
		pass



instance = ColorManagementPanel()
app.pref_plugins.append(instance)

class RendererOptionsPanel(PrefPanel):

	name = 'renderer'
	title = _('Cairo Renderer')
	icon = 'toolbar_cairo'
	category = 'root'
	category_name = _('root')

	def build(self):
		label = TLabel(self, text=self.__class__.name, font=config.preferences.large_font, justify=LEFT)
		label.pack(side=TOP, fill=X)

	def init_vars(self):
		pass

	def apply(self):
		pass

	def restore(self):
#		defaults = Preferences.__dict__
#		items = self.__dict__.items()
		pass



instance = RendererOptionsPanel()
app.pref_plugins.append(instance)


class PrintingOptionsPanel(PrefPanel):

	name = 'printing'
	title = _('Printing')
	icon = 'print'
	category = 'root'
	category_name = _('root')

	prn_commandrs = ('evince %f', 'acroread %f', 'kprinter %f')
	levels = ('1.3', '1.4', '1.5', '1.6', '1.7')

	def build(self):
		text = _('sK1 generates PDF file as a printing output. So as a printing target you can use any application \
which accepts PDF file on input: evince, kprinter, acroread etc. \
Printing command should contain %f symbols replaced by \
temporal PDF file name during printing.')
		label = Text(self, height=5, wrap=WORD)
		label.pack(side=TOP, anchor='nw')
		label.insert(END, text)

		frame = FlatFrame(self)
		frame.pack(side=TOP, fill=X, expand=1, pady=10)

		frame.columnconfigure(1, weight=1)

		label = Label(frame, text=_('Printing command:'), justify=LEFT)
		label.grid(column=0, row=0, sticky='w')


		combo = TCombobox(frame, state='normal', values=self.prn_commandrs, style='ComboNormal',
									 textvariable=self.var_print_command)#, width=30)
		combo.grid(column=1, row=0, sticky='we', pady=5, padx=10)

		label = Label(frame, text=_('Output PDF level:'), justify=LEFT)
		label.grid(column=0, row=1, sticky='w')


		combo = TCombobox(frame, state='readonly', values=self.levels, style='ComboNormal',
									 width=10, textvariable=self.var_pdf_level)
		combo.grid(column=1, row=1, sticky='w', pady=5, padx=10)

	def init_vars(self):
		self.var_print_command = StringVar(self)
		self.var_print_command.set(config.preferences.print_command)
		self.var_pdf_level = StringVar(self)
		self.var_pdf_level.set(config.preferences.pdf_level)

	def apply(self):
		if not config.preferences.print_command == self.var_print_command.get():
			config.preferences.print_command = self.var_print_command.get()
		if not config.preferences.pdf_level == self.var_pdf_level.get():
			config.preferences.pdf_level = self.var_pdf_level.get()

	def restore(self):
		defaults = Preferences.__dict__
		self.var_print_command.set(defaults['print_command'])
		self.var_pdf_level.set(defaults['pdf_level'])



instance = PrintingOptionsPanel()
app.pref_plugins.append(instance)

