# -*- coding: utf-8 -*-

# Routines for Tk and Ttk UI font management

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

import os, string, copy
from tempfile import NamedTemporaryFile

def get_builtin_fonts():
	"""
	Returns list of four predefined fonts, used in sK1 UI.
	"""
	return [
		['Sans', [], 9],
		['Sans', [], 10],
		['Sans', ['bold', ], 12],
		['Monospace', [], 10],
		]


def get_system_fonts():
	"""
	Returns list of four fonts, used in sK1 UI:
	[small_font,normal_font,large_font,fixed_font]
	Each font is a list like:
	[font_family,font_style,font_size]
	where:
	font_family - string representation of font family
	font_style - list of font styles like 'bold' and 'italic'
	font_size - font size integer value
	
	Currently Gtk binding is implemented. Win32 and MacOS X 
	implementation will be later.
	"""

	tmpfile = NamedTemporaryFile()
	command = "import gtk;w = gtk.Window();w.realize();style=w.get_style(); print style.font_desc.to_string();"
	os.system('python -c "%s" >%s 2>/dev/null' % (command, tmpfile.name))

	font = tmpfile.readline().strip()

	normal_font = process_gtk_font_string(font)
	small_font = copy.deepcopy(normal_font)
	small_font[2] -= 1

	large_font = copy.deepcopy(normal_font)
	large_font[2] += 2
	if not 'bold' in large_font[1]:
		large_font[1].append('bold')

	fixed_font = copy.deepcopy(normal_font)
	fixed_font[0] = 'monospace'

	return [small_font, normal_font, large_font, fixed_font]


def process_gtk_font_string(font):
	"""
	Converts Gtk font string to font description list
	So Gtk string like: San Serif Bold Italic 10
	will be: ['San\ Serif', ['bold','italic'], 10]
	Such form is much better for constructing of 
	Tk font description.
	"""

	font_style = []
	vals = font.split()
	font_size = int(vals[-1])
	vals.remove(vals[-1])
	if 'Bold' in vals:
		vals.remove('Bold')
		font_style.append('bold')
	if 'Italic' in vals:
		vals.remove('Italic')
		font_style.append('italic')
	font_family = string.join(vals, '\ ')
	if font_family == 'Ubuntu':font_family = 'Ubuntu\ Regular'
	return [font_family, font_style, font_size]

def tkfont_from_list(font_list, correct_font):
	"""
	Constructs tk font string from font list.
	"""
	delta = 0
	if correct_font:delta = 1
	return '%s %d ' % (font_list[0], font_list[2] - delta) + string.join(font_list[1])

if __name__ == '__main__':
	fonts = get_system_fonts()
	for item in fonts:
		print item
	print tkfont_from_list(['San\ Serif', ['bold', 'italic'], 10])


