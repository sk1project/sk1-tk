# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2002 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
#	A Dialog for managing dynamic styles
#

from string import atoi

from Tkinter import Frame, IntVar, DISABLED, NORMAL
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, END

import app
from app import _, config
from app.conf.const import STYLE, SELECTION, COMMAND
from app.events.warn import pdebug
from app.Graphics.properties import property_names, property_titles, property_types
from app.Graphics.properties import FillProperty, LineProperty, FontProperty

from sk1sdk.libttk import TFrame, TLabel, TCheckbutton, TButton, TScrollbar, TLabelframe

from sk1.tkext import UpdatedButton, UpdatedListbox, MessageDialog
from sk1.ttk_ext import TEntrybox
from sk1.dialogs.sketchdlg import PropertyPanel, SKModal

class StylePanel(PropertyPanel):

	title = _("Styles")
	receivers = PropertyPanel.receivers[:]

	def __init__(self, master, main_window, doc):
		PropertyPanel.__init__(self, master, main_window, doc, name='styledlg')
		self.main_window = main_window

	def build_dlg(self):
		root = self.top

		top = TFrame(root, borderwidth=2, style='FlatFrame')
		top.pack(side=TOP, expand=0, fill=BOTH)

		top2 = TFrame(top, height=3, style='FlatFrame')
		top2.pack(side=BOTTOM, expand=0, fill=X)

		button = UpdatedButton(top, text=_("Apply style"), command=self.apply_style, sensitivecb=self.can_apply, width=15)
		button.pack(side=BOTTOM, expand=0)
		self.Subscribe(SELECTION, button.Update)

		top2 = TFrame(top, height=3, style='FlatFrame')
		top2.pack(side=BOTTOM, expand=0, fill=X)

		button = UpdatedButton(top, text=_("Delete style"), command=self.remove_style, sensitivecb=self.can_remove, width=15)
		button.pack(side=BOTTOM, expand=0)

		top2 = TFrame(top, height=3, style='FlatFrame')
		top2.pack(side=BOTTOM, expand=0, fill=X)

		button = UpdatedButton(top, text=_("Create new style"), command=self.CreateStyleFromSelection,
							sensitivecb=self.main_window.document.CanCreateStyle, width=15)
		button.pack(side=BOTTOM, expand=0)
		self.Subscribe(SELECTION, button.Update)

		top2 = TFrame(top, height=5, style='FlatFrame')
		top2.pack(side=BOTTOM, expand=0, fill=X)

		list_frame = TFrame(top, style="RoundedFrame", borderwidth=5)
		list_frame.pack(side=TOP, expand=1, fill=BOTH)

		sb_vert = TScrollbar(list_frame, takefocus=0)
		sb_vert.pack(side=RIGHT, fill=Y)

		styles = UpdatedListbox(list_frame, bg='white', borderwidth=0, selectborderwidth=0)
		styles.pack(expand=1, fill=BOTH)
		styles.Subscribe(COMMAND, self.apply_style)

		sb_vert['command'] = (styles, 'yview')
		styles['yscrollcommand'] = (sb_vert, 'set')
		self.styles = styles
		root.resizable(width=0, height=0)

	def init_from_doc(self):
		self.styles_changed()
		self.Update()
		self.issue(SELECTION)

	def Update(self):
		self.styles.select_clear(0, END)
		properties = self.document.CurrentProperties()
		for name in properties.DynamicStyleNames():
			idx = self.style_names.index(name)
			self.styles.select_set(idx)
			self.styles.see(idx)

	receivers.append((STYLE, 'styles_changed'))
	def styles_changed(self):
		self.style_names = self.document.GetStyleNames()
		self.styles.SetList(self.style_names)
		self.Update()

	can_apply = PropertyPanel.doc_has_selection

	def apply_style(self):
		sel = self.styles.curselection()
		if sel:
			index = atoi(sel[0])
			self.document.AddStyle(self.style_names[index])

	def CreateStyleFromSelection(self):
		doc = self.document
		object = doc.CurrentObject()
		style_names = doc.GetStyleNames()
		if object:
			name = GetStyleName(self.top, object, style_names)
			if name:
				name, which_properties = name
				doc.CreateStyleFromSelection(name, which_properties)

	def can_remove(self):
		len(self.styles.curselection()) == 1

	def remove_style(self):
		sel = self.styles.curselection()
		if sel:
			index = atoi(sel[0])
			self.document.RemoveDynamicStyle(self.style_names[index])


