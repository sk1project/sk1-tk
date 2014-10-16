# -*- coding: utf-8 -*-

# tkstyle - unified routines for Tk and Ttk widget Look & Feel
# setting

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

from colors import ColorScheme
from Tkinter import StringVar
import fonts, icons, themes, colors
import sk1sdk, os, sys

BUILT_IN = 'Built-in'

CURRENT_STYLE = None
PKGDIR = os.path.join(sk1sdk.__path__[0], 'tkstyle')
MIME_MAP = {}
INITIALIZED = False

class Style:
	"""
	The class represents preferences for UI styling.
	"""

	fonts = []
	colors = None
	iconset = None
	theme = None

	def __init__(self):	pass

def set_style(widget, style, correct_font=True):
	"""
	Applies style to application L&F.
	style - should be Style object.
	"""
	if not INITIALIZED: _init_styling(widget)
	sk1sdk.tkstyle.CURRENT_STYLE = style
	_apply_colors(widget, style)
	_apply_fonts(widget, style, correct_font)
	icons.load_icons(widget, style.iconset)
	themes.set_theme(widget, style.theme)


def get_system_style(widget):
	"""
	Returns system defined style.
	"""
	style = Style()
	style.colors = ColorScheme(colors.SYSTEM_SCHEME)
	style.fonts = fonts.get_system_fonts()
	style.iconset = BUILT_IN
	style.theme = BUILT_IN
	sk1sdk.tkstyle.CURRENT_STYLE = style
	return style

def get_builtin_style(widget):
	"""
	Returns built-in style.
	"""
	style = Style()
	style.colors = ColorScheme()
	style.fonts = fonts.get_builtin_fonts()
	style.iconset = BUILT_IN
	style.theme = BUILT_IN
	sk1sdk.tkstyle.CURRENT_STYLE = style
	return style

############## Global Tk variables ##################
sk1_bg = None
sk1_fg = None
sk1_highlightbg = None
sk1_highlightcolor = None
sk1_disabledfg = None
sk1_selectbg = None
sk1_selectfg = None
sk1_txtsmall = None
sk1_txtnormal = None
sk1_txtlarge = None
#####################################################

def _init_styling(widget):
	sk1sdk.tkstyle.sk1_bg = StringVar(widget, name='sk1_bg')
	sk1sdk.tkstyle.sk1_fg = StringVar(widget, name='sk1_fg')
	sk1sdk.tkstyle.sk1_highlightbg = StringVar(widget, name='sk1_highlightbg')
	sk1sdk.tkstyle.sk1_highlightcolor = StringVar(widget, name='sk1_highlightcolor')
	sk1sdk.tkstyle.sk1_disabledfg = StringVar(widget, name='sk1_disabledfg')
	sk1sdk.tkstyle.sk1_selectbg = StringVar(widget, name='sk1_selectbg')
	sk1sdk.tkstyle.sk1_selectfg = StringVar(widget, name='sk1_selectfg')
	sk1sdk.tkstyle.sk1_txtsmall = StringVar(widget, name='sk1_txtsmall')
	sk1sdk.tkstyle.sk1_txtnormal = StringVar(widget, name='sk1_txtnormal')
	sk1sdk.tkstyle.sk1_txtlarge = StringVar(widget, name='sk1_txtlarge')
	sk1sdk.tkstyle.INITIALIZED = True

def _apply_colors(widget, style):
	color_scheme = style.colors
	sk1sdk.tkstyle.sk1_bg.set(color_scheme.bg)
	sk1sdk.tkstyle.sk1_fg.set(color_scheme.foreground)
	sk1sdk.tkstyle.sk1_highlightbg.set(color_scheme.highlightbackground)
	sk1sdk.tkstyle.sk1_highlightcolor.set(color_scheme.highlightcolor)
	sk1sdk.tkstyle.sk1_disabledfg.set(color_scheme.disabledforeground)
	sk1sdk.tkstyle.sk1_selectbg.set(color_scheme.selectbackground)
	sk1sdk.tkstyle.sk1_selectfg.set(color_scheme.selectforeground)

	widget.tk.call('tk_setPalette', color_scheme.bg)

	widget.tk.call('option', 'add', '*background', color_scheme.bg, 'interactive')
	widget.tk.call('option', 'add', '*foreground', color_scheme.foreground, 'interactive')
	widget.tk.call('option', 'add', '*selectForeground', color_scheme.selectforeground, 'interactive')
	widget.tk.call('option', 'add', '*selectBackground', color_scheme.selectbackground, 'interactive')
	widget.tk.call('option', 'add', '*highlightBackground', color_scheme.highlightbackground, 'interactive')
	widget.tk.call('option', 'add', '*highlightColor', color_scheme.highlightcolor, 'interactive')

	widget.tk.call('option', 'add', '*highlightThickness', '0', 'interactive')
	widget.tk.call('option', 'add', '*borderWidth', '0', 'interactive')

def _apply_fonts(widget, style, correct_font):
	font_list = style.fonts
	widget.tk.call('option', 'add', '*font', fonts.tkfont_from_list(font_list[1], correct_font))
	sk1_txtsmall.set(fonts.tkfont_from_list(font_list[0], correct_font))
	sk1_txtnormal.set(fonts.tkfont_from_list(font_list[1], correct_font))
	sk1_txtlarge.set(fonts.tkfont_from_list(font_list[2], correct_font))

