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
from app.UI import tkext


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
		self.SetActiveDocument(doc)
		if self.tabspanel:
			self.tabspanel.addNewTab(self.activedoc)
	
	def OpenDocument(self, filename = None, directory = None):
		self.mw.root.update()
		app = self.mw.application
#		if self.save_doc_if_edited(_("Open Document        ")) == tkext.Cancel:
#			return
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
			doc = load.load_drawing(filename)
			self.SetActiveDocument(doc)
			self.mw.add_mru_file(filename)
			self.mw.canvas.bitmap_buffer=None			
			self.mw.canvas.commands.ForceRedraw
			if self.tabspanel:
				self.tabspanel.addNewTab(self.activedoc)
		except SketchError, value:
			app.MessageBox(title = _("Open"), message = _("\nAn error occurred:\n\n") + str(value))
			self.mw.remove_mru_file(filename)
		else:
			messages = doc.meta.load_messages
			if messages:
				app.MessageBox(title = _("Open"), message=_("\nWarnings from the import filter:\n\n")+ messages)
			doc.meta.load_messages = ''
	
	def SaveDocument(self, document, use_dialog = SAVE_MODE):
		filename = document.meta.fullpathname
		native_format = document.meta.native_format
		compressed_file = document.meta.compressed_file
		compressed = document.meta.compressed
		app = self.mw.application
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
		self.SaveToFile(document, filename, fileformat, compressed, compressed_file)
	
	def SaveDocumentAs(self):
		pass
	
	def CloseDocument(self, document):
		if document is not None:
			document.Destroy()

################## Utilite methods #############################
	
	def SetActiveDocument(self, doc):
		channels = (SELECTION, UNDO, MODE)
		if self.mw.canvas:		
			self.mw.canvas.bitmap_buffer=None
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
		# issue_document has to be called before old_doc is destroyed,
		# because destroying it causes all connections to be deleted and
		# some dialogs (derived from SketchDlg) try to unsubscribe in
		# response to our DOCUMENT message. The connector currently
		# raises an exception in this case. Perhaps it should silently
		# ignore Unsubscribe() calls with methods that are actually not
		# subscribers (any more)
#		if old_doc is not None:
#			old_doc.Destroy()
		self.mw.set_window_title()
		self.mw.document.Subscribe(SELECTION, self.mw.refresh_buffer)		
		if self.mw.commands:
			self.mw.commands.Update()
			
	def Activate(self, tabspanel):
		self.tabspanel=tabspanel
		self.tabspanel.docmanager=self
		self.tabspanel.addNewTab(self.activedoc)
		
	def SaveToFile(self, document, filename, fileformat = None, compressed = '', compressed_file = ''):
		sysname=locale_utils.utf_to_locale(filename)
		app = self.mw.application
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
					result = app.MessageBox(title = _("Save To File"), message = msg, buttons = (_("Continue"), cancel))
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
			app.MessageBox(title = _("Save To File"),
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
		if compressed_file:
			self.mw.add_mru_file(compressed_file)
		else:
			self.mw.add_mru_file(filename)

		self.mw.set_window_title()	
		
	def save_doc_if_edited(self, document, title = _("sK1 - Save Document...")):
		if document is not None and document.WasEdited():
			message = _("\nFile: <%s> has been changed ! \n\nDo you want to save it?\n") % document.meta.filename
			result = self.mw.application.MessageBox(title = title, message = message, buttons = tkext.SaveDSCancel)
			self.mw.root.deiconify()
			if result == tkext.Save:
				self.SaveDocument(document)
			return result
		return tkext.No
			