class CreateStyleDlg(SKModal):

	title = _("Create Style")

	def __init__(self, master, object, style_names, **kw):
		self.object = object
		self.style_names = style_names
		apply(SKModal.__init__, (self, master), kw)

	def __del__(self):
		if __debug__:
			pdebug('__del__', '__del__', self)

	def build_dlg(self):
		root = self.top

		top = TFrame(root, borderwidth=5, style='FlatFrame')
		top.pack(side=TOP, expand=0, fill=BOTH)

		top2 = TFrame(top, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		format_label = TLabel(top2, text=_('Style name:'), borderwidth=0)
		format_label.pack(side=LEFT, pady=3)

		self.entry_name = TEntrybox(top, command=self.ok, width=15)
		self.entry_name.pack(side=TOP, fill=X)

		top2 = TFrame(top, height=5, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		prop_cont = TLabelframe(top, text=_('Style properties'), padding=10)
		prop_cont.pack(side=TOP, fill=X)

		properties = self.object.Properties()
		self.flags = {}
		for prop in property_names:
			type = property_types[prop]
			if type == FillProperty:
				state = self.object.has_fill and NORMAL or DISABLED
			elif type == LineProperty:
				state = self.object.has_line and NORMAL or DISABLED
			elif type == FontProperty:
				state = self.object.has_font and NORMAL or DISABLED
			else:
				# unknown property type!
				continue
			long, short = property_titles[prop]
			self.flags[prop] = var = IntVar(root)
			var.set(state == NORMAL)
			radio = TCheckbutton(prop_cont, text=long, state=state, variable=var)
			radio.pack(side=TOP, anchor=W)

		top2 = TFrame(top, height=3, style='FlatFrame')
		top2.pack(side=TOP, expand=0, fill=X)

		but_frame = Frame(top)
		but_frame.pack(side=TOP, fill=X)

		button = TButton(but_frame, text=_("Cancel"), command=self.cancel)
		button.pack(side=RIGHT, padx=5)
		button = TButton(but_frame, text=_("OK"), command=self.ok)
		button.pack(side=RIGHT, padx=5)

		root.resizable (width=0, height=0)

		self.entry_name.set_focus()

	def ok(self, *args):
		name = self.entry_name.get_text()
		if not name:
			MessageDialog(self.top, title=_("Create Style Info"),
							message=_("Please enter a style name."),
							icon='info')
			return
		if name in self.style_names:
			MessageDialog(self.top, title=_("Create Style"),
							message=_("The name `%(name)s' is already used.\n"
										"Please choose another one.") % locals(),
							icon='info')
			return

		which_properties = []
		for prop, var in self.flags.items():
			if var.get():
				which_properties.append(prop)
		self.close_dlg((name, which_properties))


def GetStyleName(master, object, style_names):
	dlg = CreateStyleDlg(master, object, style_names)
	return dlg.RunDialog()






class SetDefaultPropertiesDlg(SKModal):

	title = _("Set Default Properties")

	def __init__(self, master, category):
		self.category = category
		SKModal.__init__(self, master, name='setdefaults')

	def build_dlg(self):

		root = self.top
		top = TFrame(root, style='FlatFrame', borderwidth=13)
		top.pack(side=TOP)

		label = TLabel(top, text=_("Please select the object categories whose\n default properties you want to change"))
		label.pack(side=TOP, anchor=W)
		frame = TFrame(top, style='FlatFrame', borderwidth=10)
		frame.pack(side=TOP)
		self.var_graphics_style = IntVar(top)
		self.var_graphics_style.set(0)
		if self.category != 'font':
			self.var_graphics_style.set(1)
		button = TCheckbutton(frame, text=_("Graphics Objects"), state=(self.category == 'font' and DISABLED or NORMAL), variable=self.var_graphics_style)
		button.pack(side=TOP, anchor=W)
		self.var_text_style = IntVar(top)
		self.var_text_style.set(0)
		if self.category == 'font':
			self.var_text_style.set(1)
		button = TCheckbutton(frame, text=_("Text Objects"), state=(self.category == 'line' and DISABLED or NORMAL), variable=self.var_text_style)
		button.pack(side=TOP, anchor=W)

		label = TLabel(top, style="HLine")
		label.pack(side=TOP, fill=BOTH)

		but_frame = TFrame(top, style='FlatFrame')
		but_frame.pack(side=TOP, fill=BOTH, expand=1)

		button = TButton(but_frame, text=_("Cancel"), command=self.cancel)
		button.pack(side=RIGHT, expand=1)

		button = TButton(but_frame, text=_("OK"), command=self.ok)
		button.pack(side=RIGHT, expand=1)


		root.resizable (width=0, height=0)

	def ok(self, *args):
		graph = self.var_graphics_style.get()
		text = self.var_text_style.get()
		self.close_dlg((graph, text))


def WhichDefaultStyles(master, category=0):
	dlg = SetDefaultPropertiesDlg(master, category)
	return dlg.RunDialog()


def set_properties(master, document, title, category, kw):
	if document.HasSelection():
		document.BeginTransaction(title)
		try:
			apply(document.SetProperties, (), kw)
		finally:
			document.EndTransaction()
	else:
		if config.preferences.set_default_properties:
			# remove the if_type_present argument if present. The font
			# dialog uses it in a kludgy way to avoid setting the font
			# on a non-text object.
			if kw.has_key("if_type_present"):
				del kw["if_type_present"]
			which = WhichDefaultStyles(master, category=category)
			if which:
				if which[0]:
					app.Graphics.properties.set_graphics_defaults(kw)
				if which[1]:
					app.Graphics.properties.set_text_defaults(kw)
