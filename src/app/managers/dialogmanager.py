# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import app, os, string, math, string
from sk1libs.utils.system import getenv 
from sk1libs.utils.fs import gethome
from app import _
from sk1sdk.libtk.Tkinter import StringVar
from app.UI.dialogs.msgdialog import msgDialog


def convertForKdialog(filetypes):
	'''This function converts filetypes tuple into string
	in kdialog format
	'''
	result=''
	for filetype in filetypes:
		descr=filetype[0]
		extentions=filetype[1]
		for extention in extentions:
			result+=extention+' '
		result+='|'+descr+' \n'		
	return result

def convertForZenity(filetypes):
	'''This function converts filetypes tuple into string
	in zenity format
	'''
	result=''
	for filetype in filetypes:
		descr=filetype[0]
		extentions=filetype[1]	
		ext=''	
		for extention in extentions:
			ext+=extention+' '
		result+='--file-filter "'+descr+'|'+ext+'" '		
	return result


openfiletypes=((_('sK1 vector graphics files - *.sK1'),('*.sK1', '*.sk1', '*.SK1')),
				 (_("All Files"),	 '*'))		   

importfiletypes=((_('All supported files - *.sk1 *.sk *.ai *.eps *.cdr *.svg *.wmf etc. '),
				  ('*.sK1', '*.sk1', '*.SK1', '*.sk', '*.SK', '*.ai', '*.AI', '*.eps', '*.EPS', '*.ps', '*.PS',
					'*.cmx', '*.CMX', '*.cdr', '*.CDR', '*.cdt', '*.CDT', '*.ccx', '*.CCX', '*.cgm', 
					'*.CGM', '*.aff', '*.AFF', '*.svg', '*.SVG', '*.wmf', '*.WMF', '*.plt', '*.PLT', 
					'*.dxf', '*.DXF', '*.fig', '*.FIG')),
				 (_('sK1 vector graphics files - *.sk1'),('*.sK1', '*.sk1', '*.SK1')),
				 (_('Sketch\Skencil files - *.sk'),('*.sk', '*.SK')),
				 (_('Adobe Illustrator files (up to ver. 9.0) - *.ai'),('*.ai', '*.AI')),
				 (_('Encapsulated PostScript files - *.eps'),('*.eps', '*.EPS')),
				 (_('PostScript files - *.ps'),('*.ps', '*.PS')),
				 (_('CorelDRAW Graphics files (7-X4 ver.) - *.cdr'),('*.cdr', '*.CDR')),
				 (_('CorelDRAW Templates files (7-X4 ver.) - *.cdt'),('*.cdt', '*.CDT')),
				 (_('CorelDRAW Presentation Exchange files - *.cmx'),('*.cmx', '*.CMX')),
				 (_('CorelDRAW Compressed Exchange files (CDRX format) - *.ccx'),('*.ccx', '*.CCX')),
				 (_('Computer Graphics Metafile files - *.cgm'),('*.cgm', '*.CGM')),
				 (_('Acorn Draw files - *.aff'),('*.aff', '*.AFF')),
				 (_('Scalable Vector Graphics files - *.svg'),('*.svg', '*.SVG')),
				 (_('Windows Metafile files - *.wmf'),('*.wmf', '*.WMF')),
				 (_('HPGL cutting plotter files - *.plt'),('*.plt', '*.PLT')),
				 (_('AutoCAD DXF files - *.dxf'),('*.dxf', '*.DXF')),				 
				 (_('XFig files - *.fig'),('*.fig', '*.FIG')),
				 (_("All Files"),	 '*'))

savefiletypes=((_('sK1 vector graphics files - *.sK1'),('*.sK1', '*.sk1', '*.SK1')),)

exportfiletypes=((_('sK1 vector graphics files - *.sK1'),('*.sK1', '*.sk1', '*.SK1')),
				 (_('Sketch and Skencil files - *.sk'),('*.sk', '*.SK')),
				 (_('Adobe Illustrator files (ver. 5.0) - *.ai'),('*.ai', '*.AI')),
				 (_('Portable Document Format (PDF 1.5) - *.pdf'),('*.pdf', '*.PDF')),
				 (_('PostScript - *.ps'),('*.ps', '*.PS')),
				 (_('Computer Graphics Metafile files - *.cgm'),('*.cgm', '*.CGM')),
				 (_('Scalable Vector Graphics files - *.svg'),('*.svg', '*.SVG')),
				 (_('Windows Metafile files - *.wmf'),('*.wmf', '*.WMF')),
				 (_('HPGL cutting plotter files - *.plt'),('*.plt', '*.PLT')),
				 (_("All Files"),	 '*'))

