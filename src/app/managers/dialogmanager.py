# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import Tkinter, app, os, string, math
from app.utils import locale_utils

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
	def __init__(self):
		pass
	
	