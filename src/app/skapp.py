# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2002 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import sys

from app.events.warn import pdebug
from app import _, config, Publisher
from app.plugins import plugins
import app
from app.Graphics import document

from app.conf.const import CLIPBOARD

from Tkinter import Tk, TclError, PhotoImage, Wm, StringVar, DoubleVar
from app.UI import tkext
from types import ListType

from app.UI import tooltips

from app.UI import skpixmaps
pixmaps = skpixmaps.PixmapTk

#
# meta info defaults
#
meta_defaults = [
	('fullpathname', None),		# the full pathname if read from a file
	('filename', 'unnamed.sk1'),		# filename without dir
	('directory', None),		# the directory
	('backup_created', 0),		# true if a backup has been created
	('format_name', plugins.NativeFormat),# the filetype (do we need this ?)
	('native_format', 1),		# whether the file was in native format
	('ps_directory', None),		# dir where PostScript file was created
	('ps_filename', ''),		# name of last postscript file
	('compressed', ''),			# was compressed (by gzip or bzip2)
	('compressed_file', ''),		# filename of compressed file
	('load_messages', ''),		# (warning) messages
	]

for key, val in meta_defaults:
	if not hasattr(document.MetaInfo, key):
		setattr(document.MetaInfo, key, val)

#
#	Application classes
#

class TkApplication:

	# these are passed to Tk() and must be redefined by the subclasses:
	tk_basename = ''
	tk_class_name = ''

	def __init__(self, screen_name = None, geometry = None):
		self.init_tk(screen_name, geometry)

	def init_tk(self, screen_name = None, geometry = None):
		self.root = Tk(screenName = screen_name, baseName = self.tk_basename, className = self.tk_class_name)
		app.root=self.root
		
		
		from app.managers.uimanager import  UIManager
		app.uimanager=UIManager(self.root)
		
		from app.managers.dialogmanager import DialogManager
		app.dialogman=DialogManager(self.root)
		
		
		app.info1=StringVar(self.root,'')
		app.info2=StringVar(self.root,'')
		app.info3=DoubleVar(self.root,0)
		
		# Reset locale again to make sure we get properly translated
		# messages if desired by the user. For some reason it may
		# have been reset by Tcl/Tk.
		# if this fails it will already have failed in
		# app/__init__.py which also prints a warning.
		try:
			import locale
		except ImportError:
			pass
		else:
			try:
				locale.setlocale(locale.LC_MESSAGES, "")
			except:
				pass

		if not geometry:
			# try to read geometry from resource database
			geometry = self.root.option_get('geometry', 'Geometry')
		if geometry:
			try:
				self.root.geometry(geometry)
			except TclError:
				sys.stderr.write('%s: invalid geometry specification %s' % (self.tk_basename, geometry))

	def Mainloop(self):
		self.root.mainloop()

	def MessageBox(self, *args, **kw):
		return apply(tkext.MessageDialog, (self.root,) + args, kw)

	def GetOpenFilename(self, **kwargs):
		return apply(tkext.GetOpenFilename, (self.root,), kwargs)

	def GetSaveFilename(self, **kwargs):
		return apply(tkext.GetSaveFilename, (self.root,), kwargs)

	clipboard = None

	def EmptyClipboard(self):
		self.SetClipboard(None)

	def SetClipboard(self, data):
		self.clipboard = data

	def GetClipboard(self):
		return self.clipboard

	def ClipboardContainsData(self):
		return self.clipboard is not None


class ClipboardWrapper:

	def __init__(self, object):
		self.object = object

	def __del__(self):
		pdebug('__del__', '__del__', self)
		if type(self.object) == ListType:
			for obj in self.object:
				obj.Destroy()
		else:
			self.object.Destroy()

	def Object(self):
		return self.object


class SketchApplication(TkApplication, Publisher):

	tk_basename = 'sk1'
	tk_class_name = 'sK1'

	def __init__(self, filename, screen_name = None, geometry = None,
					run_script = None):
		self.filename = filename
		self.run_script = run_script
		TkApplication.__init__(self, screen_name = screen_name, geometry = geometry)
		self.build_window()

	def issue_clipboard(self):
		self.issue(CLIPBOARD)

	def SetClipboard(self, data):
		if data is not None:
			data = ClipboardWrapper(data)
		TkApplication.SetClipboard(self, data)
		self.issue_clipboard()

	def AskUser(self, title, message):
		return self.MessageBox(title = title, message = message, buttons = tkext.YesNo) == tkext.Yes

	def Run(self):
		self.SetClipboard(None)
		tooltips.Init(self.root, config.preferences.tooltip_delay, config.preferences.activate_tooltips)
		self.main_window.UpdateCommands()
		# Enter Main Loop
		self.main_window.Run()
		
	def Refresh(self):
		self.main_window.canvas.commands.FitPageToWindow

	def Exit(self):
		pixmaps.clear_cache()
		self.root.destroy()

	def init_tk(self, screen_name = None, geometry = None):
		TkApplication.init_tk(self, screen_name = screen_name, geometry = geometry)
		root = self.root
		app.init_modules_from_widget(root)
		app.uimanager.setApplicationIcon()
		app.uimanager.maximizeApp()
		root.group(root)
		config.add_options(root)

	def build_window(self):
		from app.UI.mainwindow import sK1MainWindow
		self.main_window = sK1MainWindow(self, self.filename, self.run_script)
		app.mw = self.main_window


	def SavePreferences(self, *args):
		config.save_user_preferences()

