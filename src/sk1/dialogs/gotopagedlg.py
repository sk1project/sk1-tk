# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
import app
from dialog import ModalDialog
from msgdialog import msgDialog

from sk1sdk.libttk import TButton, TLabel, TFrame
from sk1.ttk_ext import TSpinbox
from Tkinter import StringVar
from Tkinter import TOP, LEFT, RIGHT, BOTTOM, X, BOTH, W


class GoToPageDialog(ModalDialog):

	class_name = 'GoToPageDialog'
	
	def __init__(self, master, is_before = 0, dlgname = '__dialog__'):
		self.master=master
		self.title = _("Go to page")
		self.is_before=is_before
		self.init_vars()
		ModalDialog.__init__(self, master, name = dlgname)
		
	def init_vars(self):
		self.pagenum=StringVar(self.master)
		self.pagenum.set('%u'%(app.mw.document.active_page+1))
	
	def build_dlg(self):
		root = TFrame(self.top, style='FlatFrame', borderwidth = 10)
		root.pack(side = TOP, fill = BOTH, expand = 1)

		middle = TFrame(root, style='FlatFrame', borderwidth = 5)
		middle.pack(side = TOP, fill = X, expand = 1)
	
		label = TLabel(middle, text = _("Go to page No.:")+" ", style='FlatLabel')
		label.pack(side = LEFT)
		self.pagenum_spin = TSpinbox(middle, var=app.mw.document.active_page+1, vartype=0, textvariable = self.pagenum,
						min = 1, max = len(app.mw.document.pages), step = 1, width = 6, command = self.ok)
		self.pagenum_spin.pack(side = LEFT)
		if len(app.mw.document.pages)==1:
			self.pagenum_spin.set_state('disabled')
			

		bottom = TFrame(root, style='FlatFrame', borderwidth = 5)
		bottom.pack(side = BOTTOM, fill = X, expand = 1)
		cancel = TButton(bottom, text=_("Cancel"), command=self.cancel)
		cancel.pack(side = RIGHT)

		label = TLabel(bottom, text = '  ', style='FlatLabel')
		label.pack(side = RIGHT)
		ok = TButton(bottom, text=_("OK"), command=self.ok)
		ok.pack(side = RIGHT)
		self.focus_widget = ok
		
		self.top.bind('<Escape>', self.cancel)
		self.top.protocol('WM_DELETE_WINDOW', self.cancel)		
		self.top.resizable (width=0, height=0)
	
	def ok(self, *arg):		
		if not 0 <= self.pagenum_spin.get_value()-1 < len(app.mw.document.pages):
			msgDialog(self.top, title = _("Error"), message = _('Incorrect page number!'))
			self.pagenum_spin.entry.focus_set()
			return
		if self.pagenum_spin.get_value()-1<>app.mw.document.active_page:
			app.mw.document.GoToPage(self.pagenum_spin.get_value()-1)
		self.close_dlg()
	
	def cancel(self, *arg):
		self.close_dlg(None)
		
def gotopgDialog(master):
	dlg = GoToPageDialog(master)
	dlg.RunDialog()