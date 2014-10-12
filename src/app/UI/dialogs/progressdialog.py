# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
import app
from dialog import ModalDialog
from msgdialog import msgDialog

from sk1sdk.libttk import TLabel, TFrame, TProgressbar
from Tkinter import TOP, LEFT, RIGHT, BOTTOM, X, BOTH, W
from app import info1, info2, info3, info_win
import threading, time


class ProgressDialog(ModalDialog):

	class_name = 'ProgressDialog'
	
	def __init__(self, master, title = '', dlgname = '__dialog__'):
		self.master=master
		self.title = title
		ModalDialog.__init__(self, master, name = dlgname)
	
	def build_dlg(self):		
		root = TFrame(self.top, style='FlatFrame', borderwidth = 10)
		root.pack(side = TOP, fill = BOTH, expand = 1)
	
		label = TLabel(root, text = '', style='FlatLabel', textvariable=info1)
		label.pack(side = TOP, anchor=W, pady=5)
		
		label = TLabel(root, text = '', style='FlatLabel', textvariable=info2)
		label.pack(side = TOP, anchor=W, pady=5)
		
		self.prgrs = TProgressbar(root, orient = 'horizontal', style='Horizontal.Progress',
								length = 450, value=10, variable=info3)
		self.prgrs.pack(side = TOP, anchor=W)

		self.top.protocol('WM_DELETE_WINDOW', self.cancel)		
		self.top.resizable (width=0, height=0)
		
	def RunDialog(self, callback, *arg):
		app.info_win = self.top
		self.wait=0		
		ModalDialog.RunDialog(self)
		self.top.update()		
		result=callback(arg)
		##### --> return from callback
		self.CloseDialog()
		return result
	
	def CloseDialog(self):
		self.close_dlg()
		self.top.destroy()
		info3.set(0)
		app.info_win = None

class DialogUpdateThread(threading.Thread):

    def run(self):
        while(not app.info_win is None):
        	print app.info3.get()
        	app.info_win.update()
        	time.sleep(0.1)		
