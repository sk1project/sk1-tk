# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _, Document, config, dialogman, SketchError
from app.conf.const import STATE, VIEW, MODE, CHANGED, SELECTION, POSITION, UNDO, EDITED, CURRENTINFO
from app.utils import os_utils, locale_utils
from app.plugins import plugins
from app.io import load
import app, os, sys, string
from app.UI.dialogs.msgdialog import msgDialog
from app.UI.dialogs import msgdialog
from app.UI.dialogs.progressdialog import ProgressDialog
import time


EXPORT_MODE=2
SAVE_AS_MODE=1
SAVE_MODE=0

class DocumentManager:
	docs=[]
	mw=None
	tabspanel=None
	activedoc=None
	counter=0	
	
	def __init__(self, mainwindow):
		self.mw=mainwindow
		self.NewDocument()

################## Interfaces #############################
		
	def NewDocument(self):
		doc=Document(create_layer = 1)
		self.counter+=1
		doc.meta.filename='New Document %u.sk1'%self.counter
		doc.meta.view=None
		self.SetActiveDocument(doc)
		if self.tabspanel:
			self.tabspanel.addNewTab(self.activedoc)
	
	def OpenDocument(self, filename = None, directory = None):
		self.mw.root.update()
		if type(filename) == type(0):
			filename = config.preferences.mru_files[filename]
		if not filename:
			if not directory:
				directory = self.mw.document.meta.directory
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
			############--->
			dlg = ProgressDialog(self.mw.root, 'File opening')
			doc=dlg.RunDialog(self.open_callback, filename)
			############ <---
			doc.meta.view=None
			self.SetActiveDocument(doc)
			self.mw.add_mru_file(filename)			
			self.mw.canvas.ForceRedraw()			
			if self.tabspanel:
				self.tabspanel.addNewTab(self.activedoc)
		except SketchError, value:
			msgDialog(self.mw.root, title = _("Open"), message = _("\nAn error occurred:\n\n") + str(value))
			self.mw.remove_mru_file(filename)
		else:
			messages = doc.meta.load_messages
			if messages:
				msgDialog(self.mw.root, title = _("Open"), message=_("\nWarnings from the import filter:\n\n")+ messages)
			doc.meta.load_messages = ''
			
	def open_callback(self, arg):
		app.updateInfo(inf1=_('Document parsing'), 
					inf2=_('Start document processing'), inf3=3)
		filename=arg[0]
		doc = load.load_drawing(filename)
		app.updateInfo(inf1=_('Document parsing'), 
					inf2=_('Document has been loaded'), inf3=100)
		time.sleep(.1)
		return doc
	
	def SaveDocument(self, document, use_dialog = SAVE_MODE):
		filename = document.meta.fullpathname
		native_format = document.meta.native_format
		compressed_file = document.meta.compressed_file
		compressed = document.meta.compressed
		if use_dialog or not filename or not native_format:
			directory = document.meta.directory
			
			if not directory:
				if use_dialog==SAVE_AS_MODE or use_dialog==SAVE_MODE:
					directory=config.preferences.dir_for_save
					filename=document.meta.filename
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
		############ --->
		dlg = ProgressDialog(self.mw.root, 'File saving')
		dlg.RunDialog(self.save_callback, document, filename, fileformat, compressed, compressed_file)
		
	def save_callback(self,arg):
		app.updateInfo(inf1=_('Document saving/exporting'), 
					inf2=_('Start document processing'), inf3=3)
		self.SaveToFile(arg[0],arg[1],arg[2],arg[3],arg[4])
		app.updateInfo(inf2=_('Finish document processing'), inf3=100)		
		time.sleep(.1)
		return None
	
	def SaveDocumentAs(self):
		pass
	
	def CloseDocument(self, document):
		if document is not None:
			document.Destroy()
			
	def PrintDocument(self, document):
		bbox = document.BoundingRect(visible = 0, printable = 1)
		if bbox is None:
			msgDialog(self.mw.root, 
					title = _("Printing"), 
					message = _("The document doesn't have \n any printable layers!\n"))
			return
		############ --->
		dlg = ProgressDialog(self.mw.root, 'File importing')
		dlg.RunDialog(self.print_callback, document)

	def print_callback(self, arg):
		document=arg[0]
		from tempfile import NamedTemporaryFile
		pdffile=NamedTemporaryFile()
		fileformat = plugins.guess_export_plugin('.pdf')
		self.SaveToFile(document, pdffile.name, fileformat, '', '')
		
		os.popen('kprinter --caption sK1 "'+ pdffile.name + '"', 'w')
		
		self.mw.root.update()
		self.mw.canvas.ForceRedraw()
		time.sleep(.5)
		return None
	
	def ImportVector(self, filename = None):
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
			############--->
			dlg = ProgressDialog(self.mw.root, 'File importing')
			doc=dlg.RunDialog(self.import_callback, filename)
			############ <---			doc = load.load_drawing(filename)
			group = doc.as_group()
		except SketchError, value:
			group=None
			msgDialog(self.mw.root, title = _("Import vector"), message = _("\nAn error occurred:\n\n") + str(value))
			self.mw.remove_mru_file(filename)
			dlg.close_dlg()
		else:
			messages = doc.meta.load_messages
			if messages:
				msgDialog(self.mw.root, title = _("Import vector"), message=_("\nWarnings from the import filter:\n\n") + messages)
			doc.meta.load_messages = ''
		if group is not None:
			if config.preferences.import_insertion_mode:
				self.mw.canvas.PlaceObject(group)
			else:
				self.mw.document.Insert(group)
		else:
			msgDialog(self.mw.root, title = _("Import vector"), message=_("\nThe document is empty!\n"))
		config.preferences.dir_for_vector_import=os.path.dirname(filename)
		
	def import_callback(self, arg):
		app.updateInfo(inf1=_('File importing'), 
					inf2=_('Start file parsing'), inf3=3)
		filename=arg[0]
		doc = load.load_drawing(filename)
		app.updateInfo(inf1=_('File importing'), 
					inf2=_('File has been imported'), inf3=100)
		time.sleep(.1)
		return doc		
		

