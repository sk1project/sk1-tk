# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from Tkinter import StringVar, TOP, LEFT, Y, X, BOTH, Widget, END
from tkext import WidgetWithCommand, ComboMenu, ComboCommand, MenuCommand, UpdatedMenu, MakeCommand
from app import _

from Ttk import TFrame, TButton, TEntry, TMenubutton


class TEntryExt(TEntry):
	
	def __init__(self, master=None, cnf={}, **kw):
		TEntry.__init__(self, master, kw)
		self.bind('<ButtonPress-3>', self.popup_context_menu)

#--------ContextMenu-----------------------------------------------------------
	def popup_context_menu(self, event):
		self.context_menu = UpdatedMenu(self, [], tearoff = 0, auto_rebuild = self.build_context_menu)
		self.context_menu.Popup(event.x_root, event.y_root)

	def build_context_menu(self):
		entries=[]
		if self.can_cut():		
			entries += [(_("Cut"), self.cut,(),None,None,'menu_edit_cut')]
		if self.can_copy():
			entries +=[(_("Copy"), self.copy,(),None,None,'menu_edit_copy')]
		if self.can_paste():
			entries +=[(_("Paste"), self.paste,(),None,None,'menu_edit_paste')]
		entries +=[(_("Clear All"), self.clear_all,(),None,None, 'menu_edit_clear'),
				(None,'small_separator'),
				(_("Select All"), self.select_all,(),None,None)
				]
		return map(MakeCommand, entries)	

	def can_cut(self):
		return self.select_present()
	
	def can_copy(self):
		return self.select_present()
	
	def can_paste(self):
		if self.clipboar_get():
			return 1
		return 0
	
	def select_all(self):
		self.select_range(0, END)
		
	def clear_all(self):
		self.delete(0, END)
		
	def clipboar_get(self):
		try:
			return self.tk.call('::tk::GetSelection','.','CLIPBOARD')
		except:
			return None
		
	def cut(self):
		self.tk.call('::ttk::entry::Cut',self._w)
		
	def copy(self):
		self.tk.call('::ttk::entry::Copy',self._w)
	
	def paste(self):
		self.tk.call('::ttk::entry::Paste',self._w)
		
#--------ContextMenu-----------------------------------------------------------
	
class TSpinbox(TFrame):
	def __init__(self, master=None, min=0, max=100, step=1, textvariable=None, var=0, vartype=0, command=None, state='enabled', width=5, args=(), **kw):
		'''vartype=0 - integer   vartype=1 - float '''
		self.min_value=min
		self.max_value=max
		self.step=step
		self.variable=var
		self.vartype=vartype
		if textvariable:
			self.text_var=textvariable
		else:
			self.text_var=StringVar()
		self.command=command
		self.state=state
		self.width=width
		apply(TFrame.__init__, (self, master), kw)
		self["style"]="FlatFrame"
		self.entry=TEntryExt(self, textvariable=self.text_var, width=self.width, style='SpinEntry')
		self.entry.pack(side = LEFT, expand = 1, fill = BOTH)
		self.button_frame=TFrame(self,style="FlatFrame")
		self.button_frame.pack(side = LEFT,fill = Y)
		self.up_button=TButton(self.button_frame, class_='Repeater', command=self.increase, 
							image='pal_arrow_up', style='SpinUpButton')
		self.up_button.pack(side = TOP)
		self.down_button=TButton(self.button_frame, class_='Repeater', command=self.decrease,
							image='pal_arrow_down', style='SpinDownButton')
		self.down_button.pack(side = TOP)
		if self.vartype==1: 
			self.variable=float(self.variable)
		else:
			self.variable=int(self.variable)
		self.text_var.set(str(self.variable))
		self.entry.bind('<Button-4>', self.wheel_increase)
		self.entry.bind('<Button-5>', self.wheel_decrease)
		self.entry.bind('<Key-Return>', self.command)
		self.entry.bind('<Key-KP_Enter>', self.command)
		self.entry.bind ( '<KeyPress>', self.check_input)
		
	def check_input(self, event):
		print event.char
		event=None
		
	def set_state(self, state):
		self.state=state
		self.entry.configure(state = state)
		self.up_button.configure(state = state)
		self.down_button.configure(state = state)
		
	def get_state(self):
		return self.state
		
	def wheel_increase(self, event):
		self.increase()
		
	def wheel_decrease(self, event):
		self.decrease()
		
	def increase(self):
		if self.state=='enabled':
			try:
				self.variable=float(self.text_var.get())
			except:
				self.text_var.set('0')
				self.variable=float(self.text_var.get())
			self.variable=self.variable+self.step
			if self.variable>self.max_value:
				self.variable=self.variable-self.step
			if self.vartype==1: 
				self.variable=float(self.variable)
			else:
				self.variable=int(self.variable)
			self.text_var.set(str(self.variable))
		
	def decrease(self):
		if self.state=='enabled':
			try:
				self.variable=float(self.text_var.get())
			except:
				self.text_var.set('0')
				self.variable=float(self.text_var.get())
			self.variable=self.variable-self.step
			if self.variable<self.min_value:
				self.variable=self.variable+self.step
			if self.vartype==1: 
				self.variable=float(self.variable)
			else:
				self.variable=int(self.variable)
			self.text_var.set(str(self.variable))
		
	def set_value(self, value=0):
		if self.vartype==1: 
			self.variable=float(value)
		else:
			self.variable=int(value)
		self.text_var.set(str(self.variable))
	
	def get_value(self):
		try:
			self.variable=float(self.text_var.get())
		except:
			self.text_var.set('0')
			self.variable=float(self.text_var.get())
		if self.vartype==1: 
			self.variable=float(self.variable)
		else:
			self.variable=int(self.variable)
		return self.variable
			
		
	def destroy(self):
		self.entry.unbind_all(self.entry)
		self.entry.destroy()
		self.button_frame.destroy()
		self.up_button.destroy()
		self.down_button.destroy()
		self.command = self.args = None
		TFrame.destroy(self)

