# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import os, sys, string
from types import TupleType, ListType

from app.utils import os_utils
from app.events.warn import warn, warn_tb, INTERNAL, USER
from app import _, config, sKVersion
from app.plugins import plugins
from app.io import load
from app.conf import const
from app.utils import locale_utils
from app import Publisher, Point, EmptyFillStyle, EmptyLineStyle, dialogman, \
		EmptyPattern, Document, GuideLine, PostScriptDevice, SketchError, PolyBezier, CreatePath, Polar
import app
from app.Graphics import image, eps
import app.Scripting
from app.Graphics.color import rgb_to_tk

from app.conf.const import DOCUMENT, CLIPBOARD, CLOSED, COLOR1, COLOR2
from app.conf.const import STATE, VIEW, MODE, CHANGED, SELECTION, POSITION, UNDO, EDITED, CURRENTINFO

from Tkinter import TclVersion, TkVersion, Frame, Scrollbar, Label, SW, StringVar
from Tkinter import X, BOTTOM, BOTH, TOP, HORIZONTAL, LEFT, Y, RIGHT
from Ttk import  TFrame, TScrollbar, TLabel, TButton
import Tkinter
from tkext import AppendMenu, UpdatedLabel, UpdatedButton, CommandButton, ToolbarButton, \
				CommandCheckbutton, MakeCommand, MultiButton, \
			UpdatedRadiobutton, UpdatedCheckbutton, ToolsButton, ToolsCheckbutton, ToolbarCheckbutton, \
			UpdatedTButton
import tkext
from context import ctxPanel

from command import CommandClass, Keymap, Commands
from math import floor, ceil

from canvas import SketchCanvas
from ExportR import export_raster_more_interactive
import tkruler
from poslabel import PositionLabel
import palette, tooltips

import math, pathutils

import skpixmaps
pixmaps = skpixmaps.PixmapTk

from app import skapp


EXPORT_MODE=2
SAVE_AS_MODE=1
SAVE_MODE=0

command_list = []

def AddCmd(name, menu_name, method_name = None, **kw):
	kw['menu_name'] = menu_name
	if not method_name:
		method_name = name
	cmd = apply(CommandClass, (name, method_name), kw)
	command_list.append(cmd)

def AddDocCmd(name, menu_name, method_name = None, **kw):
	kw['menu_name'] = menu_name
	if not method_name:
		method_name = name
	method_name = ('document', method_name)
	for key in CommandClass.callable_attributes:
		if kw.has_key(key):
			value = kw[key]
			if type(value) == type(""):
				kw[key] = ('document', value)
	if not kw.has_key('subscribe_to'):
		kw['subscribe_to'] = SELECTION
	if not kw.has_key('sensitive_cb'):
		kw['sensitive_cb'] = ('document', 'HasSelection')
	cmd = apply(CommandClass, (name, method_name), kw)
	command_list.append(cmd)


class SketchMainWindow(Publisher):

	tk_basename = 'sk1'
	tk_class_name = 'sK1'

	def __init__(self, application, filename, run_script = None):    
		self.application = application
		self.counter=0
		self.root = application.root 
		self.filename = filename
		self.myWidth, self.myHeight = self.root.maxsize()       
		self.run_script = run_script
		self.canvas = None
		self.document = None
		self.commands = None
		self.NewDocument()
		self.create_commands()
		self.build_window()
		self.build_menu()
		self.build_toolbar()
		self.build_tools()
		#self.build_smartpanel()
		self.build_status_bar()
		self.__init_dlgs()
		self.document.Subscribe(SELECTION, self.refresh_buffer)
#               self.canvas.bind('<Configure>', self.autozoom)
		
##      self.bind('<Map>', self.init_size)
##      self.canvas.commands.FitPageToWindow
##      self.check_height = int(self.winfo_height())
##      self.check_width = int(self.winfo_width())

##    def init_size(self, event, root):
##       self.check_height = int(self.root.winfo_height())
##       self.check_width = int(self.root.winfo_width())
##       print self.check_width, ' x ', self.check_height

	def autozoom(self, event):
		check_height=-1*(int(self.canvas.winfo_height())-self.myHeight)/2
		self.myHeight=int(self.canvas.winfo_height())
		check_width=-1*(int(self.canvas.winfo_width())-self.myWidth)/2
		self.myWidth=int(self.canvas.winfo_width())
		self.canvas.ScrollXUnits(check_width) 
		self.counter=self.counter+1
		print check_width, '_X', self.counter,'X_', check_height
		
	def issue_document(self):
		self.issue(DOCUMENT, self.document)
		
	def refresh_buffer(self):
		if self.canvas:
			self.canvas.bitmap_buffer=None
