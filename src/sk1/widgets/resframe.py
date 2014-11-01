# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov.
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
# Resizable Frame for plugins strip
#

from sk1sdk.libttk import TFrame, TButton
from Tkinter import Canvas, Frame, LEFT, RIGHT, TOP, BOTTOM, X, Y, BOTH
from sk1 import appconst
import string

class ResizableTFrame(TFrame):

	def __init__(self, parent, toplevel, size=300, orient=LEFT, min=200, max=500, cnf={}, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.parent = parent
		self.panel = TFrame(self, style='FlatFrame')
		self.orient = orient
		self.min = min
		self.max = max
		self.size = size
		self.toplevel = toplevel
		self.canv_size = 0
		self.counter = 0

		if orient in [LEFT, RIGHT]:
			self.spacer = Frame(self, width=size, height=1)
			self.grip = TButton(self, style='VGrip', cursor=appconst.CurHResize)
			if orient == LEFT:
				self.spacer.pack(side=TOP)
				self.grip.pack(side=LEFT, fill=Y)
				self.panel.pack(side=RIGHT, fill=BOTH, expand=1)
			else:
				self.spacer.pack(side=TOP)
				self.grip.pack(side=RIGHT, fill=Y)
				self.panel.pack(side=LEFT, fill=BOTH, expand=1)
		else:
			self.spacer = Frame(self, width=1, height=size)
			self.grip = TButton(self, style='HGrip', cursor=appconst.CurVResize)
			if orient == BOTTOM:
				self.grip.pack(side=BOTTOM, fill=X)
				self.spacer.pack(side=RIGHT)
				self.panel.pack(side=LEFT, fill=BOTH, expand=1)
			else:
				self.grip.pack(side=TOP, fill=X)
				self.spacer.pack(side=RIGHT)
				self.panel.pack(side=LEFT, fill=BOTH, expand=1)

		self.grip.bind ("<Button-1>", self.start)
		self.grip.bind ("<ButtonRelease-1>", self.stop)

	def start(self, *args):
		self.toplevel.bind ("<Motion>", self.resize)

	def stop(self, *args):
		self.toplevel.unbind ("<Motion>")

	def resize(self, args):
		self.counter += 1
		if self.counter < 5:
			return
		self.counter = 0

		if self.orient in [LEFT, RIGHT]:
			self.canv_size = args.x
		else:
			self.canv_size = args.y

		if self.orient in [LEFT, RIGHT]:
			cw = string.atoi(self.spacer['width'])
			if self.orient == LEFT:
				cw -= self.canv_size
			else:
				cw += self.canv_size
			if cw < self.min:cw = self.min
			if cw > self.max:cw = self.max
			self.spacer['width'] = cw
		else:
			cw = string.atoi(self.spacer['height'])
			if self.orient == TOP:
				cw -= self.canv_size
			else:
				cw += self.canv_size
			if cw < self.min:cw = self.min
			if cw > self.max:cw = self.max
			self.spacer['height'] = cw
