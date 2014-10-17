# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.conf.const import SELECTION
from Tkinter import LEFT
from sk1.tkext import TCommandButton
from sk1sdk.libttk import tooltips
from subpanel import CtxSubPanel
from app import  _


class GroupPanel(CtxSubPanel):
	
	name='GroupPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		
		b = TCommandButton(self.panel, self.mw.commands.GroupSelected, style='Toolbutton', image='context_group')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, _('Group'))
		
		b = TCommandButton(self.panel, self.mw.commands.UngroupSelected, style='Toolbutton', image='context_ungroup')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, _('Ungroup'))
		
		b = TCommandButton(self.panel, self.mw.commands.UngrAll, style='Toolbutton', image='context_ungroupall')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, _('Ungroup All'))

class CombinePanel(CtxSubPanel):
	
	name='CombinePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		
		b = TCommandButton(self.panel, self.mw.commands.CombineBeziers, style='Toolbutton', image='context_combine')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, _('Combine'))
		
		b = TCommandButton(self.panel, self.mw.commands.SplitBeziers, style='Toolbutton', image='context_split')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, _('Split'))
		
class ToCurvePanel(CtxSubPanel):
	
	name='ToCurvePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		b = TCommandButton(self.panel, self.mw.commands.ConvertToCurve, style='Toolbutton', image='context_to_curve')
		b.pack(side = LEFT)
		tooltips.AddDescription(b, _('Convert to curve'))
	