#			self.canvas.save_bitmap_buffer()

	def create_commands(self):
		cmds = Commands()
		keymap = Keymap()
		for cmd_class in command_list:
			cmd = cmd_class.InstantiateFor(self)
			setattr(cmds, cmd.name, cmd)
			keymap.AddCommand(cmd)
		self.commands = cmds
		self.commands.Update()
		self.keymap = keymap

	def MapKeystroke(self, stroke):
		return self.keymap.MapKeystroke(stroke)

	def save_doc_if_edited(self, title = _("Save Document - sK1...       ")):
		if self.document is not None and self.document.WasEdited():
			message = _("\nFile: <%s> has been changed ! \n\nDo you want to save it?\n") % self.document.meta.filename
			result = self.application.MessageBox(title = title, message = message, buttons = tkext.SaveDSCancel)
			self.root.deiconify()
			if result == tkext.Save:
				self.SaveToFileInteractive()
			return result
		return tkext.No

	def Document(self):
		return self.document

	def SetDocument(self, document):
		channels = (SELECTION, UNDO, MODE)
		if self.canvas:		
			self.canvas.bitmap_buffer=None
		old_doc = self.document
		if old_doc is not None:
			for channel in channels:
				old_doc.Unsubscribe(channel, self.issue, channel)
		self.document = document
		for channel in channels:
			self.document.Subscribe(channel, self.issue, channel)
		if self.canvas is not None:
			self.canvas.SetDocument(document)
		self.issue_document()
		# issue_document has to be called before old_doc is destroyed,
		# because destroying it causes all connections to be deleted and
		# some dialogs (derived from SketchDlg) try to unsubscribe in
		# response to our DOCUMENT message. The connector currently
		# raises an exception in this case. Perhaps it should silently
		# ignore Unsubscribe() calls with methods that are actually not
		# subscribers (any more)
		if old_doc is not None:
			old_doc.Destroy()
			#import gc
			#del(old_doc)
			#gc.collect()
		self.set_window_title()
		self.document.Subscribe(SELECTION, self.refresh_buffer)
		if self.commands:
			self.commands.Update()
		

	AddCmd('NewDocument', _("New"), key_stroke = ('Ctrl+N', 'Ctrl+n'))
	AddCmd('OpenNewDocument', _("New Drawing Window"), image ='no_image')

	def NewDocument(self):
		if self.save_doc_if_edited(_("New Document        ")) == tkext.Cancel:
			return
		self.SetDocument(Document(create_layer = 1))

	AddCmd('LoadFromFile', _("Open..."), image = 'menu_fileopen',  key_stroke = ('Ctrl+O', 'Ctrl+o',))
	
	AddCmd('LoadMRU0', '', 'LoadFromFile', args = 0, key_stroke = 'Alt+1',
			name_cb = lambda: os.path.split(config.preferences.mru_files[0])[1])
	AddCmd('LoadMRU1', '', 'LoadFromFile', args = 1, key_stroke = 'Alt+2',
			name_cb = lambda: os.path.split(config.preferences.mru_files[1])[1])
	AddCmd('LoadMRU2', '', 'LoadFromFile', args = 2, key_stroke = 'Alt+3',
			name_cb = lambda: os.path.split(config.preferences.mru_files[2])[1])
	AddCmd('LoadMRU3', '', 'LoadFromFile', args = 3, key_stroke = 'Alt+4',
			name_cb = lambda: os.path.split(config.preferences.mru_files[3])[1])

	def LoadFromFile(self, filename = None, directory = None):
		self.root.update()
		app = self.application
		if self.save_doc_if_edited(_("Open Document        ")) == tkext.Cancel:
			return
		if type(filename) == type(0):
			filename = config.preferences.mru_files[filename]
		if not filename:
			if not directory:
				directory = self.document.meta.directory
			if not directory:
				directory = config.preferences.dir_for_open
			if directory=='~':
				directory=os_utils.gethome()
			if not os.path.isdir(directory):
				directory=os_utils.gethome()
			filename, sysfilename=dialogman.getOpenFilename(initialdir = directory, initialfile = filename)							
			if filename=='':
				return
		try:
			if not os.path.isabs(filename):
				filename = os.path.join(os.getcwd(), filename)
			config.preferences.dir_for_open=os.path.dirname(filename)	
			doc = load.load_drawing(filename)
			self.SetDocument(doc)
			self.add_mru_file(filename)
			self.canvas.bitmap_buffer=None			
			self.canvas.commands.ForceRedraw
		except SketchError, value:
			app.MessageBox(title = _("Open"), message = _("\nAn error occurred:\n\n") + str(value))
			self.remove_mru_file(filename)
		else:
			messages = doc.meta.load_messages
			if messages:
				app.MessageBox(title = _("Open"), message=_("\nWarnings from the import filter:\n\n")+ messages)
			doc.meta.load_messages = ''

	AddCmd('SaveToFile', _("Save"), 'SaveToFileInteractive', subscribe_to = UNDO,
				sensitive_cb = ('document', 'WasEdited'),  #bitmap = pixmaps.Save, 
				key_stroke = ('Ctrl+S', 'Ctrl+s'))
	AddCmd('SaveToFileAs', _("Save As..."), 'SaveToFileInteractive', #bitmap = pixmaps.SaveAs,
		   args = 1)
	AddCmd('ExportAs', _("Export As..."), 'SaveToFileInteractive', #bitmap = pixmaps.ExportV,
		   args = 2)

	def SaveToFileInteractive(self, use_dialog = SAVE_MODE):
		filename =  self.document.meta.fullpathname
		native_format = self.document.meta.native_format
		compressed_file = self.document.meta.compressed_file
		compressed = self.document.meta.compressed
		app = self.application
		if use_dialog or not filename or not native_format:
			directory = self.document.meta.directory
			
			if not directory:
				if use_dialog==SAVE_AS_MODE or use_dialog==SAVE_MODE:
					directory= config.preferences.dir_for_save
				if use_dialog==EXPORT_MODE:
					directory=config.preferences.dir_for_vector_export
							
			if directory=='~':
				directory=os_utils.gethome()
			if not os.path.isdir(directory):
				directory=os_utils.gethome()
				
			if use_dialog==SAVE_MODE:
				filename, sysfilename=dialogman.getSaveFilename(initialdir = directory, initialfile = filename)			
			if use_dialog==SAVE_AS_MODE:
				filename, sysfilename=dialogman.getSaveAsFilename(initialdir = directory, initialfile = filename)
			if use_dialog==EXPORT_MODE:
				filename, sysfilename=dialogman.getExportFilename(initialdir = directory, initialfile = filename)	

			if not filename:
				return
			extension = os.path.splitext(filename)[1]
			fileformat = plugins.guess_export_plugin(extension)
			if not fileformat:
				fileformat = plugins.NativeFormat
			compressed_file = '' # guess compression from filename
			compressed = ''
		else:
			fileformat = plugins.NativeFormat
		if use_dialog==SAVE_AS_MODE:
			config.preferences.dir_for_save=os.path.dirname(filename)	
		if use_dialog==EXPORT_MODE:
			config.preferences.dir_for_vector_export=os.path.dirname(filename)				
		self.SaveToFile(filename, fileformat, compressed, compressed_file)

	def SaveToFile(self, filename, fileformat = None, compressed = '', compressed_file = ''):
		sysname=locale_utils.utf_to_locale(filename)
		app = self.application
		try:
			if not self.document.meta.backup_created:
				try:
					if compressed_file:
						os_utils.make_backup(compressed_file)
					else:
						os_utils.make_backup(sysname)
				except os_utils.BackupError, value:
					backupfile = locale_utils.utf_to_locale(value.filename)
					strerror = value.strerror
					msg = (_("\nCannot create backup file %(filename)s:\n"
								"%(message)s\n\n"
								"Choose `continue' to try saving anyway,\n"
								"or `cancel' to cancel saving.")
							% {'filename':`backupfile`, 'message':strerror})
					cancel = _("Cancel")
					result = app.MessageBox(title = _("Save To File"), message = msg, buttons = (_("Continue"), cancel))
					if result == cancel:
						return

				self.document.meta.backup_created = 1
			if fileformat is None:
				fileformat = plugins.NativeFormat
			try:
				saver = plugins.find_export_plugin(fileformat)
				if compressed:
					# XXX there should be a plugin interface for this kind
					# of post-processing
					if compressed == "gzip":
						cmd = 'gzip -c -9 > ' + os_utils.sh_quote(compressed_file)
					elif compressed == "bzip2":
						cmd = 'bzip2 > ' + os_utils.sh_quote(compressed_file)
					file = os.popen(cmd, 'w')
					saver(self.document, filename, file = file)
				else:
					saver(self.document, sysname)
			finally:
				saver.UnloadPlugin()
		except IOError, value:
			if type(value) == type(()):
				value = value[1]
			app.MessageBox(title = _("Save To File"),
							message = _("\nCannot save %(filename)s:\n\n"
										"%(message)s") \
							% {'filename':`os.path.split(filename)[1]`,
								'message':value})
			self.remove_mru_file(filename)
			return

		if fileformat == plugins.NativeFormat:
			dir, name = os.path.split(filename)
			# XXX should meta.directory be set for non-native formats as well
			self.document.meta.directory = dir
			self.document.meta.filename = name
			self.document.meta.fullpathname = filename
			self.document.meta.file_type = plugins.NativeFormat
			self.document.meta.native_format = 1
		if not compressed_file:
			self.document.meta.compressed_file = ''
			self.document.meta.compressed = ''
		if compressed_file:
			self.add_mru_file(compressed_file)
		else:
			self.add_mru_file(filename)

		self.set_window_title()

	def add_mru_file(self, filename):
		if filename:
			config.add_mru_file(filename)
			self.update_mru_files()

	def remove_mru_file(self, filename):
		if filename:
			config.remove_mru_file(filename)
			self.update_mru_files()

	def update_mru_files(self):
		self.commands.LoadMRU0.Update()
		self.commands.LoadMRU1.Update()
		self.commands.LoadMRU2.Update()
		self.commands.LoadMRU3.Update()
		self.file_menu.RebuildMenu()

	AddCmd('InsertFile', _("Import vector..."))#, bitmap = pixmaps.ImportVector)
	def InsertFile(self, filename = None):
		app = self.application
		if not filename:
			directory = config.preferences.dir_for_vector_import
			if directory=='~':
				directory=os_utils.gethome()
			if not os.path.isdir(directory):
				directory=os_utils.gethome()
			filename, sysfilename=dialogman.getImportFilename(initialdir = directory, initialfile = filename)				
			if not filename:
				return
		try:
			if not os.path.isabs(filename):
				filename = os.path.join(os.getcwd(), filename)
			doc = load.load_drawing(filename)
			group = doc.as_group()
		except SketchError, value:
			group=None
			app.MessageBox(title = _("Import vector"), message = _("\nAn error occurred:\n\n") + str(value))
			self.remove_mru_file(filename)
		else:
			messages = doc.meta.load_messages
			if messages:
				app.MessageBox(title = _("Import vector"), message=_("\nWarnings from the import filter:\n\n") + messages)
			doc.meta.load_messages = ''
		if group is not None:
			if config.preferences.import_insertion_mode:
				self.canvas.PlaceObject(group)
			else:
				self.document.Insert(group)
		else:
			app.MessageBox(title = _("Import vector"), message=_("\nThe document is empty!\n"))
		config.preferences.dir_for_vector_import=os.path.dirname(filename)


	AddCmd('LoadPalette', _("Load Palette..."))
	def LoadPalette(self, filename = None):
		if not filename:
			directory = config.user_palettes
			if not directory:
				directory = os_utils.gethome()
				
			filename, sysfilename=dialogman.getGenericOpenFilename(_("Load Palette"),
																   app.managers.dialogmanager.palette_types,
																   initialdir = directory, initialfile = filename)
			if not filename:
				return

		pal = palette.LoadPalette(filename)
		if not pal:
			self.application.MessageBox(title = _("Load Palette"),
								message = _("\nCannot load palette %(filename)s!\n") % {'filename': filename})
		else:
			self.palette.SetPalette(pal)
			config.preferences.palette = filename

	def __init_dlgs(self):
		self.dialogs = {}

	def CreateDialog(self, module, dlgname):
		if self.dialogs.has_key(dlgname):
			dialog = self.dialogs[dlgname]
			dialog.deiconify_and_raise()
		else:
			exec "from %s import %s" % (module, dlgname)
			dlgclass = locals()[dlgname]
			dialog = dlgclass(self.root, self, self.document)
			dialog.Subscribe(CLOSED, self.__dlg_closed, dlgname)
			self.dialogs[dlgname] = dialog

	def HideDialogs(self):
		for dialog in self.dialogs.values():
			dialog.withdraw()
	AddCmd('HideDialogs', _("Hide Dialogs"))

	def ShowDialogs(self):
		for dialog in self.dialogs.values():
			dialog.deiconify_and_raise()
	AddCmd('ShowDialogs', _("Show Dialogs"))

	def __dlg_closed(self, dialog, name):
		try:
			del self.dialogs[name]
		except:
			# This might happen if the dialog is buggy...
			warn(INTERNAL, 'dialog %s alread removed from dialog list', name)

	AddCmd('CreateLayerDialog', _("Layers..."), 'CreateDialog', args = ('dlg_layer', 'LayerPanel'), key_stroke = 'F5')
	AddCmd('CreateAlignDialog', _("Align to ..."), 'CreateDialog', args = ('dlg_align', 'AlignPanel'), key_stroke = ('Ctrl+A', 'Ctrl+a'))
	AddCmd('CreateGridDialog', _("Grid Setup..."), 'CreateDialog', args = ('dlg_grid', 'GridPanel'), bitmap = pixmaps.DGrid)
	AddCmd('CreateLineStyleDialog', 
		   _("Outline..."), 
		   'CreateDialog', 
		   args = ('dlg_line', 'LinePanel'), 
		   #bitmap = pixmaps.OutlineButton, 
		   key_stroke = 'F12')
	AddCmd('CreateFillStyleDialog', 
		   _("Fill..."), 'CreateDialog', 
		   args = ('filldlg', 'FillPanel'), 
		   #bitmap = pixmaps.FillButton, 
		   key_stroke = 'F11')
	AddCmd('CreateFontDialog', _("Fonts..."), 'CreateDialog', args = ('fontdlg', 'FontPanel'), key_stroke = 'Ctrl+f', bitmap = pixmaps.DText)
	AddCmd('CreateStyleDialog', _("Styles..."), 'CreateDialog', args = ('styledlg', 'StylePanel'))
	AddCmd('CreateBlendDialog', _("Blend..."), 'CreateDialog', args = ('dlg_blend', 'BlendPanel'), key_stroke = ('Ctrl+B', 'Ctrl+b'))
	AddCmd('CreateLayoutDialog', _("Page Setup..."), 'CreateDialog', args = ('dlg_layout', 'LayoutPanel'), bitmap = pixmaps.DPage)
	#AddCmd('CreateExportDialog', 'Export...', 'CreateDialog', args = ('export', 'ExportPanel'))
	AddCmd('CreateCurveDialog', _("Curve Commands..."), 'CreateDialog', args = ('dlg_curve', 'CurvePanel'), bitmap = pixmaps.DNodes)
	AddCmd('CreateGuideDialog', _("Guides Setup..."), 'CreateDialog', args = ('dlg_guide', 'GuidePanel'))
	AddCmd('KPrinting', 
		   _("Print..."), 
		   'KPrinting', 
		   #bitmap = pixmaps.Printer, 
		   key_stroke = ('Ctrl+P', 'Ctrl+p'))
	AddCmd('CreatePrintDialog', _("LPR printing..."), 'CreateDialog', args = ('printdlg', 'PrintPanel'))#, bitmap = pixmaps.QPrinter)
	AddCmd('CreateMoveDialog', _("Move..."), 'CreateDialog', args = ('dlg_move', 'MovePanel'), key_stroke = 'Alt+F9', bitmap = pixmaps.Move)
	AddCmd('CreateRotateDialog', _("Rotate..."), 'CreateDialog', args = ('dlg_rotate', 'RotatePanel'), bitmap = pixmaps.Rotate)
	AddCmd('CreateSizeDialog', _("Resize..."), 'CreateDialog', args = ('dlg_size', 'SizePanel'), bitmap = pixmaps.Size)

	AddCmd('CreateReloadPanel', _("Reload Module..."), 'CreateDialog', args = ('reloaddlg', 'ReloadPanel'))

	def KGetOpenFilename(self,title="sK1", filetypes = None, initialdir = '', initialfile = ''):
		self.root.update()
		winid=str(self.root.winfo_id())
		from_K = os.popen('kdialog --caption \''+title+'\' --embed \''+winid+'\' --getopenfilename \''+initialdir+'\''+ filetypes)
		file=from_K.readline()
		file=locale_utils.strip_line(file)
		from_K.close()
		file=locale_utils.locale_to_utf(file)
		return file

	def KGetSaveFilename(self,title="sK1", filetypes = None, initialdir = '', initialfile = ''):
		self.root.update()
		winid=str(self.root.winfo_id())
		from_K = os.popen('kdialog -caption \''+title+'\' --embed \''+winid+'\' --getsavefilename \''
		+initialdir+'\''+ filetypes)
		file=from_K.readline()
		file=locale_utils.strip_line(file)
		from_K.close()
		file=locale_utils.locale_to_utf(file)
		return file

	def KPrinting(self):
		self.root.update()
		app = self.application
		bbox = self.document.BoundingRect(visible = 0, printable = 1)
		if bbox is None:
			app.MessageBox(title = _("PostScript saving"), message = _("\nThe document doesn't have \n any printable layers!\n"))
			return
		try:
			self.canvas.commands.ForceRedraw
			filename = ''
			file = None
			title = 'sK1'
			file = os.popen('kprinter --stdin --caption sK1 --', 'w')

			try:
				dev = PostScriptDevice
				ps_dev = dev(file, as_eps = 1, bounding_box = tuple(bbox),
								rotate = 0, # page rotate?
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
			return
		except:
			warn_tb(INTERNAL, 'printing to %s', file)


	def CreatePluginDialog(self, info):
		if info.HasCustomDialog():
			dialog = info.CreateCustomDialog(self.root, self, self.document)
		else:
			from plugindlg import PluginPanel
			dialog = PluginPanel(self.root, self, self.document, info)
		dialog.Subscribe(CLOSED, self.__dlg_closed, info.class_name)
		self.dialogs[info.class_name] = dialog

	AddCmd('SetOptions', _("Options..."))
	def SetOptions(self):
		import optiondlg
		optiondlg.OptionDialog(self.root, self.canvas)

	def set_window_title(self):
		self.root.client(os_utils.gethostname())
		if self.document:
			appname = config.name
			meta = self.document.meta
			if meta.compressed:
				docname = os.path.split(meta.compressed_file)[1]
				docname = os.path.splitext(docname)[0]
			else:
				docname = self.document.meta.filename
			title = config.preferences.window_title_template % locals()
			command = (config.sk_command, self.document.meta.fullpathname)
		else:
			title = config.name
			command = (config.sk_command, )
		self.root.title(title)
		self.root.command(command)

	def UpdateCommands(self):
		self.canvas.UpdateCommands()

	def Run(self):
		if self.filename:
			if os.path.isdir(self.filename):
				filename = ''
				directory = self.filename
			else:
				filename = self.filename
				directory = ''
			self.LoadFromFile(filename, directory = directory)
			self.filename = ''
		if self.run_script:
			from app.Scripting.script import Context
			dict = {'context': Context()}
			try:
				execfile(self.run_script, dict)
			except:
				warn_tb(USER, _("Error running script `%s'"), self.run_script)

		self.application.Mainloop()

	AddCmd('Exit', _("Exit"), key_stroke = ('Alt+F4'))
	def Exit(self):
		if self.save_doc_if_edited(_("EXIT        ")) != tkext.Cancel:
			self.commands = None
			self.application.Exit()

	def build_window(self):
		root = self.application.root
		
		palette_frame = TFrame(root, style='FlatFrame', borderwidth=2)
		palette_frame.pack(side = 'right', fill = Y)
		
		b = TLabel(root, style='VLine2')
		b.pack(side = 'right', fill = Y)

		# the menu
		self.mbar = TFrame(root, name = 'menubar', style='MenuBarFrame', borderwidth=2)
		self.mbar.pack(fill=X)

		# the toolbar
		self.tbar = TFrame(root, name = 'toolbar', style='ToolBarFrame', borderwidth=2)
		self.tbar.pack(fill=X)

		# the smartpanel
		self.ctxpanel=ctxPanel.ContexPanel(root, self)
		#self.fkbar = TFrame(root, name = 'fastkeys', style='ToolBarFrame', borderwidth=0)
		self.ctxpanel.panel.pack(fill=X)


		# the status bar
		self.status_bar = TFrame(root, name = 'statusbar', style='FlatFrame' )
		self.status_bar.pack(side = BOTTOM, fill=X)
		
		# the tools bar
		self.tframe = TFrame(root, name = 'tools_frame', style='FlatFrame', borderwidth=2)
		self.tframe.pack(side = LEFT, fill=Y)
		
		####################################
		# Drawing area creating
		####################################
		frame = TFrame(root, name = 'canvas_frame', style="CanvasFrame", borderwidth=5)
		frame.pack(side = LEFT, fill = BOTH, expand = 1)

		vbar = TScrollbar(frame)
		vbar.grid(in_ = frame, column = 3, row = 1, sticky = 'ns')
		vbar.bind('<Button-4>', self.ScrollUpCanvas)
		vbar.bind('<Button-5>', self.ScrollDownCanvas)
		
		hbar = TScrollbar(frame, orient = HORIZONTAL)
		hbar.grid(in_ = frame, column = 2, row = 2, sticky = 'ew')
		hbar.bind('<Button-4>', self.ScrollLeftCanvas)
		hbar.bind('<Button-5>', self.ScrollRightCanvas)
		####################################
		#tempframe = Frame(root, name = 'temp_frame')
		
		hrule = tkruler.Ruler(frame, orient = tkruler.HORIZONTAL, 
							  bg=config.preferences.ruler_color, bd=0, highlightthickness=0, relief='flat') 
		
		hrule.grid(in_ = frame, column = 2, row = 0, sticky = 'nsew', columnspan = 2)
		hrule.bind('<Double-Button-1>', self.RulerDoublePressH)
		
		####################################

		vrule = tkruler.Ruler(frame, orient = tkruler.VERTICAL,
							  bg=config.preferences.ruler_color, bd=0, highlightthickness=0, relief='flat')
		
		vrule.grid(in_ = frame, column = 1, row = 1, sticky = 'nsew', rowspan = 2)
		vrule.bind('<Double-Button-1>', self.RulerDoublePressV)
		
		#ruler corner 
		b = TLabel(frame, style="FlatLabel", image="rulers_corner")
		#b = TButton(frame, command=self.GuideDialog, style="TCornerButton", image="icon_dlg_guides", takefocus=0)
		#b = TLabel(frame, style='FlatLabel')
		b.bind('<Button-1>', self.GuideDialog)
		tooltips.AddDescription(b, self.commands.CreateGuideDialog.menu_name)
		b.grid(column = 1, row = 0, sticky = 'news')
		#ruler corner  //
		
		resolution = config.preferences.screen_resolution
		self.canvas = SketchCanvas(root, toplevel = root, background = 'white', name = 'canvas',
				resolution = resolution, main_window = self, document = self.document)
		self.canvas.grid(in_ = frame, column = 2, row = 1, sticky = 'news')
		self.canvas.focus()
		self.canvas.SetScrollbars(hbar, vbar)
		self.canvas.SetRulers(hrule, vrule)

		vrule.SetCanvas(self.canvas)
		hrule.SetCanvas(self.canvas)

		frame.columnconfigure(0, weight = 0)
		frame.columnconfigure(1, weight = 0)
		frame.columnconfigure(2, weight = 1)
		frame.columnconfigure(3, weight = 0)
		frame.rowconfigure(0, weight = 0)
		frame.rowconfigure(1, weight = 1)
		frame.rowconfigure(2, weight = 0)
		hbar['command'] = self.canvas._w + ' xview'
		vbar['command'] = self.canvas._w + ' yview'

		# the palette

		pal = palette.GetStandardPalette()
		
		palette_trough = TFrame(palette_frame, style='FlatFrame', borderwidth=0)
		palette_container = TFrame(palette_trough, style='FlatFrame', borderwidth=0)
		
		self.palette = palette.PaletteWidget(palette_container)
		
		ScrollXUnits = self.palette.ScrollXUnits
		ScrollXPages = self.palette.ScrollXPages
		CanScrollLeft = self.palette.CanScrollLeft
		CanScrollRight = self.palette.CanScrollRight
		
		but1= UpdatedTButton(palette_frame, class_='Repeater', style='Pal2TopButton', image='pal_dbl_arrow_up',
					command = ScrollXPages, args =  -1, sensitivecb = CanScrollLeft)
		but1.pack(side = TOP)
		but2= UpdatedTButton(palette_frame, class_='Repeater', style='PalTopButton', image='pal_arrow_up',
					command = ScrollXUnits, args =  -1, sensitivecb = CanScrollLeft)
		but2.pack(side = TOP)
		
		palette_trough.pack(side = TOP, fill = Y, expand = 1)
		
		b = TLabel(palette_trough, style='PalLBorder')
		b.pack(side = LEFT, fill = Y)
		
		palette_container.pack(side = LEFT, fill = Y, expand = 1)
				
		but= UpdatedTButton(palette_container, style='PalNoColorButton', image='pal_no_color',
					command = self.no_pattern, args = 'fill', borderwidth=0)
		but.pack(side = TOP)
		but.bind('<ButtonPress-3>', self.no_pattern, 'line')
		tooltips.AddDescription(but, "No color")
		
		self.palette.pack(side = LEFT, fill = Y, expand = 1)
		
		b = TLabel(palette_trough, style='PalRBorder')
		b.pack(side = 'right', fill = Y)
		
		but3= UpdatedTButton(palette_frame, class_='Repeater', style='PalBottomButton', image='pal_arrow_down',
					command = ScrollXUnits, args =  +1, sensitivecb = CanScrollRight)
		but3.pack(side = TOP)
		but4= UpdatedTButton(palette_frame, class_='Repeater', style='Pal2BottomButton', image='pal_dbl_arrow_down',
					command = ScrollXPages, args =  +1, sensitivecb = CanScrollRight)
		but4.pack(side = TOP)

		self.palette.Subscribe(COLOR1, self.canvas.FillSolid)
		self.palette.Subscribe(COLOR2, self.canvas.LineColor)
		root.protocol('WM_DELETE_WINDOW', tkext.MakeMethodCommand(self.Exit))
		
		#Binding for mouse wheel
		self.palette.bind('<Button-4>', self.ScrollUpPallette)
		self.palette.bind('<Button-5>', self.ScrollDownPallette)
		self.canvas.bind('<Button-4>', self.ScrollUpCanvas)
		self.canvas.bind('<Button-5>', self.ScrollDownCanvas)
		self.canvas.bind('<Control-Button-4>', self.ScrollLeftCanvas)
		self.canvas.bind('<Control-Button-5>', self.ScrollRightCanvas)
		self.canvas.bind('<Shift-Button-4>', self.CanvasZoomingOut)
		self.canvas.bind('<Shift-Button-5>', self.CanvasZoomingIn)

	def make_file_menu(self):
		cmds = self.commands
		return map(MakeCommand,
					[cmds.NewDocument,
					cmds.LoadFromFile,
					None,
					cmds.SaveToFile,
					cmds.SaveToFileAs,
					None,
					cmds.CreateImage,
					cmds.InsertFile,
					cmds.ExportAs,
					cmds.ExportRaster, #cmds.SavePS,
					#cmds.export_bitmap,
					None,
					cmds.KPrinting,
					cmds.CreatePrintDialog,
					None,
					#cmds.CreateExportDialog,
					#None,
					cmds.SetOptions,
					None,
					cmds.DocumentInfo,
					None,
					cmds.LoadMRU0,
					cmds.LoadMRU1,
					cmds.LoadMRU2,
					cmds.LoadMRU3,
					None,
					cmds.Exit])

	def make_edit_menu(self):
		cmds = self.canvas.commands
		return map(MakeCommand,
					[self.commands.Undo,
					self.commands.Redo,
					self.commands.ResetUndo,
					None,
					self.commands.CutSelected,
					self.commands.CopySelected,
					self.commands.PasteClipboard,
					None,
					self.commands.RemoveSelected,
					self.commands.CopyPaste,
					self.commands.DuplicateSelected,
					self.commands.SelectAll,
#                                       None,
#                                       [(_("Create"), {'auto_rebuild':self.creation_entries}),
#                                               []],
					None,
					cmds.SelectionMode,
					cmds.EditMode,
					])

	def creation_entries(self):
		cmds = self.canvas.commands
		entries = [cmds.CreateRectangle,
					cmds.CreateEllipse,
					cmds.CreatePolyBezier,
					cmds.CreatePolyLine,
					cmds.CreateSimpleText,
					self.commands.CreateImage,
					None]
		items = plugins.object_plugins.items()
		items.sort()
		place = self.place_plugin_object
		dialog = self.CreatePluginDialog
		group = self.create_plugin_group
		for name, plugin in items:
			if plugin.UsesSelection():
				entries.append((plugin.menu_text, group, plugin))
			elif plugin.HasParameters() or plugin.HasCustomDialog():
				entries.append((plugin.menu_text + '...', dialog, plugin))
			else:
				entries.append((plugin.menu_text, place, plugin))
		return map(MakeCommand, entries)

	def place_plugin_object(self, info):
		self.canvas.PlaceObject(info())

	def create_plugin_group(self, info):
		self.document.group_selected(info.menu_text, info.CallFactory)

	def PlaceObject(self, object):
		self.canvas.PlaceObject(object)

	def make_effects_menu(self):
		return map(MakeCommand,
					[self.commands.CreateMoveDialog,
					self.commands.CreateSizeDialog,
					self.commands.CreateRotateDialog,
					None,
					self.commands.FlipHorizontal,
					self.commands.FlipVertical,
					None,
					self.commands.RemoveTransformation,
					None,
					self.commands.CreateBlendDialog,
					self.commands.CancelBlend,
					None,
					self.commands.CreateMaskGroup,
					self.commands.CreatePathText
					])


	def make_curve_menu(self):
		canvas = self.canvas
		cmds = self.canvas.commands.PolyBezierEditor
		return map(MakeCommand,
					[cmds.ContAngle,
					cmds.ContSmooth,
					cmds.ContSymmetrical,
					cmds.SegmentsToLines,
					cmds.SegmentsToCurve,
					cmds.SelectAllNodes,
					None,
					cmds.DeleteNodes,
					cmds.InsertNodes,
					None,
					cmds.CloseNodes,
					cmds.OpenNodes,
					None,
					self.commands.CombineBeziers,
					self.commands.SplitBeziers,
					None,
					self.commands.ConvertToCurve])

	def make_view_menu(self):
		def MakeEntry(scale, call = self.canvas.SetScale):
			percent = int(100 * scale)
			return (('%3d%%' % percent), call, scale)
		def Make11(scale, call = self.canvas.SetScale):
			percent = int(100 * scale)
			return (("Zoom 1:1"), call, scale)
		cmds = self.canvas.commands
		scale = map(MakeEntry, [ 0.125, 0.25, 0.5, 1, 2, 4, 8])
		return map(MakeCommand,
					[Make11(1.16),
					[_("Zoom")] + scale,
					cmds.ZoomIn,
					cmds.ZoomOut,
					cmds.ZoomMode,
					None,
					cmds.FitToWindow,
					cmds.FitSelectedToWindow,
					cmds.FitPageToWindow,
					cmds.RestoreViewport,
					None,
					cmds.ForceRedraw,
					None,
					cmds.ToggleOutlineMode,
					cmds.TogglePageOutlineMode,
					None,
					cmds.ToggleCrosshairs,
					None,
					self.commands.LoadPalette
					])

	def make_layout_menu(self):
		return map(MakeCommand,
					[self.commands.CreateLayoutDialog,
					None,
					self.commands.CreateGridDialog,
					self.commands.CreateGuideDialog,
					None,
					self.commands.AddHorizGuideLine,
					self.commands.AddVertGuideLine,
					None,
					self.canvas.commands.ToggleSnapToGrid,
					self.canvas.commands.ToggleSnapToGuides,
					self.canvas.commands.ToggleSnapToObjects
					#None,
					#self.canvas.commands.ToggleSnapMoveRelative,
					#self.canvas.commands.ToggleSnapBoundingRect
					])

	def make_arrange_menu(self):
		commands = [self.commands.CreateAlignDialog,
					None,
					self.commands.MoveSelectedToTop,
					self.commands.MoveSelectedToBottom,
					self.commands.MoveSelectionUp,
					self.commands.MoveSelectionDown,
					None,
					self.commands.AbutHorizontal,
					self.commands.AbutVertical,
					None,
					self.commands.GroupSelected,
					self.commands.UngroupSelected
					]
		if config.preferences.show_advanced_snap_commands:
			commands.append(None)
			commands.append(self.canvas.commands.ToggleSnapMoveRelative)
			commands.append(self.canvas.commands.ToggleSnapBoundingRect)
		#commands = commands + [None,
			#                     self.commands.CreateLayoutDialog
			#                    ]
		return map(MakeCommand, commands)

	def make_style_menu(self):
		return map(MakeCommand,
					[self.commands.FillNone,
					self.commands.CreateFillStyleDialog,
					self.canvas.commands.FillSolid,
					None,
					self.commands.LineNone,
					self.commands.CreateLineStyleDialog,
					None,
					self.commands.CreateStyleFromSelection,
					self.commands.CreateStyleDialog,
					self.commands.UpdateStyle# ,
#                                       None,
#                                       self.commands.CreateFontDialog
					])

	def make_window_menu(self):
		cmds = self.commands
		return map(MakeCommand,
					[cmds.HideDialogs,
					cmds.ShowDialogs,
					None,
					cmds.CreateLayerDialog,
					cmds.CreateAlignDialog,
					cmds.CreateGridDialog,
					None,
					cmds.CreateLineStyleDialog,
					cmds.CreateFillStyleDialog,
					cmds.CreateFontDialog,
					cmds.CreateStyleDialog,
					None,
					cmds.CreateLayoutDialog,
					None,
					cmds.CreateBlendDialog,
					cmds.CreateCurveDialog
					])

	def make_help_menu(self):
		return map(MakeCommand,
					[self.commands.AboutBox
					])


	def make_special_menu(self):
		cmdlist = [self.commands.python_prompt,
					self.commands.CreateReloadPanel,
					self.commands.DocumentInfo,
					None,
					self.commands.DumpXImage,
					self.commands.CreateClone,
					#self.commands.export_bitmap,
					]
		app.Issue(None, const.ADD_TO_SPECIAL_MENU, cmdlist)
		return map(MakeCommand, cmdlist)

	def make_script_menu(self):
		tree = app.Scripting.Registry.MenuTree()
		cmdlist = self.convert_menu_tree(tree)
		return map(MakeCommand, cmdlist)


	def convert_menu_tree(self, tree):
		result = []
		for title, item in tree:
			if type(item) == ListType:
				result.append([title] + self.convert_menu_tree(item))
			else:
				result.append((title, item.Execute))
		return result

	def build_Xmenu(self):
		root=self.root
		bar=Tkinter.Menu(root,)
		filem=Tkinter.Menu(bar)
		filem.add_command(label="Test",command = self.MenuOne)
		bar.add_cascade(label="Test", menu=filem)
		root.config(menu=bar)
		mbar = self.mbar
		canvas = self.canvas
		b = UpdatedCheckbutton(mbar,  text= 'File', borderwidth=0, highlightthickness = 0, indicatoron = 0, selectcolor = '',
											underline=0, width = 4, bd=0, bg='#D9E2EA', activebackground='white', #activeforeground='white',
											command = self.MenuOne)
		b.pack(side = LEFT,  fill=Y)
		b = UpdatedCheckbutton(mbar, text= 'Edit', borderwidth=0, highlightthickness = 0, indicatoron = 0, selectcolor = '',
											underline=0, width = 4, bd=0, bg='#D9E2EA', activebackground='white', #activeforeground='white',
											command = self.HideMenu)
		b.pack(side = LEFT,  fill=Y)
		b = UpdatedCheckbutton(mbar, text= 'View', borderwidth=0, highlightthickness = 0, indicatoron = 0, selectcolor = '',
											underline=0, width = 5, bd=0, bg='#D9E2EA', activebackground='white', #activeforeground='white',
											command = self.Spacer)
		b.pack(side = LEFT,  fill=Y)
		
	def HideMenu(self):
		menu1.withdraw()

	def build_menu(self):
		mbar = self.mbar
		self.file_menu = AppendMenu(mbar, _("File"), self.make_file_menu(), 0)
		AppendMenu(mbar, _("Edit"), self.make_edit_menu(), 0)
		AppendMenu(mbar, _("View"), self.make_view_menu(), 0)
		AppendMenu(mbar, _("Layout"), self.make_layout_menu(), 0)
		AppendMenu(mbar, _("Arrange"), self.make_arrange_menu(), 0)
		AppendMenu(mbar, _("Effects"), self.make_effects_menu(), 4)
		AppendMenu(mbar, _("Curve"), self.make_curve_menu(), 1)
		AppendMenu(mbar, _("Style"), self.make_style_menu(), 1)
		AppendMenu(mbar, _("Script"), self.make_script_menu(), 0)
		AppendMenu(mbar, _("Windows"), self.make_window_menu(), 0)
		AppendMenu(mbar, _("Help"), self.make_help_menu(), 0 )

		if config.preferences.show_special_menu:
			AppendMenu(mbar, _("Special"), self.make_special_menu())
		self.update_mru_files()
		self.file_menu.RebuildMenu()

	def build_smartpanel(self):
		fkbar = self.fkbar
		canvas = self.canvas
		
		label = TLabel(fkbar, image = "toolbar_left")
		label.pack(side = LEFT)

		#Page Info Container
		sb2f = Frame(fkbar, relief='sunken', borderwidth=1)
		sb2f.pack(side = LEFT)
		sb2 = Frame(sb2f, relief='flat', bg='#8B898B', borderwidth=1)
		sb2.pack(side = LEFT, fill=BOTH)
		#Page Info
		stat_mode = UpdatedLabel(sb2, name = 'mode', text = '', updatecb = canvas.PageInfoText, style='SmallFlatLabel', border=0)
		stat_mode.pack(side = 'left', expand = 1)
		stat_mode.Update()
		canvas.Subscribe(POSITION, stat_mode.Update)
		b = CommandButton(sb2f, self.commands.CreateLayoutDialog)
		b.pack(side = RIGHT, fill = Y)

		bitmap1 = pixmaps.load_image(pixmaps.Sizes)
		label = Label(fkbar, image = bitmap1, borderwidth=0)
		label.pack(side = LEFT)


		b = CommandButton(fkbar, self.commands.CreateCurveDialog)
		b.pack(side = LEFT)
		self.cbar2 = Frame(fkbar, name = 'cbar2' )
		self.cbar2.pack(side = LEFT, fill=Y)
		b = CommandButton(self.cbar2, self.commands.CombineBeziers)
		b.pack(side = TOP)
		b = CommandButton(self.cbar2, self.commands.SplitBeziers)
		b.pack(side = TOP)

		self.cbar3 = Frame(fkbar, name = 'cbar3' )
		self.cbar3.pack(side = LEFT, fill=Y)
		b = CommandButton(self.cbar3, self.commands.GroupSelected)
		b.pack(side = TOP)
		b = CommandButton(self.cbar3, self.commands.UngroupSelected)
		b.pack(side = TOP)

		b = CommandButton(fkbar, self.commands.UngrAll)
		b.pack(side = LEFT)


		b = CommandButton(fkbar, self.commands.CreateFontDialog)
		b.pack(side = LEFT)


		b = CommandButton(fkbar, self.commands.ConvertToCurve)
		b.pack(side = LEFT)


	def build_tools(self):
		tframe = self.tframe
		canvas = self.canvas
		
		fr=TFrame(tframe, style='FlatFrame', borderwidth=12)
		fr.pack(side = TOP, fill = X)
		label = TLabel(fr, style='FlatLabel')
		label.pack(side = TOP, fill = X)
		
		label = TLabel(tframe, style='HLine')
		label.pack(side = TOP, fill = X)

		#Selection Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.SelectionMode, image='tools_pointer')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.SelectionMode.menu_name)
		#CurveEdit Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.EditMode, image='tools_shaper')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.EditMode.menu_name)
		#Zoom Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.ZoomMode, image='tools_zoom')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.ZoomMode.menu_name)

		#PolyLine Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.CreatePolyLine, image='tools_pencil_line')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.CreatePolyLine.menu_name)
		#PolyBezier Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.CreatePolyBezier, image='tools_pencil_curve')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.CreatePolyBezier.menu_name)

		#Ellipse Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.CreateEllipse, image='tools_ellipse')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.CreateEllipse.menu_name)
		
		#Rectangle Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.CreateRectangle, image='tools_rectangle')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.CreateRectangle.menu_name)

		#SimpleText Mode Button
		b = ToolsCheckbutton(tframe, canvas.commands.CreateSimpleText, image='tools_text')
		b.pack(side = TOP)
		tooltips.AddDescription(b, canvas.commands.CreateSimpleText.menu_name)

		b = TLabel(tframe, style='HLine')
		b.pack(side = TOP, fill = X)

		#Outline Button
		b = ToolsButton(tframe, self.commands.CreateLineStyleDialog, image='tools_color_line')
		b.pack(side = TOP)
		tooltips.AddDescription(b, self.commands.CreateLineStyleDialog.menu_name)

		#Fill Button
		b = ToolsButton(tframe, self.commands.CreateFillStyleDialog, image='tools_color_fill')
		b.pack(side = TOP)
		tooltips.AddDescription(b, self.commands.CreateFillStyleDialog.menu_name)
		#Spacer
		b = TLabel(tframe, style='HLine')
		b.pack(side = TOP, fill = X)

		b = TLabel(tframe, style='HLine')
		b.pack(side = BOTTOM, fill = X)
		
		b = ToolbarButton(tframe, self.commands.MoveSelectedToBottom, image='tools_lower')
		b.pack(side =  BOTTOM, fill= X)
		b = ToolbarButton(tframe, self.commands.MoveSelectionDown, image='tools_backward')
		b.pack(side = BOTTOM, fill= X)
		b = ToolbarButton(tframe, self.commands.MoveSelectionUp, image='tools_forward')
		b.pack(side = BOTTOM, fill= X)
		b = ToolbarButton(tframe, self.commands.MoveSelectedToTop, image='tools_raise')
		b.pack(side =  BOTTOM, fill= X)

	def build_toolbar(self):
		tbar = self.tbar
		canvas = self.canvas
		commands = self.commands
		
		label = TLabel(tbar, image = "toolbar_left")
		label.pack(side = LEFT)

		b = ToolbarButton(tbar, commands.NewDocument, image = "toolbar_new")
		tooltips.AddDescription(b, commands.NewDocument.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.LoadFromFile, image="toolbar_open")
		tooltips.AddDescription(b, commands.LoadFromFile.menu_name)
		b.pack(side = LEFT)
		
		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)
		
		b = ToolbarButton(tbar, commands.SaveToFile, image="toolbar_save")
		tooltips.AddDescription(b, commands.SaveToFile.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.SaveToFileAs, image="toolbar_saveas")
		tooltips.AddDescription(b, commands.SaveToFileAs.menu_name)
		b.pack(side = LEFT)
		
		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)
		
		b = ToolbarButton(tbar, commands.KPrinting, image="toolbar_print")
		tooltips.AddDescription(b, commands.KPrinting.menu_name)
		b.pack(side = LEFT)

		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)

		b = ToolbarButton(tbar, commands.Undo, image="toolbar_undo")
		tooltips.AddDescription(b, commands.Undo.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.Redo, image="toolbar_redo")
		tooltips.AddDescription(b, commands.Redo.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.RemoveSelected, image="toolbar_delete")
		tooltips.AddDescription(b, commands.RemoveSelected.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.CutSelected, image="toolbar_cut")
		tooltips.AddDescription(b, commands.CutSelected.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.CopySelected, image="toolbar_copy")
		tooltips.AddDescription(b, commands.CopySelected.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.PasteClipboard, image="toolbar_paste")
		tooltips.AddDescription(b, commands.PasteClipboard.menu_name)
		b.pack(side = LEFT)

		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)

		b = ToolbarButton(tbar, commands.InsertFile, image = "toolbar_iVector")
		tooltips.AddDescription(b, commands.InsertFile.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.CreateImage, image = "toolbar_iRaster")
		tooltips.AddDescription(b, commands.CreateImage.menu_name)
		b.pack(side = LEFT)

		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)

		b = ToolbarButton(tbar, commands.ExportAs, image = "toolbar_eVector")
		tooltips.AddDescription(b, commands.ExportAs.menu_name)
		b.pack(side = LEFT)
		b = ToolbarButton(tbar, commands.ExportRaster, image = "toolbar_eRaster")
		tooltips.AddDescription(b, commands.ExportRaster.menu_name)
		b.pack(side = LEFT)

		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)

		b = ToolbarButton(tbar, canvas.commands.FitPageToWindow, image = "toolbar_FitToPage")
		tooltips.AddDescription(b, canvas.commands.FitPageToWindow.menu_name)
		b.pack(side = LEFT)

		b = ToolbarButton(tbar, commands.FitToNat, image = "toolbar_FitToNative")
		tooltips.AddDescription(b, commands.FitToNat.menu_name)
		b.pack(side = LEFT)

		b = ToolbarButton(tbar, canvas.commands.FitSelectedToWindow, image = "toolbar_FitToSelected")
		tooltips.AddDescription(b, canvas.commands.FitSelectedToWindow.menu_name)
		b.pack(side = LEFT)

		b = ToolbarButton(tbar, canvas.commands.ZoomIn, image="toolbar_zoom+")
		tooltips.AddDescription(b, canvas.commands.ZoomIn.menu_name)
		b.pack(side = LEFT)

		b = ToolbarButton(tbar, canvas.commands.ZoomOut, image="toolbar_zoom-")
		tooltips.AddDescription(b, canvas.commands.ZoomOut.menu_name)
		b.pack(side = LEFT)
		
		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)
		#-----------------------------------            
		# Renderers
		#-----------------------------------
		b = ToolbarCheckbutton(tbar, canvas.commands.UseXlibRenderer, image='toolbar_xlib')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.UseXlibRenderer.menu_name)
		
		label = TLabel(tbar, image = "sb_sep")
		label.pack(side = LEFT)
		
		b = ToolbarCheckbutton(tbar, canvas.commands.UseCairoRenderer, image='toolbar_cairo')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.UseCairoRenderer.menu_name)
		
		label = TLabel(tbar, image = "sb_sep")
		label.pack(side = LEFT)
		
		#b = ToolbarCheckbuttoncommands, canvas.commands.AllowAlphaChannel, image='toolbar_alpha')
		#b.pack(side = LEFT)
		#tooltips.AddDescription(b, canvas.commands.AllowAlphaChannel.menu_name)

		
		b = ToolbarCheckbutton(tbar, canvas.commands.ToggleOutlineMode, image='toolbar_contour')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.ToggleOutlineMode.menu_name)
		
		label = TLabel(tbar, image = "toolbar_sep")
		label.pack(side = LEFT)
		
		b = ToolbarCheckbutton(tbar, canvas.commands.AllowCMS, image='enable_cms')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.AllowCMS.menu_name)
		
		label = TLabel(tbar, image = "sb_sep")
		label.pack(side = LEFT)
	
	def build_toolbar1(self):
		tbar = self.tbar
		canvas = self.canvas

		cmds = [self.commands.CreatePrintDialog,
				#self.commands.Spacer, #
				#self.commands.CreateCurveDialog,
				#self.commands.CreateFontDialog,
				#self.commands.DuplicateSelected,
				#None,
				]

		buttons = []
		x=-1
		for cmd in cmds:
			x=x+1
			if cmd is None:
				b = Frame(tbar, class_ = 'TBSeparator')
				b.pack(side = LEFT, fill = Y)
			else:
				if cmd.is_check:
					b = CommandCheckbutton(tbar, cmd)
				else:
					b = CommandButton(tbar, cmd)
				tooltips.AddDescription(b, cmd.menu_name)
				b.pack(side = LEFT, fill = Y)

		def state_changed(buttons = buttons):
			for button in buttons:
				button.Update()

		canvas.Subscribe(STATE, state_changed)


	def build_status_bar(self):
		status_bar = self.status_bar
		canvas = self.canvas

		#Container
		sb1 = TFrame(status_bar, style="FlatFrame")
		sb1.pack(side = LEFT, fill = Y)
		#Position Info
		stat_pos = PositionLabel(sb1, name = 'position', text = '', width=20, updatecb = canvas.GetCurrentPos)
		stat_pos.pack(side = 'left')
		stat_pos.Update()
		canvas.Subscribe(POSITION, stat_pos.Update)


		sb_frame2 = TFrame(status_bar, style="RoundedSBFrame", borderwidth=2)
		sb_frame2.pack(side = LEFT, fill = BOTH)

		#OnGrid
		b = ToolbarCheckbutton(sb_frame2, canvas.commands.ToggleSnapToGrid, image='snap_to_grid')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.ToggleSnapToGrid.menu_name)
		
		label = TLabel(sb_frame2, image = "sb_sep")
		label.pack(side = LEFT)
		
		#OnGuide
		b = ToolbarCheckbutton(sb_frame2, canvas.commands.ToggleSnapToGuides, image='snap_to_guide')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.ToggleSnapToGuides.menu_name)
		
		label = TLabel(sb_frame2, image = "sb_sep")
		label.pack(side = LEFT)
		
		#OnObject
		b = ToolbarCheckbutton(sb_frame2, canvas.commands.ToggleSnapToObjects, image='snap_to_object')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.ToggleSnapToObjects.menu_name)

		
		label = TLabel(sb_frame2, image = "sb_sep")
		label.pack(side = LEFT)
		
		#ForceRedraw
		b = ToolbarButton(sb_frame2, canvas.commands.ForceRedraw, image='statusbar_refresh')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, canvas.commands.ForceRedraw.menu_name)


		#Zoom Info
		#l=Label(status_bar, anchor=SW, text='    Zoom:')
		#l.pack(side='left')

		#stat_zoom = UpdatedLabel(status_bar, name = 'zoom', text = '', updatecb = canvas.ZoomInfoText)
		#stat_zoom.pack(side = 'left')
		#stat_zoom.Update()
		#canvas.Subscribe(VIEW, stat_zoom.Update)

		#stat_edited = UpdatedLabel(status_bar, name = 'edited', text = '',
		#                          updatecb = self.EditedInfoText)
		#stat_edited.pack(side = 'left')
		#stat_edited.Update()
		#self.Subscribe(UNDO, stat_edited.Update)

		#Selection Color switch
		def ColorInfo():
				if len(self.document.selection) != 1 or self.document.CanUngroup():
					fill_frame["style"]='ColorWatchDisabled'
					outline_frame["style"]='ColorWatchDisabled'
					fill_frame['background']=app.uimanager.currentColorTheme.bg
					outline_frame['background']=app.uimanager.currentColorTheme.bg
					return _("")
					
				properties = self.document.CurrentProperties()
				filltxt=''
				outlinetxt=''
				try:
					fill_frame["style"]='ColorWatchNormal'
					fillcolor=rgb_to_tk(properties.fill_pattern.Color().RGB())
					fill_frame["background"]=fillcolor
					filltxt='Fill: ' + properties.fill_pattern.Color().toString()
				except:
					fill_frame["style"]='ColorWatchTransp'
					filltxt='Fill: None'
					
				try:
					outline_frame["style"]='ColorWatchNormal'
					outline_frame["background"]=rgb_to_tk(properties.line_pattern.Color().RGB())
					outlinetxt='Outline: '+ str(math.ceil(math.floor(10**4*properties.line_width/2.83465)/10)/1000) +' mm' 
				except:
					outline_frame["style"]='ColorWatchTransp'
					outlinetxt='Outline: None'
					
				return _(filltxt + "\n" + outlinetxt)

		space = Frame(status_bar, relief='flat', borderwidth=0, width=5)
		space.pack(side = RIGHT, fill=Y)
		sb3f = Frame(status_bar, relief='flat', borderwidth=1, width=20, height=15)
		sb3f.pack(side = RIGHT)
		
		fill_frame = TLabel(sb3f, style='ColorWatchDisabled', image='space_12')           
		outline_frame = TLabel(sb3f,  style='ColorWatchDisabled', image='space_12')
		
		fill_frame.grid(row=0, column=0, sticky = 'EW')
		outline_frame.grid(row=1, column=0, sticky = 'EW', pady=1)

		l=UpdatedLabel(status_bar, name='colors', text='', justify='right', updatecb = ColorInfo)
		l.pack(side= RIGHT)
		l.Update()
		canvas.Subscribe(POSITION, l.Update)
		canvas.Subscribe(EDITED, l.Update)
		canvas.Subscribe(SELECTION, l.Update)

		#Object Info
		stat_sel = UpdatedLabel(status_bar, name = 'selection',  justify='center', text = '', updatecb = canvas.CurrentInfoText)
		stat_sel.pack(side = 'left', fill = X, expand = 1)
		stat_sel.Update()
		update = stat_sel.Update
		canvas.Subscribe(SELECTION, update)
		canvas.Subscribe(CURRENTINFO, update)
		canvas.Subscribe(EDITED, update)

	def EditedInfoText(self):
		if self.document.WasEdited():
			return _("modified")
		return _("unmodified")


	AddCmd('AboutBox', _("About sK1..."))

	def BellTest(self, event):
			self.root.bell()