################## Utilite methods #############################
	
	def SetActiveDocument(self, doc):
		channels = (SELECTION, UNDO, MODE)
		view=None
		if self.mw.canvas:		
			self.mw.canvas.bitmap_buffer=None
			self.activedoc.meta.view=self.mw.canvas.get_viewport_data()
		old_doc = self.activedoc
		
		self.activedoc=doc
			
		if old_doc is not None:
			for channel in channels:
				old_doc.Unsubscribe(channel, self.mw.issue, channel)
		self.mw.document = doc
		for channel in channels:
			self.mw.document.Subscribe(channel, self.mw.issue, channel)
		if self.mw.canvas is not None:
			self.mw.canvas.SetDocument(self.mw.document)
		self.mw.issue_document()
		
		self.set_window_title()
		self.mw.document.Subscribe(SELECTION, self.mw.refresh_buffer)		
		if self.mw.commands:
			self.mw.commands.Update()
		if self.activedoc.meta.view is not None:
			self.mw.canvas.restore_viewport_from_data(self.activedoc.meta.view)

			
	def Activate(self, tabspanel):
		self.tabspanel=tabspanel
		self.tabspanel.docmanager=self
		self.tabspanel.addNewTab(self.activedoc)
		
	def SaveToFile(self, document, filename, fileformat = None, compressed = '', compressed_file = ''):
		sysname=locale_utils.utf_to_locale(filename)
		try:
			if not document.meta.backup_created:
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
					result = msgDialog(self.mw.root, title = _("Save To File"), message = msg, buttons = (_("Continue"), cancel))
					if result == cancel:
						return

				document.meta.backup_created = 1
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
					saver(document, filename, file = file)
				else:
					saver(document, sysname)
			finally:
				saver.UnloadPlugin()
		except IOError, value:
			if type(value) == type(()):
				value = value[1]
			msgDialog(self.mw.root, title = _("Save To File"),
							message = _("\nCannot save %(filename)s:\n\n"
										"%(message)s") \
							% {'filename':`os.path.split(filename)[1]`,
								'message':value})
			self.mw.remove_mru_file(filename)
			return

		if fileformat == plugins.NativeFormat:
			dir, name = os.path.split(filename)
			# XXX should meta.directory be set for non-native formats as well
			document.meta.directory = dir
			document.meta.filename = name
			document.meta.fullpathname = filename
			document.meta.file_type = plugins.NativeFormat
			document.meta.native_format = 1
		if not compressed_file:
			document.meta.compressed_file = ''
			document.meta.compressed = ''
		if fileformat == plugins.NativeFormat:
			if compressed_file:
				self.mw.add_mru_file(compressed_file)
			else:
				self.mw.add_mru_file(filename)

		self.set_window_title()	
		
	def save_doc_if_edited(self, document, title = _("sK1 - Save Document...")):
		if document is not None and document.WasEdited():
			message = _("\nFile: <%s> has been changed ! \n\nDo you want to save it?\n") % document.meta.filename
			result = msgDialog(self.mw.root, title = title, message = message, buttons = msgdialog.SaveDontSaveCancel)
			self.mw.root.deiconify()
			if result == msgdialog.Save:
				self.SaveDocument(document)
			return result
		return msgdialog.No
	
	def set_window_title(self):
		self.mw.root.client(os_utils.gethostname())
		if self.mw.document:
			appname = config.name
			meta = self.mw.document.meta
			if meta.compressed:
				docname = os.path.split(meta.compressed_file)[1]
				docname = os.path.splitext(docname)[0]
			else:
				if meta.fullpathname:					
					docname = meta.fullpathname
				else:
					docname = os.path.splitext(meta.filename)[0]
			title = config.preferences.window_title_template % locals()
			command = (config.sk_command, meta.fullpathname)
		else:
			title = config.name
			command = (config.sk_command, )
		self.mw.root.title(title)
		self.mw.root.command(command)
			