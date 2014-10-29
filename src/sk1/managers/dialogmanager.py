# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import app, os, sk1
from app import _
from tempfile import NamedTemporaryFile

PATH = os.path.dirname(os.path.abspath(__file__))

openfiletypes = ((_('sK1 vector graphics files - *.sK1'), ('*.sK1', '*.sk1', '*.SK1')),
				 (_("All Files"), 	 '*'))

importfiletypes = ((_('All supported files - *.sk1 *.sk *.ai *.eps *.cdr *.svg *.wmf etc. '),
				  ('*.sK1', '*.sk1', '*.SK1', '*.sk', '*.SK', '*.ai', '*.AI', '*.eps', '*.EPS', '*.ps', '*.PS',
					'*.cmx', '*.CMX', '*.cdr', '*.CDR', '*.cdt', '*.CDT', '*.ccx', '*.CCX', '*.cgm',
					'*.CGM', '*.aff', '*.AFF', '*.svg', '*.SVG', '*.wmf', '*.WMF', '*.plt', '*.PLT',
					'*.dxf', '*.DXF', '*.fig', '*.FIG')),
				 (_('sK1 vector graphics files - *.sk1'), ('*.sK1', '*.sk1', '*.SK1')),
				 (_('Sketch\Skencil files - *.sk'), ('*.sk', '*.SK')),
				 (_('Adobe Illustrator files (up to ver. 9.0) - *.ai'), ('*.ai', '*.AI')),
				 (_('Encapsulated PostScript files - *.eps'), ('*.eps', '*.EPS')),
				 (_('PostScript files - *.ps'), ('*.ps', '*.PS')),
				 (_('CorelDRAW Graphics files (7-X4 ver.) - *.cdr'), ('*.cdr', '*.CDR')),
				 (_('CorelDRAW Templates files (7-X4 ver.) - *.cdt'), ('*.cdt', '*.CDT')),
				 (_('CorelDRAW Presentation Exchange files - *.cmx'), ('*.cmx', '*.CMX')),
				 (_('CorelDRAW Compressed Exchange files (CDRX format) - *.ccx'), ('*.ccx', '*.CCX')),
				 (_('Computer Graphics Metafile files - *.cgm'), ('*.cgm', '*.CGM')),
				 (_('Acorn Draw files - *.aff'), ('*.aff', '*.AFF')),
				 (_('Scalable Vector Graphics files - *.svg'), ('*.svg', '*.SVG')),
				 (_('Windows Metafile files - *.wmf'), ('*.wmf', '*.WMF')),
				 (_('HPGL cutting plotter files - *.plt'), ('*.plt', '*.PLT')),
				 (_('AutoCAD DXF files - *.dxf'), ('*.dxf', '*.DXF')),
				 (_('XFig files - *.fig'), ('*.fig', '*.FIG')),
				 (_("All Files"), 	 '*'))

savefiletypes = ((_('sK1 vector graphics files - *.sK1'), ('*.sK1', '*.sk1', '*.SK1')),)

exportfiletypes = ((_('sK1 vector graphics files - *.sK1'), ('*.sK1', '*.sk1', '*.SK1')),
				 (_('Sketch and Skencil files - *.sk'), ('*.sk', '*.SK')),
				 (_('Adobe Illustrator files (ver. 5.0) - *.ai'), ('*.ai', '*.AI')),
				 (_('Portable Document Format (PDF 1.5) - *.pdf'), ('*.pdf', '*.PDF')),
				 (_('PostScript - *.ps'), ('*.ps', '*.PS')),
				 (_('Computer Graphics Metafile files - *.cgm'), ('*.cgm', '*.CGM')),
				 (_('Scalable Vector Graphics files - *.svg'), ('*.svg', '*.SVG')),
				 (_('Windows Metafile files - *.wmf'), ('*.wmf', '*.WMF')),
				 (_('HPGL cutting plotter files - *.plt'), ('*.plt', '*.PLT')),
				 (_("All Files"), 	 '*'))

imagefiletypes = ((_('All supported files - *.png *.jpg *.tif *.gif *.psd *.bmp *.pcx etc.'),
				 ('*.png', '*.PNG', '*.gif', '*.GIF', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.tif', '*.TIF',
				  '*.tiff', '*.TIFF', '*.bmp', '*.BMP', '*.pcx', '*.PCX', '*.pbm', '*.PBM',
				  '*.pgm', '*.PGM', '*.ppm', '*.PPM', '*.eps', '*.EPS')),
				(_('Portable Network Graphics files - *.png'), ('*.png', '*.PNG')),
				(_('Encapsulated PostScript files - *.eps'), ('*.eps', '*.EPS')),
				(_('JPEG files - *.jpg *jpeg'), ('*.jpg', '*.JPG', '*.jpeg', '*.JPEG')),
				(_('TIFF files - *.tif *.tiff'), ('*.tif', '*.TIF', '*.tiff', '*.TIFF')),
				(_('CompuServ Graphics files - *.gif'), ('*.gif', '*.GIF')),
				(_('Adobe Photoshop files (up to v.3.0) - *.psd'), ('*.psd', '*.PSD')),
				(_('Windows Bitmap files - *.bmp'), ('*.bmp', '*.BMP')),
				(_('Paintbrush files - *.pcx'), ('*.pcx', '*.PCX')),
				(_('Portable Bitmap files - *.pbm'), ('*.pbm', '*.PBM')),
				(_('Portable Graymap files - *.pgm'), ('*.pgm', '*.PGM')),
				(_('Portable Pixmap files - *.ppm'), ('*.ppm', '*.PPM')),
				(_("All Files"), 	 '*'))

