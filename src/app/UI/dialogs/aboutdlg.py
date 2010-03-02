# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
import app, os, string, sys
from dialog import ModalDialog
from app import dialogman

from Ttk import TButton, TLabel, TFrame, TNotebook, TScrollbar
from app.UI.ttk_ext import TSpinbox
from sk1sdk.libtk.Tkinter import StringVar, Text, TclVersion
from sk1sdk.libtk.Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END, NONE


class AboutDialog(ModalDialog):

	class_name = 'AboutDialog'
	
	def __init__(self, master, dlgname = '__dialog__'):
		self.master=master
		self.title = _("About sK1")
		ModalDialog.__init__(self, master, name = dlgname)
	
	def build_dlg(self):
		self.root = TFrame(self.top, style='FlatFrame', borderwidth = 5)
		self.root.pack(side = TOP, fill = BOTH, expand = 1)
		
		panel = TFrame(self.root, style='FlatFrame', borderwidth = 5)		
		panel.pack(side = TOP, fill = X)
		
		icon=TLabel(panel, style='FlatLabel', image='icon_sk1_48')
		icon.pack(side = LEFT, padx=5,pady=5)
		
		panel = TFrame(panel, style='FlatFrame', borderwidth = 5)		
		panel.pack(side = LEFT)
		
		text=TLabel(panel, style='FlatLabel', text='sK1 v.%s'%app.sKVersion, 
				font=app.config.preferences.large_font+' bold')
		text.pack(side = TOP, anchor=W)
		
		text=TLabel(panel, style='FlatLabel', 
				text=_('Uses libraries: Tcl/Tk %s; Python %s')%
				(TclVersion, string.split(sys.version)[0]))
		text.pack(side = TOP, anchor=W)
		
		self.nb = TNotebook(self.root, height=150, width=500, padding=5)
		self.nb.pack(side = TOP, fill = BOTH, expand = 1)
				
		self.build_tab_about()
		self.build_tab_authors()
		self.build_tab_localization()
		self.build_tab_license()

		ok = TButton(self.root, text=_("Close"), command=self.ok)
		ok.pack(side = RIGHT, padx=5,pady=5)
		
		self.focus_widget = ok
		
		self.top.bind('<Escape>', self.cancel)
		self.top.protocol('WM_DELETE_WINDOW', self.cancel)
	
	def build_tab_about(self):	
		panel = TFrame(self.root, style='FlatFrame', borderwidth = 10)
		self.nb.add(panel, text='About application')

		subpanel = TFrame(panel, style='FlatFrame', borderwidth = 0)		
		subpanel.pack(side=TOP, fill=Y, expand = 1)
		
		subpanel = TFrame(subpanel, style='FlatFrame', borderwidth = 5)		
		subpanel.pack(side=LEFT,anchor='center')
		
		text=TLabel(subpanel, style='FlatLabel', 
				text=_("Illustration program for prepress"))
		text.pack(side = TOP, anchor=W,pady=10)
		
		from time import gmtime, strftime
		year=strftime("%Y", gmtime())
				
		text=TLabel(subpanel, style='FlatLabel', text="(c)2003-%s sK1 Team"%(year))
		text.pack(side = TOP, anchor=W,pady=10)
				
		text=TLabel(subpanel, style='FlatLabel', text='http://sk1project.org',
				foreground='blue', underline=20, cursor='hand2')
		text.pack(side = TOP, anchor=W)
		text.bind('<Button-1>', self.goToSite)
		
	def goToSite(self, *arg):
		dialogman.launchBrowserURL('http://sk1project.org')
				
			
	def build_tab_authors(self):
		panel = TFrame(self.root, style='FlatFrame', borderwidth = 5)
		self.nb.add(panel, text='Authors')
		
		subpanel = TFrame(panel, style='RoundedFrame', borderwidth = 4)		
		subpanel.grid(sticky=N+S+E+W)
		
		panel.rowconfigure(0, weight=1)
		panel.columnconfigure(0, weight=1)
		subpanel.rowconfigure(0, weight=1)
		subpanel.columnconfigure(0, weight=1)
		
		sb=TScrollbar(subpanel)
		sb.grid(row=0, column=1,sticky=N+S)
				
		text=Text(subpanel, bg='white',highlightthickness=0, wrap=NONE)
		text.grid(row=0, column=0,sticky=N+S+E+W)
		
		text['yscrollcommand'] = sb.set
		sb['command'] = text.yview
		
		txt=_('\nTo report bugs please use project bugtracker: https://bugs.launchpad.net/sk1/.\n\n')
		txt+=_('Igor Novikov\n   igor.e.novikov@gmail.com\n   Project Leader\n\n')
		txt+=_('Maxim Barabash\n   maxim.s.barabash@gmail.com\n   Designer\n\n')
		txt+=_('Acknowledgments:\n=======================================\n')
		txt+=_('Valek Fillipov\n   CDR format reverse engineering\n\n')
		txt+=_('Alexandre Prokoudine\n   alexandre.prokoudine@gmail.com\n   Information support (http://linuxgraphics.ru)')
		text['state']=NORMAL
		text.insert(END, txt)
		text['state']=DISABLED
	
	def build_tab_localization(self):
		panel = TFrame(self.root, style='FlatFrame', borderwidth = 5)
		self.nb.add(panel, text='Localization')
		
		subpanel = TFrame(panel, style='RoundedFrame', borderwidth = 4)		
		subpanel.grid(sticky=N+S+E+W)
		
		panel.rowconfigure(0, weight=1)
		panel.columnconfigure(0, weight=1)
		subpanel.rowconfigure(0, weight=1)
		subpanel.columnconfigure(0, weight=1)
		
		sb=TScrollbar(subpanel)
		sb.grid(row=0, column=1,sticky=N+S)
				
		text=Text(subpanel, bg='white',highlightthickness=0, wrap=NONE)
		text.grid(row=0, column=0,sticky=N+S+E+W)
		
		text['yscrollcommand'] = sb.set
		sb['command'] = text.yview
		
		txt=_('\nThe project is not localized yet.\n')
		txt+=_('We plan to provide localization resources for next version\n')
		txt+=_('So if you wish joining to sK1 team as a localizator, just contact us!')
		text['state']=NORMAL
		text.insert(END, txt)
		text['state']=DISABLED
	
	def build_tab_license(self):
		panel = TFrame(self.root, style='FlatFrame', borderwidth = 5)
		self.nb.add(panel, text='License')
		
		subpanel = TFrame(panel, style='RoundedFrame', borderwidth = 4)
		subpanel.grid(sticky=N+S+E+W)
		
		panel.rowconfigure(0, weight=1)
		panel.columnconfigure(0, weight=1)
		subpanel.rowconfigure(0, weight=1)
		subpanel.columnconfigure(0, weight=1)
		
		sb=TScrollbar(subpanel)
		sb.grid(row=0, column=1,sticky=N+S)
						
		text=Text(subpanel, highlightthickness=0, font=app.config.preferences.fixed_font, wrap=NONE)
		text.grid(row=0, column=0,sticky=N+S+E+W)
		
		text['yscrollcommand'] = sb.set
		sb['command'] = text.yview
		
		text['state']=NORMAL
		txt=open(os.path.join(app.config.sk_dir, 'GNU_LGPL_v2')).read()
		text.insert(END, txt)
		text['state']=DISABLED
		
	def ok(self, *arg):
		self.close_dlg()
	
	def cancel(self, *arg):
		self.close_dlg(None)
		
def aboutDialog(master):
	dlg = AboutDialog(master)
	dlg.RunDialog()