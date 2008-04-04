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

from Tkinter import Tk, TclError, PhotoImage, Wm
from app.UI import tkext

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
#	file type info
#

def openfiletypes():
	types=' \'*.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sK1 \''
	return types

def importfiletypes():
	types=' \'*.sK1 *.sk1 *.SK1 *.sk *.SK *.ai *.AI *.eps *.EPS *.ps *.PS'
	types=types+'*.cmx *.CMX *.cdr *.CDR *.cdt *.CDT *.ccx *.CCX'
	types=types+'*.cgm *.CGM *.aff *.AFF *.svg *.SVG *.wmf *.WMF *.fig *.FIG'
	types=types+'|All supported files - *.sk1 *.sk *.ai *.eps *.cdr *.svg *.wmf etc. \n'
	#Detalied extentions list
	types=types+' *.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sk1 \n'
	types=types+' *.sk *.SK|Sketch and Skencil files - *.sk \n'
	types=types+' *.ai *.AI|Adobe Illustrator files (up to ver. 9.0) - *.ai \n'
	types=types+' *.eps *.EPS|Encapsulated PostScript files - *.eps \n'
	types=types+' *.ps *.PS|PostScript files - *.ps \n'
	types=types+' *.cdr *.CDR|CorelDRAW Graphics files (7-X3 ver.) - *.cdr \n'
	types=types+' *.cdt *.CDT|CorelDRAW Templates files (7-X3 ver.) - *.cdt \n'	
	types=types+' *.cmx *.CMX|CorelDRAW Presentation Exchange files - *.cmx \n'
	types=types+' *.ccx *.CCX|CorelDRAW Compressed Exchange files (CDRX format) - *.ccx \n'
	types=types+' *.cgm *.CGM|Computer Graphics Metafile files - *.cgm \n'
	types=types+' *.aff *.AFF|Draw files - *.aff \n'
	types=types+' *.svg *.SVG|Scalable Vector Graphics files - *.svg \n'
	types=types+' *.wmf *.WMF|Windows Metafile files - *.wmf \n'
	types=types+' *.fig *.FIG|XFig files - *.fig \''
	return types

def savefiletypes():
	types=' \'*.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sK1 \''
	return types

def exportfiletypes():
	types=' \'*.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sK1 \n'
	types=types+' *.sk *.SK|Sketch and Skencil files - *.sk \n'
	types=types+' *.ai *.AI|Adobe Illustrator files (ver. 5.0) - *.ai \n'
	types=types+' *.cgm *.CGM|Computer Graphics Metafile files - *.cgm \n'
	types=types+' *.svg *.SVG|Scalable Vector Graphics files - *.svg \n'
	types=types+' *.wmf *.WMF|Windows Metafile files - *.wmf \''
	return types

def imagefiletypes():
	types=' \'*.png *.PNG *.gif *.GIF *.jpg *.JPG *.jpeg *.JPEG *.tif *.TIF' 
	types=types+' *.tiff *.TIFF *.gif *.GIF *.bmp *.BMP *.pcx *.PCX *.pbm *.PBM'
	types=types+' *.pgm *.PGM *.ppm *.PPM *.eps *.EPS'
	types=types+'|All supported files - *.png *.jpg *.tif *.gif *.psd *.bmp *.pcx etc. \n'
	types=types+' *.png *.PNG|Portable Network Graphics files - *.png \n'
	types=types+' *.eps *.EPS|Encapsulated PostScript files - *.eps \n'
	types=types+' *.jpg *.JPG *.jpeg *.JPEG|JPEG files - *.jpg *jpeg \n'
	types=types+' *.tif *.TIF *.tiff *.TIFF|TIFF files - *.tif *.tiff \n'
	types=types+' *.gif *.GIF|CompuServ Graphics files - *.gif \n'
	types=types+' *.psd *.PSD|Adobe Photoshop files (up to v.3.0) - *.psd \n'
	types=types+' *.bmp *.BMP|Windows Bitmap files - *.bmp \n'
	types=types+' *.pcx *.PCX|Paintbrush files - *.pcx \n'
	types=types+' *.pbm *.PBM|Portable Bitmap files - *.pbm \n'
	types=types+' *.pgm *.PGM|Portable Graymap files - *.pgm \n'
	types=types+' *.ppm *.PPM|Portable Pixmap files - *.ppm \''
	return types

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
		
		#self.root.tk.call('lappend', 'auto_path', config.sk_themes)
		#self.root.tk.call('package', 'require', 'tkpng')
		#self.root.tk.call('package', 'require', 'tile')
		#self.root.tk.call('tile::setTheme', config.preferences.style)
		
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
		tooltips.Init(self.root)
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
		#root.iconname('sK1')
		#root.tk.call('wm', 'attributes', root, '-zoomed', 1)
		#root.tk.call('wm', 'iconphoto', root, 'icon_sk1_16')
		root.group(root)
		config.add_options(root)

	def build_window(self):
		from app.UI.mainwindow import SketchMainWindow
		self.main_window = SketchMainWindow(self, self.filename, self.run_script)


	def SavePreferences(self, *args):
		config.save_user_preferences()

