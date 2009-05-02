# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory

from fill_plugin import FillPanel
import app
from app import _, SolidPattern, EmptyPattern
from app.UI import styledlg


class OutlineColorPanel(FillPanel):
	
	name='OutlineColor'
	title = _("Outline Color")
	default_color=None
	sign='tools_color_line'
	
	def init(self, master):
		FillPanel.init(self, master)
		
	def apply_pattern(self):
		kw={}
		if self.current_color is None:
			kw["line_pattern"] = EmptyPattern
		else:
			kw["line_pattern"]  = SolidPattern(self.current_color)
		styledlg.set_properties(self.mw.root, self.document, _("Set Outline Color"), 'line', kw)
		
	def init_from_properties(self, properties):
		if properties and properties.HasLine() and properties.line_pattern.__class__ == SolidPattern:
			return properties.line_pattern.Color()	
		elif properties and properties.HasFill() and properties.line_pattern.__class__ == EmptyPattern_:
			return None
		elif not self.current_color is None and len(self.document.selection) > 1:
			return self.current_color
		else:
			return None
		
		
instance=OutlineColorPanel()
app.objprop_plugins.append(instance)