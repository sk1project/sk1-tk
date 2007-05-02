# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2002 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import os

from sketchdlg import SketchPanel
from Tkinter import BOTH, LEFT, TOP, X
from Tkinter import Frame, Label, IntVar, StringVar, Radiobutton, Checkbutton
from tkext import UpdatedButton, MyEntry

from view import SketchView
from app import skapp

from app import _, config
from app.utils import os_utils
from app.events.warn import warn_tb, INTERNAL
import app

import skpixmaps
pixmaps = skpixmaps.PixmapTk

class PrintPanel(SketchPanel):

	title = _("Print")

	def __init__(self, master, main_window, doc):
		SketchPanel.__init__(self, master, main_window, doc, name = 'printdlg')

	def build_dlg(self):
		top = self.top

		# The preview widget
		self.view = SketchView(top, self.document, width = 200, height = 200,
								background = 'white')
		self.view.pack(side = TOP, fill = BOTH, expand = 1)

		# PostScript Options
		frame = Frame(top, name = "options")
		frame.pack(side = TOP, fill = X)
		#	EPS
		#self.var_create_eps = IntVar(top)
		#self.var_create_eps.set(1)
		#button = Checkbutton(frame, text = _("Create EPS file"),
		#		      variable = self.var_create_eps)
		#button.pack(side = LEFT, expand = 1, fill = X)
		#	Rotate
		self.var_rotate = IntVar(top)
		self.var_rotate.set(0)
		button = Checkbutton(frame, text = _("Rotate ccw."),
								variable = self.var_rotate)
		button.pack(side = LEFT, expand = 1, fill = X)


		# Print Command and Filename
		frame = Frame(top, name = "command")
		frame.pack(side = TOP)
		self.print_dest = StringVar(top)
		button = Radiobutton(frame, text = _("Printer"), value = 'printer',
								variable = self.print_dest, anchor = 'w')
		button.grid(column = 0,row = 0, sticky = 'ew')
		label = Label(frame, text = _("Command"), anchor = 'e')
		label.grid(column = 1, row = 0, sticky = 'ew')
		self.print_command = StringVar(top)
		self.print_command.set('lpr')
		entry = MyEntry(frame, textvariable = self.print_command)
		entry.grid(column = 2, row = 0, sticky = 'ew')

		button = Radiobutton(frame, text = _("EPS"), value = 'file',
								variable = self.print_dest, anchor = 'w')
		button.grid(column = 0, row = 1, sticky = 'ew')
		label = Label(frame, text = _("Filename"), anchor = 'e')
		label.grid(column = 1, row = 1, sticky = 'ew')
		self.print_filename = StringVar(top)
		self.print_filename.set('')
		entry = MyEntry(frame, textvariable = self.print_filename)
		entry.grid(column = 2, row = 1, sticky = 'ew')
		button = UpdatedButton(frame, text = _("..."),
								command = self.get_filename)
		button.grid(column = 3, row = 1, sticky = 'ew')

		frame = Frame(top)
		frame.pack(side = TOP)
		button = UpdatedButton(frame, text = _("Print"),
								command = self.do_print)
		button.pack(side = LEFT)
		button = UpdatedButton(frame, text = _("Close"),
								command = self.close_dlg)
		button.pack(side = LEFT)

		# init vars
		self.print_dest.set(config.preferences.print_destination)

	def init_from_doc(self):
		self.view.SetDocument(self.document)
		self.print_filename.set(self.default_filename())

	def get_filename(self):
		app = self.main_window.application
		dir, name = os.path.split(self.print_filename.get())
		if not dir:
			dir = self.document.meta.ps_directory
			if not dir:
				dir = config.preferences.print_dir
		filename = app.GetSaveFilename(title = _("Save As PostScript"),
										filetypes = skapp.psfiletypes,
										initialdir = dir,
										initialfile = name)
		self.print_filename.set(filename)

	def default_filename(self):
		dir = self.document.meta.ps_directory
		if not dir:
			dir = self.document.meta.directory
		if not dir:
			dir = os.getcwd()

		name = self.document.meta.filename
		name, ext = os.path.splitext(name)
		return os.path.join(dir, name + '.ps')


	def do_print(self):
		app = self.main_window.application
		bbox = self.document.BoundingRect(visible = 0, printable = 1)
		if bbox is None:
			app.MessageBox(title = _("Save As PostScript"),
							message = _("\nThe document doesn't have \n"
										"any printable layers.\n"),
							icon = pixmaps.Warning, icon1=pixmaps.smallicon)
			return
		try:
			filename = ''
			file = None
			if self.print_dest.get() == 'file':
				# print to file
				filename = self.print_filename.get()
				# use filename as file just in case the user is trying
				# to save into an EPS that is referenced by the
				# document. The psdevice knows how to handle such cases.
				file = filename
				title = os.path.basename(filename)
			else:
				file = os.popen(self.print_command.get(), 'w')
				title = 'sK1'
			try:
				dev = app.PostScriptDevice
				ps_dev = dev(file, as_eps = 1, bounding_box = tuple(bbox),
								rotate = self.var_rotate.get(),
								For = os_utils.get_real_username(),
								CreationDate = os_utils.current_date(), Title = title,
								document = self.document)
				self.document.Draw(ps_dev)
				ps_dev.Close()
				if filename:
					self.document.meta.ps_filename = filename
					self.document.meta.ps_directory =os.path.split(filename)[0]
			finally:
				# close the file. Check for the close attribute first
				# because file can be either a string or a file object.
				if hasattr(file, "close"):
					file.close()

		except IOError, value:
			app.MessageBox(title = _("Save As PostScript"),
							message = _("\nCannot save %(filename)s:\n"
										"%(message)s\n") \
							% {'filename':`os.path.split(filename)[1]`,
								'message':value[1]},
							icon = pixmaps.Warning, icon1=pixmaps.smallicon)
			return
		except:
			warn_tb(INTERNAL, 'printing to %s', file)
