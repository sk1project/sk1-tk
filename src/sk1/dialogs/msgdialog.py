# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2003 by Bernhard Herzog 
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
from dialog import ModalDialog

from sk1sdk.libttk import TButton, TLabel, TFrame
from Tkinter import TOP, LEFT, RIGHT, BOTTOM, X, BOTH
from types import TupleType

from sk1.tkext import UpdatedButton



Ok = _("OK")
Yes = _("Yes")
No = _("No")
Save =_("Save")
SaveDontSaveCancel =_("Don't Save")
Cancel  =_("Cancel")
OkCancel = (Ok, Cancel)
YesNo = (Yes, No)
YesNoCancel = (Yes, No, Cancel)
SaveDontSaveCancel = (Save, SaveDontSaveCancel, Cancel)

class MessageDialog(ModalDialog):

	class_name = 'MessageDialog'
	
	def __init__(self, master, title, message, buttons = _("OK"), default = 0, icon = 'warning', dlgname = '__dialog__'):
		self.title = title
		self.message = message
		if type(buttons) != type(()):
			buttons = (buttons,)
		self.buttons = buttons
		self.default = -1
		self.image = icon
		ModalDialog.__init__(self, master, name = dlgname)
	
	def build_dlg(self):
		root = self.top
		top = TFrame(root, style='FlatFrame', borderwidth = 10)
		top.pack(side = TOP, fill = BOTH, expand = 1)
		
		frame = TFrame(top, name = 'top', style='FlatFrame')
		frame.pack(side = TOP, fill = BOTH, expand = 1)
		label = TLabel(frame, image = 'messagebox_'+self.image, style='FlatLabel')
		label.pack(side = LEFT, padx = 10, pady = 5)
		label = TLabel(frame, text = self.message, name = 'msg', style='FlatLabel', justify='center', anchor='center')
		label.pack(side = RIGHT, fill = BOTH, expand = 1, padx = 5)
	
		frame = TFrame(top, name = 'bot', style='FlatFrame')
		frame.pack(side = BOTTOM)#, fill = X, expand = 1)
		root.protocol('WM_DELETE_WINDOW', self.stub)
	
		command = self.ok
		for i in range(len(self.buttons)):
			button = UpdatedButton(frame, text = ' '+self.buttons[i]+' ', command = command, args = i)
			button.grid(column = i, row = 0, sticky = 'ew', padx = 10, pady= 0)
			if i == self.default:
				button['default'] = 'active'
				self.focus_widget = button
			else:
				button['default'] = 'normal'
	
		if self.default is not None:
			top.bind('<Return>', self.invoke_default)
			
		frame = TFrame(top, name = 'mid', style='FlatFrame', borderwidth=1)
		frame.pack(side = TOP, fill = X)

		root.resizable (width=0, height=0)
	
	def ok(self, pos):
		self.close_dlg(pos)
	
	def invoke_default(self, *rest):
		self.ok(self.default)
		
def msgDialog(master, title, message, buttons = Ok, default = 0, icon = 'warning', icon1= 'warning'):
	if type(buttons) != TupleType:
		buttons = (buttons,)	
	dlg = MessageDialog(master, title, message, buttons, default, icon, icon1)
	result = dlg.RunDialog()
	if result is not None:
		return buttons[result]
	return ''
