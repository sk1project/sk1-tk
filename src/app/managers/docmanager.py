# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


class DocumentManager:
	docs=[]
	mainwindow=None
	
	def __init__(self, mainwindow):
		self.mainwindow=mainwindow