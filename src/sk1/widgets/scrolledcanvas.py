# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TScrollbar, TFrame
from Tkinter import Canvas

class ScrolledCanvas:
	def __init__(self, master, **opts):
		if not opts.has_key('yscrollincrement'):
			opts['yscrollincrement'] = 20
		self.master = master		
		self.frame = TFrame(master, style="FlatFrame")
		self.frame.rowconfigure(0, weight=1)
		self.frame.columnconfigure(0, weight=1)
		self.canvas = Canvas(self.frame, **opts)
		self.canvas.grid(row=0, column=0, sticky="nsew")
		self.vbar = TScrollbar(self.frame, name="vbar")
		self.vbar.grid(row=0, column=1, sticky="nse")
		self.hbar = TScrollbar(self.frame, name="hbar", orient="horizontal")
		self.hbar.grid(row=1, column=0, sticky="ews")
		self.canvas['yscrollcommand'] = lambda f, l: self.scroll_sh(self.vbar, f, l)
		self.vbar['command'] = self.canvas.yview
		self.canvas['xscrollcommand'] = lambda f, l: self.scroll_sh(self.hbar, f, l)
		self.hbar['command'] = self.canvas.xview
		self.canvas.bind("<Key-Prior>", self.page_up)
		self.canvas.bind("<Key-Next>", self.page_down)
		self.canvas.bind("<Key-Up>", self.unit_up)
		self.canvas.bind("<Key-Down>", self.unit_down)
		self.canvas.bind("<Alt-Key-2>", self.zoom_height)
		self.canvas.bind("<Button-4>", self.unit_up)
		self.canvas.bind("<Button-5>", self.unit_down)
		self.canvas.focus_set()
	def page_up(self, event):
		self.canvas.yview_scroll(-1, "page")
		return "break"
	def page_down(self, event):
		self.canvas.yview_scroll(1, "page")
		return "break"
	def unit_up(self, event):
		first,last=self.vbar.get()
		if first <= 0 and last >= 1:
			return "break"
		self.canvas.yview_scroll(-1, "unit")
		return "break"
	def unit_down(self, event):
		first,last=self.vbar.get()
		if first <= 0 and last >= 1:
			return "break"
		self.canvas.yview_scroll(1, "unit")
		return "break"
	def zoom_height(self, event):
		return "break"
	def scroll_sh(self, scroll, first, last):
	    first, last = float(first), float(last)
	    if first <= 0 and last >= 1:
	        scroll.grid_remove()
	    else:
	        scroll.grid()
	    scroll.set(first, last)