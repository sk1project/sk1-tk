# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory. 

import Tkinter

class FlatFrame(Tkinter.Frame):
	"""
	Represents flat frame which is often used in UI.
	The class just simplified UI composition.
	"""
	def __init__(self, parent=None, **kw):
		kw['borderwidth']=0
		kw['highlightthickness']=0
		kw['relief']=Tkinter.FLAT
		apply(Tkinter.Frame.__init__, (self, parent), kw)
		self['highlightcolor']=self['bg']
		self['highlightbackground']=self['bg']