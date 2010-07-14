# -*- coding: utf-8 -*-


# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

from pagelayout import PageLayout

class Page:
	
	name=""	
	pagelayout=None
	layers=[]
	
	def __init__(self, name="", pagelayout=PageLayout()):
		self.name=name
		self.pagelayout=pagelayout
		
	def SaveToFile(self, file):	
		for layer in self.layers:
		    layer.SaveToFile(file)
	
	