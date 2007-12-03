# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.UI.Ttk import TButton
from Tkinter import LEFT, RIGHT
from subpanel import CtxSubPanel
from app import  _, PolyBezier, CreatePath, Point
from app.UI import tooltips

class GuidesPanel(CtxSubPanel):
	
	name='GuidesPanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)		
		b = TButton(self.panel, command=self.makePageFrame, style='Toolbutton', image='context_add_page_frame')
		tooltips.AddDescription(b, _('Add page frame'))
		b.pack(side = LEFT)
		b = TButton(self.panel, command=self.addGuidesFrame, style='Toolbutton', image='context_add_guides_frame')
		tooltips.AddDescription(b, _('Add guides across page border'))
		b.pack(side = LEFT)
		b = TButton(self.panel, command=self.removeAllGuides, style='Toolbutton', image='context_remove_all_guides')
		tooltips.AddDescription(b, _('Remove all guides'))
		b.pack(side = LEFT)

		
	def makePageFrame(self):
		doc=self.parent.mainwindow.document
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
	
	def addGuidesFrame(self):
		doc=self.parent.mainwindow.document
		layout = doc.Layout()
		hor_p=layout.Width()
		ver_p=layout.Height()
		doc.AddGuideLine(Point(0, 0), 1)
		doc.AddGuideLine(Point(0, 0), 0)
		doc.AddGuideLine(Point(0, ver_p), 1)
		doc.AddGuideLine(Point(hor_p, 0), 0)	
	
	def removeAllGuides(self):
		doc=self.parent.mainwindow.document
		guide_lines = doc.GuideLines()
		for line in guide_lines:
				doc.RemoveGuideLine(line)
	