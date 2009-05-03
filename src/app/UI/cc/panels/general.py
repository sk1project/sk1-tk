# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from Ttk import TFrame, TLabel, TButton
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import _, config
import app
from app.UI.cc.prefpanel import PrefPanel

class GeneralOptionsPanel(PrefPanel):
	
	name='general'
	title=_('General Options')
	category='root'
	category_name=_('root')
	
	def build(self):		
		label=TLabel(self, text=self.__class__.name, font=config.preferences.large_font, justify=LEFT)
		label.pack(side=TOP, fill=X)
	
		
instance=GeneralOptionsPanel()
app.pref_plugins.append(instance)