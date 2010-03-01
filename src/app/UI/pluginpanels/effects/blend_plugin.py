# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Ttk import TFrame, TLabel, TCheckbutton, TButton
from Tkinter import IntVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect, mw
from app.conf import const
import app
from app.UI.tkext import UpdatedButton

from app.UI.pluginpanels.ppanel import PluginPanel

class BlendPlugin(PluginPanel):
	
	name='Blend'
	title = _("Blend")
	
	def init(self, master):
		PluginPanel.init(self, master)
		
		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)
		
		sign = TFrame(top, style='RoundedFrame', borderwidth=5)
		sign.pack(side = TOP)

		self.sign=TLabel(sign, image='shaping_divide')
		self.sign.pack(side=TOP)
		
		
		
		
instance=BlendPlugin()
app.effects_plugins.append(instance)