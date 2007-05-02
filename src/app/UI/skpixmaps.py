# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2003 by Bernhard Herzog 
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
#	Pixmap/Bitmap handling stuff
#

import os

from app import config
from app.events.warn import warn, USER

_builtin = [ 'Transp', 'DPage1', 'DGrid', 'DGuidelines', 'Portrait', 'Landscape',
			'Corner',
			'JoinMiter', 'JoinRound', 'JoinBevel',
			'CapButt', 'CapRound', 'CapProjecting',
			'Duplicate', 'About',
			'Warning', 'Docinfo', 'Blend',
			'DocInfo',
			'sK1_icon', 'sK1_icon_mask', 'smallicon'
			]
#_align = ['AlignTop', 'AlignBottom', 'AlignCenterY', 'Align',
			#'AlignLeft', 'AlignRight', 'AlignCenterX']
#_align_dir='align'

_fill = ['fill_gradient', 'fill_hatch', 'fill_solid', 'fill_tile','fill_none',
			'gradient_linear', 'gradient_conical', 'gradient_radial']
_fill_dir='fill'

_layers = ['printable', 'non_printable', 'editable', 'non_editable', 'eye', 'non_eye',
				'fill', 'non_fill','LayerNew']
_layers_dir='layers'

_fastkeys = ['UngrAll', 'ToCurve', 'AddGuidesFrame', 'PFrame', 'RAG','FlipVertical', 'FlipHorizontal',
					'RotLeft','RotRight','Rot180', 'CCombine', 'Break', 'Group', 'Ungroup','DPage', 'DText',
					'Sizes', 'DNodes', 'Move', 'Rotate', 'Size']
_fastkeys_dir='fastkeys'

#_palette = ['ArrLeft', 'ArrRight', 'ArrArrLeft', 'ArrArrRight', 'NoPattern']
#_palette_dir='palette'

_nodes = ['BezierAngle', 'BezierSmooth', 'BezierSymm',
			'BezierDeleteNode', 'BezierInsertNode',
			'BezierCurveLine', 'BezierLineCurve',
			'BezierOpenNodes', 'BezierCloseNodes']
_nodes_dir='nodes'

#_toolbar = ['Triple','Mono','OpenNewDocument','NewDocument', 'Open', 'Save', 'SaveAs', 'Printer', 'QPrinter','Spacer', 'Spacer1',
			#'Undo', 'Redo', 'Delete', 'Copy', 'Paste', 'Cut', 'ImportVector', 'ImportImage',
			#'ExportV', 'ExportR','FitToPage', 'FitToNative', 'FitToSelected', 'ZoomIn', 'ZoomOut','BarEnd']
#_toolbar_dir='toolbar'

#_tools = ['SelectionMode', 'EditMode', 'Zoom', 'CreateRect', 'CreateEllipse', 'CreateCurve',
			#'CreatePoly', 'Text', 'FillButton', 'OutlineButton', 'MoveToTop', 'MoveToBottom',
			#'MoveOneUp', 'MoveOneDown', 'Tools']
#_tools_dir='tools'

#_statusbar = ['OnGrid', 'OnGuide', 'OnObject', 'Refresh','No_colors']
#_statusbar_dir='statusbar'

#_cursors = ['CurEdit', 'CurStd', 'CurStd1', 'CurZoom', 'CurUpDown', 'CurDown', 'CurUp']
_cursors = ['CurEdit', 'CurZoom']
_cursors_dir='cursors'

_canvas = ['TurnTL', 'TurnTR', 'TurnBL', 'TurnBR', 'Center',
				'ShearLR', 'ShearUD']
_canvas_dir='/canvas'

#_alias = [('Icon', 'sK1_icon'), ('Icon_mask', 'sK1_icon_mask')]


class SketchPixmaps:

	def InitFromWidget(self, widget, files, basedir):
		for name in files:
			file_base = os.path.join(basedir, name)
			try:
				pixmap = widget.ReadBitmapFile(file_base + '.xbm')[2]
				setattr(self, name, pixmap)
			except IOError, info:
				warn(USER, "Warning: Can't load Pixmap from %s: %s",
						file_base + '.xbm', info)


class PixmapTk:

	_cache = {}

	def load_image(self, name):
		import Tkinter
		if name[0] == '*':
			if config.preferences.color_icons:
				image = self._cache.get(name)
				if image is None:
					image = Tkinter.PhotoImage(file = name[1:], format = 'GIF')
					self._cache[name] = image
			else:
				image = '@' + name[1:-3] + 'xbm'
		else:
			image = name
		return image

	def clear_cache(self):
		self._cache.clear()

PixmapTk = PixmapTk()


def make_file_names(filenames, subdir = ''):
	default = 'error'	# a standard Tk bitmap
	for name in filenames:
		fullname = os.path.join(config.pixmap_dir, subdir, name)
		if os.path.exists(fullname + '.png'):
			setattr(PixmapTk, name, '*' + fullname + '.png')
		elif os.path.exists(fullname + '.gif'):
			setattr(PixmapTk, name, '*' + fullname + '.gif')
		elif os.path.exists(fullname + '.ppm'):
			setattr(PixmapTk, name, '@' + fullname + '.ppm')
		elif os.path.exists(fullname + '.xbm'):
			setattr(PixmapTk, name, '@' + fullname + '.xbm')
		else:
			warn(USER, "Warning: no file %s substituting '%s'",
					fullname, default)
			setattr(PixmapTk, name, default)

make_file_names(_builtin)
#make_file_names(_tools, _tools_dir)
#make_file_names(_toolbar, _toolbar_dir)
#make_file_names(_palette, _palette_dir)
#make_file_names(_statusbar, _statusbar_dir)
make_file_names(_layers, _layers_dir)
#make_file_names(_align, _align_dir)
make_file_names(_fastkeys, _fastkeys_dir)
make_file_names(_nodes, _nodes_dir)
make_file_names(_fill, _fill_dir)

def make_cursor_names(names, subdir = ''):
	from app.conf import const
	default = 'X_cursor'	# a standard X cursor
	for name in names:
		fullname = os.path.join(config.pixmap_dir, subdir, name + '.xbm')
		fullname_mask = os.path.join(config.pixmap_dir, subdir, name + '_mask.xbm')
		if os.path.exists(fullname) and os.path.exists(fullname_mask):
			setattr(const, name, ('@' + fullname, fullname_mask,
									'black', 'white'))
		else:
			warn(USER, "Warning: no file %s (or *_mask) substituting '%s'",
					fullname, default)
			setattr(const, name, default)

make_cursor_names(_cursors, _cursors_dir)

#def make_alias(aliases):
	#for alias, name in aliases:
		#setattr(PixmapTk, alias, getattr(PixmapTk, name))

#make_alias(_alias)

pixmaps = SketchPixmaps()


_init_done = 0
def InitFromWidget(widget):
	global _init_done
	if not _init_done:
		pixmaps.InitFromWidget(widget, _canvas, config.pixmap_dir + _canvas_dir)