class TEntrybox(TFrame):
	def __init__(self, master=None, text='', vartype=0, command=None, state='enabled', width=5, args=(), **kw):
		self.vartype=vartype
		self.text_var=StringVar()
		self.command=command
		self.state=state
		self.width=width
		apply(TFrame.__init__, (self, master), kw)
		self["style"]="FlatFrame"
		self.entry=TEntryExt(self, textvariable=self.text_var, width=self.width)
		self.entry.pack(side = LEFT, expand = 1, fill = BOTH)
		
		self.text_var.set(text)
		self.entry.bind('<Key-Return>', self.command)
		self.entry.bind('<Key-KP_Enter>', self.command)
		
	def set_state(self, state):
		self.state=state
		self.entry.configure(state = state)
		
	def get_state(self):
		return self.state
		
	def set_focus(self):
		self.entry.focus()
		
	
	def set_text(self, text=''):
		self.text_var.set(text)
	
	def get_text(self):
		return self.text_var.get()
		
	def destroy(self):
		self.entry.unbind_all(self.entry)
		self.entry.destroy()
		self.command = self.args = None
		TFrame.destroy(self)
		
		
		
class TComboSmall(WidgetWithCommand, TMenubutton):

	tk_widget_has_command = 0

	def __init__(self, master, values, command = None, args = (), variable = None, **kw):

		kw['style'] = 'TComboSmall'
		if variable is not None:
			kw['textvariable'] = variable
		self.variable = variable
		WidgetWithCommand.__init__(self)
		Widget.__init__(self, master, "ttk::menubutton", kw)
		if command:
			self.set_command(command, args)

		entries = []
		for value in values:
			entries.append(ComboCommand(value, command = self.choose_opt, args = value))
			
		self.__menu = ComboMenu(self, entries, auto_update = 0, name="menu", tearoff=0)

		menu = self.__menu.menu
		self.menuname = menu._w
		self["menu"] = menu

	def destroy(self):
		WidgetWithCommand.clean_up(self)
		TMenubutton.destroy(self)
		self.__menu = None

	def choose_opt(self, value):
		self['text'] = value
		self._call_cmd(value)

	def __getitem__(self, name):
		if name == 'menu':
			return self.__menu.menu
		return Widget.__getitem__(self, name)
	