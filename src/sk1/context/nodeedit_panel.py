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
from app.conf.const import SELECTION

class NodeEditPanel(CtxSubPanel):
	
	name='NodeEditPanel'
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		self.builded=0
		self.ReSubscribe()
		
	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.update)
	
	def build_dlg(self):
		if not self.builded:
			cmds = self.mw.canvas.commands.PolyBezierEditor		
			b = TButton(self.panel, command=cmds.InsertNodes.Invoke, style='Toolbutton', image='context_node_add')
			tooltips.AddDescription(b, _('Insert node'))
			b.pack(side = LEFT)
			b = TButton(self.panel, command=cmds.DeleteNodes.Invoke, style='Toolbutton', image='context_node_remove')
			tooltips.AddDescription(b, _('Remove nodes'))
			b.pack(side = LEFT)
			
			#############
			b = TLabel(self.panel, image = "toolbar_sep")
			b.pack(side = LEFT)
			
			b = TButton(self.panel, command=cmds.CloseNodes.Invoke, style='Toolbutton', image='context_node_join')
			tooltips.AddDescription(b, _('Join selected nodes'))
			b.pack(side = LEFT)
			b = TButton(self.panel, command=cmds.OpenNodes.Invoke, style='Toolbutton', image='context_node_break')
			tooltips.AddDescription(b, _('Break path at selected nodes'))
			b.pack(side = LEFT)
			
			#############
			b = TLabel(self.panel, image = "toolbar_sep")
			b.pack(side = LEFT)
						
			b = TButton(self.panel, command=cmds.ContAngle.Invoke, style='Toolbutton', image='context_node_corner')
			tooltips.AddDescription(b, _('Make selected nodes corner'))
			b.pack(side = LEFT)
			b = TButton(self.panel, command=cmds.ContSmooth.Invoke, style='Toolbutton', image='context_node_smooth')
			tooltips.AddDescription(b, _('Make selected nodes smooth'))
			b.pack(side = LEFT)
			b = TButton(self.panel, command=cmds.ContSymmetrical.Invoke, style='Toolbutton', image='context_node_symm')
			tooltips.AddDescription(b, _('Make selected nodes symmetric'))
			b.pack(side = LEFT)
						
			#############
			b = TLabel(self.panel, image = "toolbar_sep")
			b.pack(side = LEFT)			
			
			b = TButton(self.panel, command=cmds.SegmentsToLines.Invoke, style='Toolbutton', image='context_node_line')
			tooltips.AddDescription(b, _('Make selected segments lines'))
			b.pack(side = LEFT)
			b = TButton(self.panel, command=cmds.SegmentsToCurve.Invoke, style='Toolbutton', image='context_node_curve')
			tooltips.AddDescription(b, _('Make selected segments curves'))
			b.pack(side = LEFT)
			
			#############
			b = TLabel(self.panel, image = "toolbar_sep")
			b.pack(side = LEFT)	
			
			b = TButton(self.panel, command=cmds.SelectAllNodes.Invoke, style='Toolbutton', image='context_node_all')
			tooltips.AddDescription(b, _('Select all nodes in path'))
			b.pack(side = LEFT)			

			self.builded=1
		
	def update(self,*arg):
		if not self.mw.canvas is None:
			self.build_dlg()
		
	def stub(self):
		pass