palette_types = ((_("sK1 color swatch palette"), ('*.skp', '*.SKP')),
				(_("All Files"), 	 '*'))

pdf_types = ((_("Portable Document Format (PDF 1.5) - *.pdf"), ('*.pdf', '*.PDF')),
				(_("All Files"), 	 '*'))

png_types = ((_('Portable Network Graphics files - *.png'), ('*.png', '*.PNG')),
				(_("All Files"), 	 '*'))

SAVEMODE = 1
OPENMODE = 0

def convert_for_gtk2(filetypes):
	'''This function converts filetypes tuple into string format
	useful for gtk2 dialogs.
	'''
	result = ''
	for filetype in filetypes:
		descr = filetype[0]
		extentions = filetype[1]
		ext = ''
		for extention in extentions:
			ext += extention + ' '
		result += descr + '|' + ext + '@'
	return result

class DialogManager:
	root = None
	dialogObject = None
	def __init__(self, root):
		self.root = root
		self.app_icon = os.path.join(app.config.sk_share_dir, 'images')
		self.app_icon = os.path.join(self.app_icon, 'sk1-app-icon.png')

	def get_dialog_type(self, mode):
		if mode == SAVEMODE: return Gtk2_GetSaveFilename
		if mode == OPENMODE: return Gtk2_GetOpenFilename

	def launchBrowserURL(self, url):
		import webbrowser
		webbrowser.open_new(url)

	def getGenericOpenFilename(self, title, filetypes, **kw):
		name = app.config.name
		kw['filetypes'] = filetypes
		dialog_type = self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getOpenFilename(self, **kw):
		name = app.config.name
		title = _('Open file')
		kw['filetypes'] = openfiletypes
		dialog_type = self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getImportFilename(self, **kw):
		name = app.config.name
		title = _('Import drawing')
		kw['filetypes'] = importfiletypes
		dialog_type = self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getImportBMFilename(self, **kw):
		name = app.config.name
		title = _('Import bitmap')
		kw['filetypes'] = imagefiletypes
		dialog_type = self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getGenericSaveFilename(self, title, filetypes, **kw):
		name = app.config.name
		if not title: title = _('Save file')
		kw['filetypes'] = filetypes
		dialog_type = self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getSaveFilename(self, **kw):
		name = app.config.name
		title = _('Save file')
		kw['filetypes'] = savefiletypes
		dialog_type = self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getSaveAsFilename(self, **kw):
		name = app.config.name
		title = _('Save file As...')
		kw['filetypes'] = savefiletypes
		dialog_type = self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getExportFilename(self, **kw):
		name = app.config.name
		title = _('Export drawing')
		kw['filetypes'] = exportfiletypes
		dialog_type = self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getExportBMFilename(self, **kw):
		name = app.config.name
		title = _('Export drawing as a bitmap')
		kw['filetypes'] = imagefiletypes
		dialog_type = self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def dialog_thread(self, dialog_type, name, title, **kw):
		return apply(dialog_type, (self.root, name, title, self.app_icon), kw)

def check_initialdir(initialdir):
	if not os.path.exists(initialdir):
		return '~'
	else:
		return initialdir

def Gtk2_GetOpenFilename(master, name, title, icon, **kw):
	''' Calls Gtk2 open file dialog.   
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	
	Returns: tuple of utf8 and system encoded file names
	'''
	initialdir = check_initialdir(kw['initialdir'])
	master.update()
	filetypes = convert_for_gtk2(kw['filetypes'])
	name += ' - ' + title

	tmpfile = NamedTemporaryFile()
	execline = ''
	if sk1.LANG: execline += 'export LANG=' + sk1.LANG + ';'
	execline += 'python %s/gtk/open_file_dialog.py ' % (PATH,)
	execline += ' caption="' + name + '" start_dir="' + initialdir + '"'
	execline += ' filetypes="' + filetypes + '" window-icon="' + icon + '"'
	os.system(execline + '>' + tmpfile.name)
	result = tmpfile.readline().strip()
	return (result, result)

def Gtk2_GetSaveFilename(master, name, title, icon, **kw):
	''' Calls Gnome open file dialog.   
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	initialfile - file name
	
	Returns: tuple of utf8 and system encoded file names
	'''
	initialdir = check_initialdir(kw['initialdir'])
	initialfile = ''
	if kw['initialfile']: initialfile = kw['initialfile']

	filetypes = convert_for_gtk2(kw['filetypes'])
	name += ' - ' + title

	tmpfile = NamedTemporaryFile()
	execline = ''
	if sk1.LANG: execline += 'export LANG=' + sk1.LANG + ';'
	path = os.path.join(initialdir, initialfile)
	execline += 'python %s/gtk/save_file_dialog.py ' % (PATH,)
	execline += ' caption="' + name + '" path="' + path + '" '
	execline += ' filetypes="' + filetypes + '" window-icon="' + icon + '"'
	os.system(execline + '>' + tmpfile.name)
	result = tmpfile.readline().strip()
	return (result, result)