#Pallette Scrolling
	def ScrollUpPallette(self, delta):
			self.palette.ScrollXUnits(-1)
	def ScrollDownPallette(self, delta):
			self.palette.ScrollXUnits(1)

#Canvas Scrolling self.canvas.commands.ZoomOut
	def ScrollUpCanvas(self, delta):
			self.canvas.ScrollYUnits(-1)
	def ScrollDownCanvas(self, delta):
			self.canvas.ScrollYUnits(1)
	def ScrollLeftCanvas(self, delta):
			self.canvas.ScrollXUnits(-1)
	def ScrollRightCanvas(self, delta):
			self.canvas.ScrollXUnits(1)
	def CanvasZoomingOut(self, delta):
			self.canvas.ZoomFactor(0.75)
	def CanvasZoomingIn(self, delta):
			self.canvas.ZoomFactor(1.5)

	def RulerDoublePressH(self, event):
			self.root.bell()
			self.CreateDialog('dlg_grid', 'GridPanel')
	def RulerDoublePressV(self, event):
			self.CreateDialog('dlg_layer', 'LayerPanel')
	def MenuOne(self):
			self.CreateDialog('menu1', 'Menu1')
	def GuideDialog(self, action=None):
			self.CreateDialog('dlg_guide', 'GuidePanel')

	def AboutBox(self):
		abouttext = _("sK1 (%(version)s) - A Python&Tcl/Tk -based vector graphics editor for printing industry.\n "
						"(c) 2003-2006 by Igor E. Novikov\n\n"
						"This program is free software under the terms of "
						"the GNU LGPL v.2.0. For more info - COPYRIGHTS file in sK1 root directory.\n\n"
						"Libraries versions:\n"
						"Python:\t%(py)s\t\nTcl:\t%(tcl)s\n"
						"Tkinter:\t%(tkinter)s\t\nTk:\t%(tk)s") \
					% {'version':sKVersion,
						'py':string.split(sys.version)[0],
						'tcl':TclVersion,
						'tkinter':string.split(Tkinter.__version__)[1],
						'tk':TkVersion}

		self.application.MessageBox(title = _("About sK1"), message = abouttext, icon = 'construct')


	#
	#       Special methods. Mainly interesting for debugging
	#
	AddCmd('DocumentInfo', "Document Info...")#, bitmap = pixmaps.DocInfo)

	def DocumentInfo(self):
		text = self.document.DocumentInfo()

		from app import _sketch
		meminfo = '\nMemory:\n'\
					'# Bezier Paths:\t\t%d\n'\
					'# RGBColors:\t\t%d\n' \
					'# Rects:\t\t%d\n'\
					'# Trafos:\t\t%d\n'\
					'# Points:\t\t%d' % (_sketch.num_allocated(),
										_sketch.colors_allocated(),
										_sketch.rects_allocated(),
										_sketch.trafos_allocted(),
										_sketch.points_allocated())
		text = '\n' + text + '\n\n' + meminfo+ '\n\n'

		self.application.MessageBox(title = 'Document Info', message = text, icon = 'construct')

	AddCmd('DumpXImage', 'Dump XImage')
	def DumpXImage(self):
		gc = self.canvas.gc
		if gc.ximage:
			gc.ximage.dump_data("~/.sK1/ximage.dat")



