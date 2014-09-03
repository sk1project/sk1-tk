# -*- coding: utf-8 -*-

# tkpng - small wrapper for Tcl package tkpng
# This package works faster for bulk icons uploading
# then PIL tkimage (see comments in tkimage) and allows
# creating named icons.

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

import sk1sdk

INIT_FLAG=False

def init_tkpng(widget):
	"""
	Initiates tkpng package. Executed automatically at first
	request to this python package.
	widget - any tcl/tk widget. Needed for tcl interpreter call.
	"""	
	if not sk1sdk.tkpng.INIT_FLAG:
		widget.tk.call('lappend', 'auto_path', sk1sdk.__path__[0])
		widget.tk.call('package', 'require', 'tkpng')
		sk1sdk.tkpng.INIT_FLAG=True

def load_icon(widget, path, name):
	"""
	Loads PNG image as a named icon.
	Note that routine doesn't check icon name reservation. So if the name
	has been reserved the routine will overwrite icon (can be useful for 
	iconset changing on the fly).
	widget - any tcl/tk widget. Needed for tcl interpreter call.
	path - full qualified path to PNG file.
	name - name of uploaded icon.
	"""
	if not sk1sdk.tkpng.INIT_FLAG:
		init_tkpng(widget)
	widget.tk.call('image', 'create', 'photo', name, '-format', 'png', '-file', path)