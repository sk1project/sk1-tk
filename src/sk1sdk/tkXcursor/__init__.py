 
# -*- coding: utf-8 -*-

# tkXcursor -  RGBA/animated cursor management extension 
#for Tkinter widgets under X.org

#Copyright (c) 2009 by Igor E.Novikov
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

import os
import _tkXcursor

class tkXcursorError(Exception):
    pass

def is_xcursor_supported(widget):
	"""
	Checks is ARGB/animated cursor supported in the system.
	
	RETURN VALUE
	the function returns true/false depending on ARGB/animated cursor system support.
	"""
	if _tkXcursor.IsSupportedARGB(widget._w, widget.tk.interpaddr()):
		return True
	return False

def load_cursor(widget, filename):
	"""Loads custom RGBA/animated Xcursor from resource file
	
	INPUT VALUES
	widget - any instantiated widget or toplevel
	filename - absolute or relative path to Xcursor resource file
	
	RETURN VALUE
	the function returns integer value which corresponds cursor XID on X11 side
	"""
	if not os.path.isfile(filename):
		raise tkXcursorError('Xcursor resource file is missing: '+filename)
	return _tkXcursor.FilenameLoadCursor(widget._w, widget.tk.interpaddr(), filename)

def set_cursor(widget, cursor_id):
	"""Sets custom RGBA/animated Xcursor for provided widget
	
	INPUT VALUES
	widget - target widget
	cursor_id - integer value which corresponds cursor XID on X11 side
	"""
	_tkXcursor.SetCursor(widget._w, widget.tk.interpaddr(), cursor_id)

