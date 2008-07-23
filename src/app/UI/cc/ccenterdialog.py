# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
import app, os, string, sys
from app.UI.dialogs.dialog import ModalDialog
from app.UI.widgets.resframe import ResizableTFrame
from app import dialogman

from Ttk import TButton, TLabel, TFrame, TScrollbar
from app.UI.ttk_ext import TSpinbox
from Tkinter import Canvas
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END, NONE



class ControlCenter(ModalDialog):

	class_name = 'ControlCenter'
	
	def __init__(self, master, dlgname = '__dialog__'):
		self.master=master
		self.title = _("sK1 Preferences")
		ModalDialog.__init__(self, master, name = dlgname)
	
	def build_dlg(self):
		self.root = TFrame(self.top, style='FlatFrame', borderwidth = 10)
		self.root.pack(side = TOP, fill = BOTH, expand = 1)
		
		##### top panel #########################RoundedFrame
		
		toppanel = TFrame(self.root, style='FlatFrame')		
		toppanel.pack(side = TOP, fill = BOTH, expand = 1)
		
		rpanel = ResizableTFrame(toppanel, self.top, size=260, orient=RIGHT)		
		rpanel.pack(side = LEFT, fill = Y)
		
		panel = TFrame(rpanel.panel, style='RoundedFrame', borderwidth = 5)		
		panel.pack(side = LEFT, fill = BOTH, expand = 1)
		
		can=Canvas(panel, bg='white', width=5, height=5)
		can.pack(side = LEFT, fill = BOTH, expand = 1)
		
		plugpanel = TFrame(toppanel, style='FlatFrame')		
		plugpanel.pack(side = RIGHT, fill = BOTH, expand = 1)
		
		lab=TLabel(plugpanel, style='FlatLabel', text='Test label')
		lab.pack(side = LEFT)
		
		##### line #########################
				
		line = TLabel(self.root, style='HLine2')
		line.pack(side = TOP, fill = X)				

		##### bottom panel #########################
		
		botpanel = TFrame(self.root, style='FlatFrame')		
		botpanel.pack(side = BOTTOM, fill = X, expand=0)

		
		cancel_bt = TButton(botpanel, text=_("Cancel"), command=self.ok)
		cancel_bt.pack(side = RIGHT)
		
		apply_bt = TButton(botpanel, text=_("Apply"), command=self.ok)
		apply_bt.pack(side = RIGHT, padx=10)
		
		ok_bt = TButton(botpanel, text=_("OK"), command=self.ok)
		ok_bt.pack(side = RIGHT)
		
		help_bt = TButton(botpanel, text=_("Help"), state='disabled')
		help_bt.pack(side = LEFT)
		
		rdefs_bt = TButton(botpanel, text=_("Restore Defaults"))
		rdefs_bt.pack(side = LEFT, padx=10)
		
		self.focus_widget = cancel_bt
		
		self.top.bind('<Escape>', self.cancel)
		self.top.protocol('WM_DELETE_WINDOW', self.cancel)
		self.width=700	
		self.height=500
		
	def ok(self, *arg):
		self.close_dlg()
	
	def cancel(self, *arg):
		self.close_dlg(None)