imagefiletypes=((_('All supported files - *.png *.jpg *.tif *.gif *.psd *.bmp *.pcx etc.'),
				 ('*.png', '*.PNG', '*.gif', '*.GIF', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.tif', '*.TIF',
				  '*.tiff', '*.TIFF', '*.bmp', '*.BMP', '*.pcx', '*.PCX', '*.pbm', '*.PBM',
				  '*.pgm', '*.PGM', '*.ppm', '*.PPM', '*.eps', '*.EPS')),
				(_('Portable Network Graphics files - *.png'),('*.png', '*.PNG')),
				(_('Encapsulated PostScript files - *.eps'),('*.eps', '*.EPS')),
				(_('JPEG files - *.jpg *jpeg'),('*.jpg', '*.JPG', '*.jpeg', '*.JPEG')),
				(_('TIFF files - *.tif *.tiff'),('*.tif', '*.TIF', '*.tiff', '*.TIFF')),
				(_('CompuServ Graphics files - *.gif'),('*.gif', '*.GIF')),
				(_('Adobe Photoshop files (up to v.3.0) - *.psd'),('*.psd', '*.PSD')),
				(_('Windows Bitmap files - *.bmp'),('*.bmp', '*.BMP')),
				(_('Paintbrush files - *.pcx'),('*.pcx', '*.PCX')),
				(_('Portable Bitmap files - *.pbm'),('*.pbm', '*.PBM')),
				(_('Portable Graymap files - *.pgm'),('*.pgm', '*.PGM')),
				(_('Portable Pixmap files - *.ppm'),('*.ppm', '*.PPM')),
				(_("All Files"),	 '*'))

palette_types = ((_("sK1 color swatch palette"), ('*.skp', '*.SKP')),
				(_("All Files"),	 '*'))

pdf_types = ((_("Portable Document Format (PDF 1.5) - *.pdf"), ('*.pdf', '*.PDF')),
				(_("All Files"),	 '*'))

KDE_DIALOG=1
GNOME_DIALOG=2
TK_DIALOG=3

SAVEMODE=1
OPENMODE=0

UNKNOWN_DESKTOP=0
KDE_DESKTOP=1
GNOME_DESKTOP=2

