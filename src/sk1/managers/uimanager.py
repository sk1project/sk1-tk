# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import app, os
from sk1 import appconst
import Tkinter
from sk1sdk import tkstyle
from uc.utils import system


class UIManager:
	currentColorTheme = None
	root = None

	style = None

	def __init__(self, root=None):
		if not root:
			self.root = Tkinter._default_root
		else:
			self.root = root

		self.style = tkstyle.get_system_style(root)
		self.currentColorTheme = self.style.colors
		tkstyle.set_style(root, self.style, app.config.preferences.correct_font)
		self.uploadExtentions()
		self.defineCursors()

	def defineCursors(self):
		cur_dir = os.path.join(app.config.sk_share_dir, 'cursors')
		if system.get_os_family() == system.LINUX:
			from sk1sdk import tkXcursor
			if tkXcursor.is_xcursor_supported(self.root):
				cur_dir = os.path.join(cur_dir, 'xcursor')
				loader = tkXcursor.load_cursor
				setattr(appconst, 'CurStd', loader(self.root, os.path.join(cur_dir, 'cur_std.xcur')))
				setattr(appconst, 'CurEdit', loader(self.root, os.path.join(cur_dir, 'cur_edit.xcur')))
				setattr(appconst, 'CurZoom', loader(self.root, os.path.join(cur_dir, 'cur_zoom.xcur')))
				setattr(appconst, 'CurCreate', loader(self.root, os.path.join(cur_dir, 'cur_create.xcur')))
				setattr(appconst, 'CurCreateRect', loader(self.root, os.path.join(cur_dir, 'cur_create_rect.xcur')))
				setattr(appconst, 'CurCreateEllipse', loader(self.root, os.path.join(cur_dir, 'cur_create_ellipse.xcur')))
				setattr(appconst, 'CurCreatePolyline', loader(self.root, os.path.join(cur_dir, 'cur_create_polyline.xcur')))
				setattr(appconst, 'CurCreateBezier', loader(self.root, os.path.join(cur_dir, 'cur_create_bezier.xcur')))
				setattr(appconst, 'CurPick', loader(self.root, os.path.join(cur_dir, 'cur_pick.xcur')))
				setattr(appconst, 'CurText', loader(self.root, os.path.join(cur_dir, 'cur_text.xcur')))
				setattr(appconst, 'CurPlace', loader(self.root, os.path.join(cur_dir, 'cur_place.xcur')))
				setattr(appconst, 'CurHandle', loader(self.root, os.path.join(cur_dir, 'cur_handle.xcur')))
				setattr(appconst, 'CurHGuide', loader(self.root, os.path.join(cur_dir, 'cur_hguide.xcur')))
				setattr(appconst, 'CurVGuide', loader(self.root, os.path.join(cur_dir, 'cur_vguide.xcur')))
				setattr(appconst, 'CurMove', loader(self.root, os.path.join(cur_dir, 'cur_move.xcur')))
				setattr(appconst, 'CurCopy', loader(self.root, os.path.join(cur_dir, 'cur_copy.xcur')))

			else:
				cur_dir = os.path.join(cur_dir, 'xbm')
				setattr(appconst, 'CurEdit', ('@' + os.path.join(cur_dir, 'CurEdit.xbm'), 'black'))
				setattr(appconst, 'CurZoom', ('@' + os.path.join(cur_dir, 'CurZoom.xbm'), 'black'))
		elif system.get_os_family() == system.WINDOWS:
			pass
		elif system.get_os_family() == system.MACOSX:
			pass
		else:
			pass

	def uploadExtentions(self):
		tcl = os.path.join(app.config.sk1sdk_dir, 'tcl')
		self.root.tk.call('source', os.path.join(tcl, 'combobox.tcl'))
		self.root.tk.call('source', os.path.join(tcl, 'button.tcl'))
		self.root.tk.call('source', os.path.join(tcl, 'tkmenu.tcl'))
		self.root.tk.call('source', os.path.join(tcl, 'tkfbox.tcl'))
		self.root.tk.call('source', os.path.join(tcl, 'repeater.tcl'))
		self.root.tk.call('source', os.path.join(tcl, 'launch_dialog.tcl'))

	def setApplicationIcon(self, icon='icon_sk1_16', iconname='sK1'):
		self.root.iconname(iconname)
		self.root.tk.call('wm', 'iconphoto', self.root, icon)

	def maximizeApp(self):
		self.root.tk.call('wm', 'attributes', self.root, '-zoomed', 1)

	def center_root(self):
		w = self.root.winfo_screenwidth()
		h = self.root.winfo_screenheight()
		rootsize = (1024, 720)
		x = w / 2 - rootsize[0] / 2
		y = h / 2 - rootsize[1] / 2
		self.root.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))















