# -*- coding: utf-8 -*-

# Routines for Tk and Ttk icon management

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

import os, sk1sdk
from sk1sdk import tkpng
from uc.utils import fs

BUILT_IN='Built-in'

def load_builtin_icons(widget):
	"""
	Loads default iconset.
	
	widget - any Tk widget for tk interpreter call
	"""
	load_icons(widget, os.path.join(sk1sdk.__path__[0],'tkstyle','icons','CrystalSVG'))

def load_icons(widget,path=BUILT_IN):
	"""
	Loads iconset from provided path.
	
	widget - any Tk widget for tk interpreter call
	path - full path to iconset	
	"""
	if path==BUILT_IN:		
		load_builtin_icons(widget)
		return 
	icons=fs.get_files_tree(os.path.join(path,'application'))
	_load_icons(widget,icons)	
	icons=fs.get_files_tree(os.path.join(path,'mimetypes'))
	_load_icons(widget,icons)
	sk1sdk.tkstyle.MIME_MAP=_load_mime_map(path)


def _load_icons(widget,icons):
	"""
	Internal routine for bulk icon loading.
	
	widget - any Tk widget for tk interpreter call
	icons - icon path list
	"""
	for icon in icons:
		item=os.path.basename(icon)[:-4]
		tkpng.load_icon(widget, icon, item)	
	
def _load_mime_map(path):
	"""
	Internal routine for mime map loading.
	"""
	lines=[]
	result={}	
	file=open(os.path.join(path,'mimes.map'),'rb')
	while 1:
		line=file.readline()
		if line[-1:]=='\n':
			line=line[:-1]
		if line=='':
			break
		if not line[-1:]=='-':
			lines.append(line)
	file.close()
	
	for line in lines:
		words=line.split(' => ')
		result[words[0].strip()]=words[1].strip()
	return result
	
if __name__ == '__main__':
	from sk1sdk.libtk import Tkinter
	root=Tkinter.Tk()
	load_builtin_icons(root)
	label=Tkinter.Label(root, image='icon_sk1_64')
	label.pack()
	root.mainloop()
	