class DialogManager:
	#0- unknown; 1- KDE; 2- Gnome
	root=None
	desktop=UNKNOWN_DESKTOP
	dialogObject=None
	is_kdialog=0
	is_zenity=0
	is_konqueror=0
	is_firefox=0
	is_mozilla=0
	is_opera=0
	is_kprinter=0
	def __init__(self, root):
		self.root=root
		self.check_enviroment()
		self.validate_binaries()
		self.app_icon=os.path.join(app.config.user_icons,app.config.preferences.icons)
		self.app_icon=os.path.join(self.app_icon, 'icon_sk1_16.png')
	
	def check_enviroment(self):
		ds=getenv('DESKTOP_SESSION')
		if ds:
			if string.find(string.upper(ds), 'KDE')>0:
				self.desktop=KDE_DESKTOP
			else:
				if string.find(string.upper(ds), 'GNOME')>0:
					self.desktop=GNOME_DESKTOP
				else:
					self.desktop=UNKNOWN_DESKTOP
		else:
			self.desktop=UNKNOWN_DESKTOP
	
	def validate_binaries(self):
		if os.system('which kdialog>/dev/null 2>/dev/null'):
			self.is_kdialog=0
		else:
			self.is_kdialog=1
		if os.system('which zenity>/dev/null 2>/dev/null'):
			self.is_zenity=0
		else:
			self.is_zenity=1
		if os.system('which konqueror>/dev/null 2>/dev/null'):
			self.is_konqueror=0
		else:
			self.is_konqueror=1
		if os.system('which firefox>/dev/null 2>/dev/null'):
			self.is_firefox=0
		else:
			self.is_firefox=1
		if os.system('which mozilla>/dev/null 2>/dev/null'):
			self.is_mozilla=0
		else:
			self.is_mozilla=1
		if os.system('which opera>/dev/null 2>/dev/null'):
			self.is_opera=0
		else:
			self.is_opera=1		
		if os.system('which kprinter>/dev/null 2>/dev/null'):
			self.is_kprinter=0
		else:
			self.is_kprinter=1		
			
	def get_dialog_type(self, mode):
		dialog_mode=app.config.preferences.dialog_type
		if not dialog_mode:
			if not self.desktop:
				dialog_type=TK_DIALOG
			else:
				dialog_type=self.desktop	
				
			if dialog_type==TK_DIALOG and self.is_zenity==1:
				dialog_type=GNOME_DIALOG
				
			if dialog_type==TK_DIALOG and self.is_kdialog==1:
				dialog_type=KDE_DIALOG
		else:
			dialog_type=dialog_mode
			
		if dialog_type==KDE_DIALOG and self.is_kdialog==0:
			dialog_type=TK_DIALOG
		if dialog_type==GNOME_DIALOG and self.is_zenity==0:
			dialog_type=TK_DIALOG

							
		if mode==SAVEMODE:
			if dialog_type==KDE_DIALOG:
				return KDE_GetSaveFilename
			if dialog_type==GNOME_DIALOG:
				return Gnome_GetSaveFilename
			if dialog_type==TK_DIALOG:
				return TkGetSaveFilename
		if mode==OPENMODE:
			if dialog_type==KDE_DIALOG:
				return KDE_GetOpenFilename
			if dialog_type==GNOME_DIALOG:
				return Gnome_GetOpenFilename
			if dialog_type==TK_DIALOG:
				return TkGetOpenFilename
			
	def launchBrowserURL(self,url):
		if self.is_konqueror:
			os.spawnlp(os.P_NOWAIT, 'konqueror', 'konqueror', url)
		elif self.is_firefox:
			os.spawnlp(os.P_NOWAIT, 'firefox', 'firefox', url)
		elif self.is_mozilla:
			os.spawnlp(os.P_NOWAIT, 'mozilla', 'mozilla', url)
		elif self.is_opera:
			os.spawnlp(os.P_NOWAIT, 'opera', 'opera','-newpage', url)
		else:
			msgDialog(self.root, 
					title = _("Browser not found"), 
					message=_("sK1 has checked presence of following browsers:\n" +
							'konqueror, firefox, mozilla, opera\n' +
							_("and all the browsers are absent in the system!\n")+
							_("Please consider installing browser in your system.")))
			
	def getGenericOpenFilename(self, title, filetypes, **kw):
		name=app.config.name
		kw['filetypes']=filetypes
		dialog_type=self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
			
	def getOpenFilename(self, **kw):
		name=app.config.name
		title=_('Open file')
		kw['filetypes']=openfiletypes
		dialog_type=self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
	
	def getImportFilename(self, **kw):
		name=app.config.name
		title=_('Import drawing')
		kw['filetypes']=importfiletypes
		dialog_type=self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
	
	def getImportBMFilename(self, **kw):
		name=app.config.name
		title=_('Import bitmap')
		kw['filetypes']=imagefiletypes
		dialog_type=self.get_dialog_type(OPENMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getGenericSaveFilename(self, title, filetypes,  **kw):
		name=app.config.name
		kw['filetypes']=filetypes
		dialog_type=self.get_dialog_type(SAVEMODE)
		if dialog_type==Gnome_GetSaveFilename:
			title=_('Save file As...')
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
	
	def getSaveFilename(self, **kw):
		name=app.config.name
		title=_('Save file')
		kw['filetypes']=savefiletypes
		dialog_type=self.get_dialog_type(SAVEMODE)
		if dialog_type==Gnome_GetSaveFilename:
			title=_('Save file As...')
		return apply(self.dialog_thread, (dialog_type, name, title), kw)

	def getSaveAsFilename(self, **kw):
		name=app.config.name
		title=_('Save file As...')
		kw['filetypes']=savefiletypes
		dialog_type=self.get_dialog_type(SAVEMODE)
		#return apply(dialog_type, (self.root, name, title, self.app_icon), kw)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
	
	def getExportFilename(self, **kw):
		name=app.config.name
		title=_('Export drawing')
		kw['filetypes']=exportfiletypes
		dialog_type=self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
	
	def getExportBMFilename(self, **kw):
		name=app.config.name
		title=_('Export drawing as a bitmap')
		kw['filetypes']=imagefiletypes
		dialog_type=self.get_dialog_type(SAVEMODE)
		return apply(self.dialog_thread, (dialog_type, name, title), kw)
	
	def dialog_thread(self, dialog_type, name, title,  **kw):
		return apply(dialog_type, (self.root, name, title, self.app_icon), kw)

def check_initialdir(initialdir):
	if not os.path.exists(initialdir):
		return gethome()
	else:
		return initialdir
	
def TkGetOpenFilename(master, name, title, icon, **kw):
	''' Calls regular Tk open file dialog.
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	filetypes - tuple of file types (see examples in the package)
	
	Returns: tuple of utf8 and system encoded file names
	'''
	kw['title']=name+' - '+title
	kw['initialdir']=check_initialdir(kw['initialdir'])
	filename = apply(master.tk.call, ('tk_getOpenFile', '-parent', master._w) + master._options(kw))
	return (filename, master.tk.utf8_to_system(filename))

def TkGetSaveFilename(master, name, title, icon, **kw):
	''' Calls regular Tk save file dialog.
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	initialfile - file name
	filetypes - tuple of file types (see examples in the package)
	
	Returns: tuple of utf8 and system encoded file names
	'''
	kw['title']=name+' - '+title
	kw['initialdir']=check_initialdir(kw['initialdir'])
	filename = apply(master.tk.call, ('tk_getSaveFile', '-parent', master._w) + master._options(kw))
	return (filename, master.tk.utf8_to_system(filename))

def KDE_GetOpenFilename(master, name, title, icon, **kw):
	''' Calls KDE open file dialog.
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	filetypes - tuple of file types (see examples in the package)
	
	Returns: tuple of utf8 and system encoded file names
	'''
	initialdir=check_initialdir(kw['initialdir'])
	filetypes=convertForKdialog(kw['filetypes'])
	winid=str(master.winfo_id())
	execline=StringVar(master, name='execline')
	execline.set('kdialog --title "'+name+
					  '" --caption "'+title+'" --attach '+winid+
					  ' --name "'+name+'" --icon "'+icon+
					  '" --getopenfilename "'+initialdir+'" "'+ filetypes+' "')
	filename=master.tk.call('::desktop_integration::launch_dialog')
	return (master.tk.system_to_utf8(filename), filename)

def KDE_GetSaveFilename(master, name, title, icon, **kw):
	''' Calls KDE save file dialog.   
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	filetypes - tuple of file types (see examples in the package)
	
	Returns: tuple of utf8 and system encoded file names
	'''
	initialdir=check_initialdir(kw['initialdir'])
	filetypes=convertForKdialog(kw['filetypes'])	
	winid=str(master.winfo_id())
	execline=StringVar(master, name='execline')
	execline.set('kdialog --title "'+name+
					  '" --caption "'+title+'" --attach "'+winid+
					  '" --name "'+name+'" --icon "'+icon+
					  '" --getsavefilename "'+initialdir+'" "'+ filetypes+'"')
	filename=master.tk.call('::desktop_integration::launch_dialog')
	return (master.tk.system_to_utf8(filename), filename)

def Gnome_GetOpenFilename(master, name, title, icon, **kw):
	''' Calls Gnome open file dialog.   
	Parameteres:
	master - parent window
	name - application name
	title - dialog title
	**kw:
	initialdir - absolute path to initial dir
	
	Returns: tuple of utf8 and system encoded file names
	'''
	initialdir=string.replace(check_initialdir(kw['initialdir']),' ','\ ')
	master.update()
	filetypes=convertForZenity(kw['filetypes'])
	winid=str(master.winfo_id())
	name+=' - '+title
	name=string.replace(name,' ','\ ')
	icon=string.replace(icon,' ','\ ')
	execline=StringVar(master, name='execline')
	execline.set('zenity --file-selection --name='+name+' --filename='+initialdir+'/ '+filetypes+'--window-icon='+icon)
	filename=master.tk.call('::desktop_integration::launch_dialog')
	return (master.tk.system_to_utf8(filename), filename)

def Gnome_GetSaveFilename(master, name, title, icon, **kw):
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
	initialdir=string.replace(check_initialdir(kw['initialdir']),' ','\ ')
	if kw['initialfile']:
		initialfile=string.replace(kw['initialfile'],' ','\ ')
	else:
		initialfile=''
	winid=str(master.winfo_id())	
	filetypes=convertForZenity(kw['filetypes'])
	name+=' - '+title
	name=string.replace(name,' ','\ ')
	icon=string.replace(icon,' ','\ ')
	execline=StringVar(master, name='execline')
	execline.set('zenity --file-selection --save --name="'+name+'" --filename='+os.path.join(initialdir,initialfile)+' '+filetypes+' --window-icon='+icon+' --confirm-overwrite')	
	filename=master.tk.call('::desktop_integration::launch_dialog')
	return (master.tk.system_to_utf8(filename), filename)

