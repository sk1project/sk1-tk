# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.conf.const import SELECTION
from sk1sdk.libtk.Tkinter import LEFT
from app.UI.tkext import TCommandButton
from subpanel import CtxSubPanel
from app import  _


class GroupPanel(CtxSubPanel):
	
	name='GroupPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		b = TCommandButton(self.panel, self.mw.commands.GroupSelected, style='TextButton', text=_('Group'))
		b.pack(side = LEFT)
		b = TCommandButton(self.panel, self.mw.commands.UngroupSelected, style='TextButton', text=_('Ungroup'))
		b.pack(side = LEFT)
		b = TCommandButton(self.panel, self.mw.commands.UngrAll, style='TextButton', text=_('Ungroup All'))
		b.pack(side = LEFT)

class CombinePanel(CtxSubPanel):
	
	name='CombinePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		b = TCommandButton(self.panel, self.mw.commands.CombineBeziers, style='TextButton', text=_('Combine'))
		b.pack(side = LEFT)
		b = TCommandButton(self.panel, self.mw.commands.SplitBeziers, style='TextButton', text=_('Split'))
		b.pack(side = LEFT)
		
class ToCurvePanel(CtxSubPanel):
	
	name='ToCurvePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		b = TCommandButton(self.panel, self.mw.commands.ConvertToCurve, style='Toolbutton', image='context_to_curve')
		b.pack(side = LEFT)
	