# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import app, os, string, math
from app.conf import const
from sk1sdk.libtk import Tkinter
from sk1sdk import tkstyle
from sk1libs.utils import system 

	
class UIManager:
	currentColorTheme=None
	root=None
	
	style=None	

	def __init__(self, root=None):
		if not root:
			self.root = Tkinter._default_root
		else:
			self.root=root
		
		self.style=tkstyle.get_system_style(root)
		self.currentColorTheme=self.style.colors		
		tkstyle.set_style(root, self.style)
		self.uploadExtentions()
		self.defineCursors()
		
	def defineCursors(self):
		cur_dir=os.path.join(app.config.sk_share_dir,'cursors')
		if system.get_os_family()==system.LINUX:
			from sk1sdk import tkXcursor
			if tkXcursor.is_xcursor_supported(self.root):
				cur_dir=os.path.join(cur_dir,'xcursor')
				loader=tkXcursor.load_cursor
				setattr(const, 'CurStd', loader(self.root, os.path.join(cur_dir,'cur_std')))
				setattr(const, 'CurEdit', loader(self.root, os.path.join(cur_dir,'cur_edit')))
				setattr(const, 'CurZoom', loader(self.root, os.path.join(cur_dir,'cur_zoom')))
				setattr(const, 'CurCreate', loader(self.root, os.path.join(cur_dir,'cur_create')))
				setattr(const, 'CurCreateRect', loader(self.root, os.path.join(cur_dir,'cur_create_rect')))
				setattr(const, 'CurCreateEllipse', loader(self.root, os.path.join(cur_dir,'cur_create_ellipse')))
				setattr(const, 'CurCreatePolyline', loader(self.root, os.path.join(cur_dir,'cur_create_polyline')))
				setattr(const, 'CurCreateBezier', loader(self.root, os.path.join(cur_dir,'cur_create_bezier')))
				setattr(const, 'CurPick', loader(self.root, os.path.join(cur_dir,'cur_pick')))
				setattr(const, 'CurText', loader(self.root, os.path.join(cur_dir,'cur_text')))
				setattr(const, 'CurPlace', loader(self.root, os.path.join(cur_dir,'cur_place')))
				setattr(const, 'CurHandle', loader(self.root, os.path.join(cur_dir,'cur_handle')))
				setattr(const, 'CurHGuide', loader(self.root, os.path.join(cur_dir,'cur_hguide')))
				setattr(const, 'CurVGuide', loader(self.root, os.path.join(cur_dir,'cur_vguide')))
				setattr(const, 'CurMove', loader(self.root, os.path.join(cur_dir,'cur_move')))
				setattr(const, 'CurCopy', loader(self.root, os.path.join(cur_dir,'cur_copy')))
				
			else:
				cur_dir=os.path.join(cur_dir,'xbm')
				setattr(const, 'CurEdit', ('@' + os.path.join(cur_dir,'CurEdit.xbm'),'black'))
				setattr(const, 'CurZoom', ('@' + os.path.join(cur_dir,'CurZoom.xbm'),'black'))
		elif system.get_os_family()==system.WINDOWS:
			pass
		elif system.get_os_family()==system.MACOSX:
			pass
		else:
			pass
		
	def uploadExtentions(self):
		tcl=os.path.join(app.config.sk_dir,'app','tcl')
		self.root.tk.call('source', os.path.join(tcl,'combobox.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'button.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'tkmenu.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'tkfbox.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'repeater.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'launch_dialog.tcl'))
		
	def setApplicationIcon(self, icon='icon_sk1_16', iconname='sK1'):
		self.root.iconname(iconname)
		self.root.tk.call('wm', 'iconphoto', self.root, icon)
		
	def maximizeApp(self):
		self.root.tk.call('wm', 'attributes', self.root, '-zoomed', 1)	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
