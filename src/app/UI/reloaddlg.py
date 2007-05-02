# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import operator, string

from app.events.warn import pdebug, warn_tb, INTERNAL

from Tkinter import Frame, Scrollbar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, TOP
from tkext import UpdatedButton, UpdatedListbox, COMMAND

from sketchdlg import SketchPanel
import prompt


class ReloadPanel(SketchPanel):

	title = 'Reload Modules'
	receivers = []

	def __init__(self, master, main_window, doc):
		SketchPanel.__init__(self, master, main_window, doc,
								name = 'reloaddlg')

	def build_dlg(self):
		top = self.top

		list_frame = Frame(top)
		list_frame.pack(side = TOP, expand = 1, fill = BOTH)

		sb_vert = Scrollbar(list_frame, takefocus = 0)
		sb_vert.pack(side = RIGHT, fill = Y)
		module_list = UpdatedListbox(list_frame, name = 'list')
		module_list.pack(expand = 1, fill = BOTH)
		module_list.Subscribe(COMMAND, self.do_reload)
		sb_vert['command'] = (module_list, 'yview')
		module_list['yscrollcommand'] = (sb_vert, 'set')
		self.module_list = module_list

		frame = Frame(top)
		frame.pack(side = BOTTOM, fill = X)
		for text, cmd in [('Reload Module', self.do_reload),
							('Update List', self.update_list),
							('Close', self.close_dlg)]:
			button = UpdatedButton(frame, text = text, command = cmd)
			button.pack(side = TOP, fill = X, expand = 1)

		self.update_list()


	def init_from_doc(self):
		pass

	def update_list(self):
		modules = prompt.get_sketch_modules()
		modules = map(lambda mod: (mod.__name__, mod), modules)
		modules.sort()
		names = map(operator.getitem, modules, [0] * len(modules))
		self.module_list.SetList(names)
		self.modules = modules

	def do_reload(self):
		index = self.module_list.curselection()
		index = string.atoi(index[0])

		pdebug(None, 'reloading', self.modules[index])
		try:
			reload(self.modules[index][1])
		except:
			warn_tb(INTERNAL)
