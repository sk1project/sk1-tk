# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TButton
from Tkinter import LEFT, RIGHT, TOP, X, Y, BOTH, BOTTOM
from app import _, Publisher
from app.conf.const import PAGE, DOCUMENT

class Pager(TFrame, Publisher):
	
	hidden=1
	
	def __init__(self, parent, mainwindow):
		self.parent=parent
		self.mainwindow=mainwindow
		TFrame.__init__(self, self.parent, name = 'pagerPanel', style='FlatFrame', borderwidth=0)
		top_border=TLabel(self, style='FlatLabel', image='space_1')
		top_border.pack(side=TOP, fill=X)
		
		self.container=TFrame(self, style='FlatFrame', borderwidth=0)

		space=TLabel(self.container, style='FlatLabel', image='space_3')
		space.pack(side=LEFT, fill=Y)
		self.home_but=TButton(self.container, style='PagerHome', command=self.PageHome)
		self.home_but.pack(side=LEFT)
		self.home_but=TButton(self.container, style='PagerPrevious', command=self.PagePrevious)
		self.home_but.pack(side=LEFT)
		self.text=TLabel(self.container, style='FlatLabel', text=' '+_('Page 2 of 2')+' ')
		self.text.pack(side=LEFT)
		self.home_but=TButton(self.container, style='PagerNext', command=self.PageNext)
		self.home_but.pack(side=LEFT)
		self.home_but=TButton(self.container, style='PagerEnd', command=self.PageEnd)
		self.home_but.pack(side=LEFT)
		space=TLabel(self.container, style='FlatLabel', image='space_3')
		space.pack(side=LEFT, fill=Y)
		self.mainwindow.Subscribe(DOCUMENT, self.Resubscribe)
		self.Resubscribe()
		self.doc_paged()
		self.text.bind('<Double-Button-1>', self.GoToPage)
				
	def stub(self):
		pass
	
	def doc_paged(self):		
		current_page=self.mainwindow.document.active_page+1
		num_pages=len(self.mainwindow.document.pages)
		if self.hidden and num_pages>1:
			self.container.pack(side=LEFT, fill=Y)
			self.hidden=0
		if not self.hidden and num_pages==1:
			self.container.forget()
			self.hidden=1		
		self.text['text']=' '+_('Page %u of %u')%(current_page,num_pages)+' '
		
	def Resubscribe(self, *arg):
		self.mainwindow.document.Subscribe(PAGE, self.doc_paged)
		self.doc_paged()
		
	def PageHome(self):
		self.mainwindow.document.GoToPage(0)
		self.mainwindow.document.SelectNone()
		self.mainwindow.canvas.ForceRedraw()
	
	def PageEnd(self):
		self.mainwindow.document.GoToPage(len(self.mainwindow.document.pages)-1)
		self.mainwindow.document.SelectNone()
		self.mainwindow.canvas.ForceRedraw()
				
	def PagePrevious(self):
		self.mainwindow.PreviousPage()
		
	def PageNext(self):
		self.mainwindow.NextPage()	
		
	def GoToPage(self, *args):
		self.mainwindow.GotoPage()
		

