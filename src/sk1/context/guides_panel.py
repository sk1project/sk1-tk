# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TLabel, TButton
from sk1.ttk_ext import TSpinbox
from app.conf.const import CHANGED
from Tkinter import LEFT, DoubleVar, StringVar, RIGHT
from subpanel import CtxSubPanel
from app import  _, config, PolyBezier, CreatePath, Point
from sk1sdk.libttk import tooltips
from sk1.widgets.lengthvar import LengthVar

class GuidesPanel(CtxSubPanel):
	
	name='GuidesPanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)		
		b = TButton(self.panel, command=self.makePageFrame, style='Toolbutton', image='context_add_page_frame')
		tooltips.AddDescription(b, _('Add page frame'))
		b.pack(side = LEFT)
		b = TButton(self.panel, command=self.addCenteredGuides, style='Toolbutton', image='context_add_centered_guides')
		tooltips.AddDescription(b, _('Add guides for page center'))
		b.pack(side = LEFT)
		
		#############
		b = TLabel(self.panel, image = "toolbar_sep")
		b.pack(side = LEFT)
		b = TButton(self.panel, command=self.addGuidesFrame, style='Toolbutton', image='context_add_guides_frame')
		tooltips.AddDescription(b, _('Add guides across page border'))
		b.pack(side = LEFT)
		
		
		self.var_jump_number=DoubleVar(self.mw.root)
		
		unit = config.preferences.default_unit
		var_jump_unit = StringVar(self.mw.root)
		self.var_jump = LengthVar(10, unit, self.var_jump_number, var_jump_unit)
		
		self.entry_jump = TSpinbox(self.panel,  var=0, 
						vartype=1, textvariable = self.var_jump_number,
						min = -1000, max = 1000, step = 5, width = 6, command = self.addGuidesFrame)
		self.entry_jump.pack(side = LEFT, padx=2)
		config.preferences.Subscribe(CHANGED, self.update)		
		self.var_jump.set(0)
		self.update(0, 0)		
		
		
		b = TLabel(self.panel, image = "toolbar_sep")
		b.pack(side = LEFT)
		##############
		
		b = TButton(self.panel, command=self.removeAllGuides, style='Toolbutton', image='context_remove_all_guides')
		tooltips.AddDescription(b, _('Remove all guides'))
		b.pack(side = LEFT)
		
	def update(self,*arg):
		self.var_jump.unit=config.preferences.default_unit

		
	def makePageFrame(self):
		doc=self.doc
		layout = doc.Layout()
		hor_p=layout.Width()
		ver_p=layout.Height()
		path = CreatePath()
		path.AppendLine(Point(0, 0))
		path.AppendLine(Point(hor_p, 0))
		path.AppendLine(Point(hor_p, ver_p))
		path.AppendLine(Point(0, ver_p))
		path.AppendLine(Point(0, 0))
		path.AppendLine(path.Node(0))
		path.ClosePath()
		bezier = PolyBezier((path,))
		doc.Insert(bezier)
	
	def addGuidesFrame(self, *arg):		
		border=self.var_jump.get()
		doc=self.doc
		layout = doc.Layout()
		hor_p=layout.Width()
		ver_p=layout.Height()
		doc.AddGuideLine(Point(0, 0+border), 1)
		doc.AddGuideLine(Point(0+border, 0), 0)
		doc.AddGuideLine(Point(0, ver_p-border), 1)
		doc.AddGuideLine(Point(hor_p-border, 0), 0)	
		
	def addCenteredGuides(self):
		doc=self.doc
		layout = doc.Layout()
		hor_p=layout.Width()
		ver_p=layout.Height()
		doc.AddGuideLine(Point(0, ver_p/2), 1)
		doc.AddGuideLine(Point(hor_p/2, 0), 0)
	
	def removeAllGuides(self):
		doc=self.doc
		guide_lines = doc.GuideLines()
		for line in guide_lines:
				doc.RemoveGuideLine(line)
	