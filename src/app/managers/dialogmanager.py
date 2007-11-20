# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import Tkinter, app, os, string, math
from app.utils import os_utils
from app.utils import locale_utils
from app import _



openfiletypes=((_('sK1 vector graphics files - *.sK1'),('*.sK1', '*.sk1', '*.SK1')))

importfiletypes=((_('All supported files - *.sk1 *.sk *.ai *.eps *.cdr *.svg *.wmf etc. '),
				  ('*.sK1', '*.sk1', '*.SK1', '*.sk', '*.SK', '*.ai', '*.AI', '*.eps', '*.EPS', '*.ps', '*.PS',
					'*.cmx', '*.CMX', '*.cdr', '*.CDR', '*.cdt', '*.CDT', '*.ccx', '*.CCX', '*.cgm', 
					'*.CGM', '*.aff', '*.AFF', '*.svg', '*.SVG', '*.wmf', '*.WMF', '*.fig', '*.FIG')),
				 (_('sK1 vector graphics files - *.sk1'),('*.sK1', '*.sk1', '*.SK1')),
				 (_('Sketch\Skencil files - *.sk'),('*.sk', '*.SK')),
				 (_('Adobe Illustrator files (up to ver. 9.0) - *.ai'),('*.ai', '*.AI')),
				 (_('Encapsulated PostScript files - *.eps'),('*.eps', '*.EPS')),
				 (_('PostScript files - *.ps'),('*.ps', '*.PS')),
				 (_('CorelDRAW Graphics files (7-X3 ver.) - *.cdr'),('*.cdr', '*.CDR')),
				 (_('CorelDRAW Templates files (7-X3 ver.) - *.cdt'),('*.cdt', '*.CDT')),
				 (_('CorelDRAW Presentation Exchange files - *.cmx'),('*.cmx', '*.CMX')),
				 (_('CorelDRAW Compressed Exchange files (CDRX format) - *.ccx'),('*.ccx', '*.CCX')),
				 (_('Computer Graphics Metafile files - *.cgm'),('*.cgm', '*.CGM')),
				 (_('Acorn Draw files - *.aff'),('*.aff', '*.AFF')),
				 (_('Scalable Vector Graphics files - *.svg'),('*.svg', '*.SVG')),
				 (_('Windows Metafile files - *.wmf'),('*.wmf', '*.WMF')),				 
				 (_('XFig files - *.fig'),('*.fig', '*.FIG')))

savefiletypes=((_('sK1 vector graphics files - *.sK1'),('*.sK1', '*.sk1', '*.SK1')))

exportfiletypes=((_('sK1 vector graphics files - *.sK1'),('*.sK1', '*.sk1', '*.SK1')),
				 (_('Sketch and Skencil files - *.sk'),('*.sk', '*.SK')),
				 (_('Adobe Illustrator files (ver. 5.0) - *.ai'),('*.ai', '*.AI')),
				 (_('Computer Graphics Metafile files - *.cgm'),('*.cgm', '*.CGM')),
				 (_('Scalable Vector Graphics files - *.svg'),('*.svg', '*.SVG')),
				 (_('Windows Metafile files - *.wmf'),('*.wmf', '*.WMF')))

