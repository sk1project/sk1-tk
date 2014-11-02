# -*- coding: utf-8 -*-

# Routines for Ttk widget theme management

# Copyright (c) 2010 by Igor E.Novikov
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Library General Public
#License as published by the Free Software Foundation; either
#version 2 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Library General Public License for more details.
#
#You should have received a copy of the GNU Library General Public
#License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os, string, sk1sdk
from tempfile import NamedTemporaryFile
from sk1sdk import tkpng
from uc.utils import fs 
from PIL import Image

INITIALIZED=False
BUILT_IN='Built-in'
BUILTIN_THEME_PATH=os.path.join(sk1sdk.__path__[0],'tkstyle','themes')

def init_theme(widget,theme_parent_dir=BUILTIN_THEME_PATH):
	"""
	Routine for theme initialization. 
	"""
	widget.tk.call('lappend', 'auto_path', theme_parent_dir)

def set_builtin_theme(widget):
	"""
	Sets built-in widget theme.
	
	widget - any tk widget for tcl interpreter call
	"""
	_load_widget_templates(widget,os.path.join(BUILTIN_THEME_PATH,'Plastik','widgets'))
	_load_composite_templates(widget,os.path.join(BUILTIN_THEME_PATH,'Plastik','composite'))
	set_theme(widget, 'Plastik')
	
def set_theme(widget, theme_name):
	"""
	Sets specified widget theme.
	
	widget - any tk widget for tcl interpreter call
	"""
	if not INITIALIZED:
		init_theme(widget)
	if theme_name==BUILT_IN:
		set_builtin_theme(widget)
		return
	widget.tk.call('ttk::setTheme', theme_name)

if __name__ == '__main__':
	print os.path.join(sk1sdk.__path__[0],'tkstyle','themes')
	
def _load_widget_templates(widget,path):
	"""
	Recursively loads PNG templates.
	
	widget - any tk widget for tcl interpreter call
	path - full path to templates	
	"""
	icons=fs.get_files_tree(path,'png')
	for icon in icons:
		item=os.path.basename(icon)[:-4]
		tkpng.load_icon(widget, icon, item)
		
def _load_composite_templates(widget,path):
	"""
	Loads composite templates. This routine allows UI to look more native.
	
	widget - any tk widget for tcl interpreter call
	path - full path to templates
	"""
	files=fs.get_files(path,'png')
	for file in files:
		filename=file[:-4]
		action=filename.split('_')[-1]
		result=string.join(filename.split('_')[0:-1],'_')
		
		colors=sk1sdk.tkstyle.CURRENT_STYLE.colors
		
		mask=Image.open(os.path.join(path,file))
		mask.load()
		
		mask_color=colors.bg
		if action=='sel':
			mask_color=colors.selectbackground
		if action=='fg':
			mask_color=colors.foreground
			
		if action in ['sel','fg','bg']:
			color_plate=Image.new('RGB', mask.size, mask_color)
			color_plate.convert('RGBA')
			color_plate.putalpha(mask)
		
		if action=='bgmask':
			bgmask=Image.open(os.path.join(path,'masks',result+'_mask.png'))
			color_plate=Image.new('RGB', bgmask.size, mask_color)
			color_plate.convert('RGBA')
			color_plate.putalpha(bgmask)
			color_plate.paste(mask,(0,0), mask.split()[3])
			
		if action=='bgselmask':
			mask_color=colors.selectbackground
			bgmask=Image.open(os.path.join(path,'masks',result+'_mask.png'))
			selmask=Image.open(os.path.join(path,'masks',result+'_selmask.png'))
			color_sel=Image.new('RGB', bgmask.size, mask_color)
			color_sel.convert('RGBA')
			color_sel.putalpha(selmask)		
			
			mask_color=colors.bg
			color_plate=Image.new('RGB', bgmask.size, mask_color)
			color_plate.convert('RGBA')
			color_plate.putalpha(bgmask)
			color_plate.paste(mask,(0,0), mask.split()[3])
			color_plate.paste(color_sel,(0,0), color_sel.split()[3])
				
		
		imagefile=NamedTemporaryFile()
		color_plate.save(imagefile, 'PNG')
		
		tkpng.load_icon(widget, imagefile.name, result)
		
