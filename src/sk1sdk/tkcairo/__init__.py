# -*- coding: utf-8 -*-

# tkcairo -  extension for pycairo context initialization
# for Tkinter widgets under X.org
# Copyright (C) 2014 by Igor E.Novikov
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

import _tkcairo

def create_context(widget):
	"""Creates cairo context for provided widget
	
	INPUT VALUES: widget - target widget	
	RETURN: pycairo context 
	"""
	winname = widget._w
	interpaddr = widget.tk.interpaddr()
	w = widget.winfo_width()
	h = widget.winfo_height()
	return _tkcairo.create_pycairo_context(winname, interpaddr, w, h)