imagefiletypes=((_('All supported files - *.png *.jpg *.tif *.gif *.psd *.bmp *.pcx etc.'),
				 ('*.png', '*.PNG', '*.gif', '*.GIF', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.tif', '*.TIF',
				  '*.tiff', '*.TIFF', '*.gif', '*.GIF', '*.bmp', '*.BMP', '*.pcx', '*.PCX', '*.pbm', '*.PBM',
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
				(_('Portable Pixmap files - *.ppm'),('*.ppm', '*.PPM')))


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

class DialogManager:
	#0- unknown; 1- KDE; 2- Gnome app.config.preferences
	desktop=0
	dialogObject=None
	is_kdialog=0
	is_zenity=0
	def __init__(self, root):
		self.root=root
		self.check_enviroment()
		self.validate_binaries()
	
	def check_enviroment(self):
		ds=os_utils.getenv('DESKTOP_SESSION')
		if ds:
			if string.find(string.upper(ds), 'KDE')>0:
				self.desktop=1
			else:
				if string.find(string.upper(ds), 'GNOME')>0:
					self.desktop=2
				else:
					self.desktop=0
		else:
			self.desktop=0
	
	def validate_binaries(self):
		if os.path.isfile('/usr/bin/kdialog'):
			self.is_kdialog=1
		else:
			self.is_kdialog=0
		if os.system('zenity --help-misc>/dev/null'):
			self.is_zenity=0
		else:
			self.is_zenity=1	
	
	
	
	
	
	
	
	
	
	
	
	
#def imagefiletypes():
	#types=' \'*.png *.PNG *.gif *.GIF *.jpg *.JPG *.jpeg *.JPEG *.tif *.TIF' 
	#types=types+' *.tiff *.TIFF *.gif *.GIF *.bmp *.BMP *.pcx *.PCX *.pbm *.PBM'
	#types=types+' *.pgm *.PGM *.ppm *.PPM *.eps *.EPS'
	#types=types+'|All supported files - *.png *.jpg *.tif *.gif *.psd *.bmp *.pcx etc. \n'
	#types=types+' *.png *.PNG|Portable Network Graphics files - *.png \n'
	#types=types+' *.eps *.EPS|Encapsulated PostScript files - *.eps \n'
	#types=types+' *.jpg *.JPG *.jpeg *.JPEG|JPEG files - *.jpg *jpeg \n'
	#types=types+' *.tif *.TIF *.tiff *.TIFF|TIFF files - *.tif *.tiff \n'
	#types=types+' *.gif *.GIF|CompuServ Graphics files - *.gif \n'
	#types=types+' *.psd *.PSD|Adobe Photoshop files (up to v.3.0) - *.psd \n'
	#types=types+' *.bmp *.BMP|Windows Bitmap files - *.bmp \n'
	#types=types+' *.pcx *.PCX|Paintbrush files - *.pcx \n'
	#types=types+' *.pbm *.PBM|Portable Bitmap files - *.pbm \n'
	#types=types+' *.pgm *.PGM|Portable Graymap files - *.pgm \n'
	#types=types+' *.ppm *.PPM|Portable Pixmap files - *.ppm \''
	#return types
	
#def exportfiletypes():
	#types=' \'*.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sK1 \n'
	#types=types+' *.sk *.SK|Sketch and Skencil files - *.sk \n'
	#types=types+' *.ai *.AI|Adobe Illustrator files (ver. 5.0) - *.ai \n'
	#types=types+' *.cgm *.CGM|Computer Graphics Metafile files - *.cgm \n'
	#types=types+' *.svg *.SVG|Scalable Vector Graphics files - *.svg \n'
	#types=types+' *.wmf *.WMF|Windows Metafile files - *.wmf \''
	#return types	
	
#def savefiletypes():
	#types=' \'*.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sK1 \''
	#return types	
	
#def openfiletypes():
	#types=' \'*.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sK1 \''
	#return types 
	#(_(''),('')),

#def importfiletypes():
	#types=' \'*.sK1 *.sk1 *.SK1 *.sk *.SK *.ai *.AI *.eps *.EPS *.ps *.PS'
	#types=types+'*.cmx *.CMX *.cdr *.CDR *.cdt *.CDT *.ccx *.CCX'
	#types=types+'*.cgm *.CGM *.aff *.AFF *.svg *.SVG *.wmf *.WMF *.fig *.FIG'
	#types=types+'|All supported files - *.sk1 *.sk *.ai *.eps *.cdr *.svg *.wmf etc. \n'
	##Detalied extentions list
	#types=types+' *.sK1 *.sk1 *.SK1|sK1 vector graphics files - *.sk1 \n'
	#types=types+' *.sk *.SK|Sketch and Skencil files - *.sk \n'
	#types=types+' *.ai *.AI|Adobe Illustrator files (up to ver. 9.0) - *.ai \n'
	#types=types+' *.eps *.EPS|Encapsulated PostScript files - *.eps \n'
	#types=types+' *.ps *.PS|PostScript files - *.ps \n'
	#types=types+' *.cdr *.CDR|CorelDRAW Graphics files (7-X3 ver.) - *.cdr \n'
	#types=types+' *.cdt *.CDT|CorelDRAW Templates files (7-X3 ver.) - *.cdt \n'	
	#types=types+' *.cmx *.CMX|CorelDRAW Presentation Exchange files - *.cmx \n'
	#types=types+' *.ccx *.CCX|CorelDRAW Compressed Exchange files (CDRX format) - *.ccx \n'
	#types=types+' *.cgm *.CGM|Computer Graphics Metafile files - *.cgm \n'
	#types=types+' *.aff *.AFF|Acorn Draw files - *.aff \n'
	#types=types+' *.svg *.SVG|Scalable Vector Graphics files - *.svg \n'
	#types=types+' *.wmf *.WMF|Windows Metafile files - *.wmf \n'
	#types=types+' *.fig *.FIG|XFig files - *.fig \''
	#return types	
	
#imagefiletypes = ((_("All Files"), '*'),
				  #(_("Encapsulated PostScript"), ('.eps', '.ps')),
				  #(_("JPEG"),	('.jpg', '.jpeg')),
				  #(_("GIF"),	'.gif'),
				  #(_("Portable Bitmap"),	'.pbm'),
				  #(_("Portable Graymap"),	'.pgm'),
				  #(_("Portable Pixmap"),	'.ppm'),
				  #(_("TIFF"),	('.tif', '.tiff')),
				  #(_("Windows / OS/2 Bitmap"), '.bmp'),
				  #(_("PCX"),	'.pcx'))