#     AddCmd('export_bitmap', 'Export Bitmap')
#     def export_bitmap(self):
#       import export
#       export.export_bitmap(self.document)

	AddCmd('python_prompt', 'Python Prompt')
	def python_prompt(self):
		if config.preferences.show_special_menu:
			import prompt
			prompt.PythonPrompt()


	#
	#       Insert Special Objects
	#

	#
	#       Create Image
	#

	def GetOpenImageFilename(self, title = None, initialdir = '', initialfile = '', no_eps = 0):
		if title is None:
			title = _("to load image - sK1")
		if no_eps:
			filetypes = skapp.imagefiletypes()
		else:
			filetypes = skapp.imagefiletypes()
		filename = self.KGetOpenFilename(title = title,
													filetypes = filetypes,
													initialdir = initialdir,
													initialfile = initialfile)
		return filename

	AddCmd('CreateImage', _("Import bitmap..."), #bitmap = pixmaps.ImportImage,
			subscribe_to = None)
	def CreateImage(self, filename = None):
		if not filename:
			filename = self.GetOpenImageFilename(title = _("to import bitmap - sK1"),
										initialdir = config.preferences.image_dir,
													initialfile = '')
		if filename:
			try:
				self.canvas.commands.ForceRedraw
				file = open(filename, 'r')
				is_eps = eps.IsEpsFileStart(file.read(256))
				file.close()
				dir, name = os.path.split(filename)
				config.preferences.image_dir = dir
				if is_eps:
					imageobj = eps.EpsImage(filename = filename)
				else:
					imageobj = image.Image(imagefile = filename)
				self.canvas.PlaceObject(imageobj)
			except IOError, value:
				if type(value) == TupleType:
					value = value[1]
				self.application.MessageBox(title = _("Load Image"),
								message = _("Cannot load %(filename)s:\n"
											"%(message)s") \
								% {'filename':`os.path.split(filename)[1]`,
									'message':value})

	AddCmd('AddHorizGuideLine', _("Add Horizontal Guide Line"), 'AddGuideLine', args = 1)
	AddCmd('AddVertGuideLine', _("Add Vertical Guide Line"), 'AddGuideLine', args = 0)
	def AddGuideLine(self, horizontal = 1):
		self.canvas.PlaceObject(GuideLine(Point(0, 0), horizontal))

	#
	#
	#

	AddCmd('CreateStyleFromSelection', _("Name Style..."), sensitive_cb = ('document', 'CanCreateStyle'), subscribe_to = SELECTION)
	def CreateStyleFromSelection(self):
		import styledlg
		doc = self.document
		object = doc.CurrentObject()
		style_names = doc.GetStyleNames()
		if object:
			name = styledlg.GetStyleName(self.root, object, style_names)
			if name:
				name, which_properties = name
				doc.CreateStyleFromSelection(name, which_properties)

	def no_pattern(self, category):
		import styledlg
		if category == 'fill':
			title = _("No Fill")
			prop = 'fill_pattern'
		else:
			title = _("No Line")
			prop = 'line_pattern'
		styledlg.set_properties(self.root, self.document, title, category,
								{prop: EmptyPattern})


	#
	#       Document commands
	#

	AddDocCmd('SelectAll', _("Select All"), sensitive_cb = 'IsSelectionMode',
				subscribe_to = MODE)
	AddDocCmd('SelectNextObject', _("Select Next"), key_stroke = 'Alt+Right')
	AddDocCmd('SelectPreviousObject', _("Select Previous"),
				key_stroke = 'Alt+Left')
	AddDocCmd('SelectFirstChild', _("Select First Child"),
				key_stroke = 'Alt+Down')
	AddDocCmd('SelectParent', _("Select Parent"), key_stroke = 'Alt+Up')

	# rearrange object

	AddDocCmd('MoveUp', _("Move Up"), 'HandleMoveSelected', args=(0,1), key_stroke = ('Up', 'KP_Up'))        
	AddDocCmd('MoveDown', _("Move Down"), 'HandleMoveSelected', args=(0,-1), key_stroke = ('Down', 'KP_Down'))
	AddDocCmd('MoveRight', _("Move Right"), 'HandleMoveSelected', args=(1,0), key_stroke = ('Right', 'KP_Right'))
	AddDocCmd('MoveLeft', _("Move Left"), 'HandleMoveSelected', args=(-1,0), key_stroke = ('Left', 'KP_Left'))

	AddDocCmd('RemoveSelected', _("Delete"), key_stroke = ('Del', 'Delete', 'KP_Delete'))#, bitmap = pixmaps.Delete)

	AddDocCmd('MoveSelectedToTop', _("Move to Top"), #bitmap = pixmaps.MoveToTop,
			  key_stroke = ('Shift+PgUp', 'Shift+Prior', 'Shift-KP_Prior'))
	AddDocCmd('MoveSelectedToBottom', _("Move to Bottom"),#bitmap = pixmaps.MoveToBottom,
			  key_stroke = ('Shift+PgDown', 'Shift+Next', 'Shift-KP_Next'))

	AddDocCmd('MoveSelectionUp', _("Move One Up"), #bitmap = pixmaps.MoveOneUp,
			  key_stroke = ('Ctrl+PgUp', 'Ctrl+Prior', 'Ctrl+KP_Prior'))
	AddDocCmd('MoveSelectionDown', _("Move One Down"), #bitmap = pixmaps.MoveOneDown,
			  key_stroke = ('Ctrl+PgDown', 'Ctrl+Next', 'Ctrl+KP_Next'))

	AddDocCmd('ApplyToDuplicate', _("Duplicate0"))
	AddDocCmd('DuplicateSelected', _("Duplicate"), #bitmap = pixmaps.Duplicate,
			  key_stroke = ('Ctrl+D', 'Ctrl+d'))
	AddDocCmd('GroupSelected', _("Group selected objects"), sensitive_cb = 'CanGroup', key_stroke = ('Ctrl+G', 'Ctrl+g'), bitmap = pixmaps.Group)
	AddDocCmd('UngroupSelected', _("Ungroup selection"), sensitive_cb = 'CanUngroup', key_stroke = ('Ctrl+U', 'Ctrl+u'), bitmap = pixmaps.Ungroup)
	AddDocCmd('ConvertToCurve', _("Convert To Curve"), sensitive_cb = 'CanConvertToCurve', key_stroke = ('Ctrl+Q', 'Ctrl+q'), bitmap = pixmaps.ToCurve)
	AddDocCmd('CombineBeziers', _("Combine Beziers"), sensitive_cb = 'CanCombineBeziers', key_stroke = ('Ctrl+L','Ctrl+l'), bitmap = pixmaps.CCombine)
	AddDocCmd('SplitBeziers', _("Split Beziers"), sensitive_cb = 'CanSplitBeziers', key_stroke = ('Ctrl+K', 'Ctrl+k'), bitmap = pixmaps.Break)

	#
	#       Align
	#
	AddDocCmd('AbutHorizontal', _("Abut Horizontal"))
	AddDocCmd('AbutVertical', _("Abut Vertical"))

	AddDocCmd('FlipHorizontal', _("Flip Horizontal"), 'FlipSelected', args = (1, 0), bitmap = pixmaps.FlipHorizontal)
	AddDocCmd('FlipVertical', _("Flip Vertical"), 'FlipSelected', args = (0, 1), bitmap = pixmaps.FlipVertical)


	# effects
	AddDocCmd('CancelBlend', _("Cancel Blend"), sensitive_cb = 'CanCancelBlend')
	AddDocCmd('RemoveTransformation', _("Remove Transformation"))
	AddDocCmd('CreateMaskGroup', _("Create Mask Group"), sensitive_cb = 'CanCreateMaskGroup')
	AddDocCmd('CreatePathText', _("Create Path Text"), sensitive_cb = 'CanCreatePathText')
	AddDocCmd('CreateClone', _("Create Clone"), sensitive_cb = 'CanCreateClone')


	#
	#       Cut/Paste
	#

	def CutCopySelected(self, method):
		objects = getattr(self.document, method)()
		if objects is not None:
			self.application.SetClipboard(objects)

	def CopyPasteSelected(self,method):
		objects = getattr(self.document, method)()
		if objects is not None:
			self.application.SetClipboard(objects)
			if self.application.ClipboardContainsData():
					obj = self.application.GetClipboard().Object()
					obj = obj.Duplicate()
					self.canvas.PlaceObject(obj)

	def FitToNat (self):
		hp=float(self.canvas.winfo_screenheight())
		hm=float(self.canvas.winfo_screenmmheight())
		self.canvas.SetScale(1.07+hm/hp)


	AddCmd('FitToNat', _("Zoom 1:1"), 'FitToNat')#, bitmap = pixmaps.FitToNative)

	AddCmd('CopySelected', _("Copy"), 'CutCopySelected',
			args= ('CopyForClipboard',), subscribe_to = SELECTION,
			#bitmap = pixmaps.Copy,
			key_stroke = ('Ctrl+C', 'Ctrl+c'),
			sensitive_cb = ('document', 'HasSelection'))
			
	AddCmd('CopyPaste', _("Copy&Paste"), 'CopyPasteSelected',
			args= ('CopyForClipboard',), subscribe_to = SELECTION, key_stroke = 'F6',
			sensitive_cb = ('document', 'HasSelection'))
	
	AddCmd('CutSelected', _("Cut"), 'CutCopySelected',
			args= ('CutForClipboard',), subscribe_to = SELECTION,
			#bitmap = pixmaps.Cut, 
			key_stroke = ('Ctrl+X', 'Ctrl+x'),
			sensitive_cb = ('document', 'HasSelection'))
			
	AddCmd('PasteClipboard', _("Paste"),
			#bitmap = pixmaps.Paste,
			key_stroke = ('Ctrl+V', 'Ctrl+v'),
			subscribe_to = ('application', CLIPBOARD),
			sensitive_cb = ('application', 'ClipboardContainsData'))
			
	AddCmd('ExportRaster', 
		   _("Export Bitmap..."), 
		   #bitmap = pixmaps.ExportR, 
		   'ExportRaster')

	AddDocCmd('RotLeft', _("Rotate Left 90"), 'RotateSelected', args=(90),  bitmap = pixmaps.RotLeft)
	AddDocCmd('Rot180', _("Rotate 180"), 'RotateSelected', args=(180),  bitmap = pixmaps.Rot180)
	AddDocCmd('RotRight', _("Rotate Right 90"), 'RotateSelected', args=(-90),  bitmap = pixmaps.RotRight)
	AddDocCmd('UngrAll', _("Ungroup All"), 'UngroupAllSelected', sensitive_cb = 'CanUngroupAll', bitmap = pixmaps.UngrAll)




	def Spacer(self):
			pass
	def ExportRaster(self):
			export_raster_more_interactive(self)

	def PasteClipboard(self):
		if self.application.ClipboardContainsData():
			obj = self.application.GetClipboard().Object()
			obj = obj.Duplicate()
			if config.preferences.insertion_mode:
				self.canvas.PlaceObject(obj)
			else:
				self.document.Insert(obj)

	#
	#       Undo/Redo
	#

	AddDocCmd('Undo', _("Undo"), 
			  subscribe_to = UNDO, 
			  sensitive_cb = 'CanUndo',
			  #bitmap = pixmaps.Undo, 
			  name_cb = 'UndoMenuText', 
			  key_stroke = ('Ctrl+Z', 'Ctrl+z'))
	AddDocCmd('Redo', _("Redo"), 
			  subscribe_to = UNDO, 
			  sensitive_cb = 'CanRedo', 
			  name_cb = 'RedoMenuText',
			  #bitmap = pixmaps.Redo,
			  key_stroke = ('Ctrl+Shift+Z', 'Ctrl+Z'))

	AddDocCmd('ResetUndo', _("Discard Undo History"), subscribe_to = None, sensitive_cb = None)


	#
	#       Styles
	#
	AddDocCmd('FillNone', _("No Fill"), 'AddStyle', args = EmptyFillStyle)
	AddDocCmd('LineNone', _("No Line"), 'AddStyle', args = EmptyLineStyle)
	AddDocCmd('UpdateStyle', _("Update Style"), 'UpdateDynamicStyleSel')

	
