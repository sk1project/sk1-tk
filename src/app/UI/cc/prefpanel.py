# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from sk1sdk.libttk import TFrame, TLabel, TButton
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END
from app import _, config
import app

class PrefPanel(TFrame):
	
	name='PreferencePanel'
	title=_('Preference Panel')
	icon='pref_plugin'
	activated=0
	contents=[]
	
	def init(self, master):
		
		TFrame.__init__(self, master)
		
		##### Title #########################
		
		self.title_label=TLabel(self, text=self.title, font=config.preferences.large_font, justify=LEFT)
		self.title_label.pack(side=TOP, anchor=W)
		
		##### line #########################
				
		line = TLabel(self, style='HLine2')
		line.pack(side = TOP, fill = X)				

		##### here should be panel content #########################
		
		self.init_vars()		
		self.build()
		self.activated=1
		
	def init_vars(self):
		#Copies preferences to object fields
		pass
		
	def build(self):
		#builds panel UI
		pass
	
	def apply(self):
		#Applies changes
		pass
	
