# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app.conf.const import SELECTION
from Tkinter import LEFT
from app.UI.tkext import TCommandButton
from subpanel import CtxSubPanel
from app import  _


class GroupPanel(CtxSubPanel):
	
	name='GroupPanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		mw=self.parent.mainwindow.commands
		b = TCommandButton(self.panel, mw.GroupSelected, style='TextButton', text=_('Group'))
		b.pack(side = LEFT)
		b = TCommandButton(self.panel, mw.UngroupSelected, style='TextButton', text=_('Ungroup'))
		b.pack(side = LEFT)
		b = TCommandButton(self.panel, mw.UngrAll, style='TextButton', text=_('Ungroup All'))
		b.pack(side = LEFT)

class CombinePanel(CtxSubPanel):
	
	name='CombinePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		mw=self.parent.mainwindow.commands
		b = TCommandButton(self.panel, mw.CombineBeziers, style='TextButton', text=_('Combine'))
		b.pack(side = LEFT)
		b = TCommandButton(self.panel, mw.SplitBeziers, style='TextButton', text=_('Split'))
		b.pack(side = LEFT)
		
class ToCurvePanel(CtxSubPanel):
	
	name='ToCurvePanel'	
	
	def __init__(self, parent):
		CtxSubPanel.__init__(self, parent)
		mw=self.parent.mainwindow.commands
		b = TCommandButton(self.panel, mw.ConvertToCurve, style='Toolbutton', image='context_to_curve')
		b.pack(side = LEFT)
	