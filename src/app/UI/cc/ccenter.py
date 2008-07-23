# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from ccenterdialog import ControlCenter

cc_nodes=[]
cc_leafs=[]
cc_tree=None

class CCItem:
	id='Item'
	name='Item'
	description='Something like description'
	icon='leaf'
	childs=None
	
	def __init__(self):
		pass
	
	def build(self):
		pass
	
	def run(self):
		pass
	
	

def cCenter(master):
	dlg = ControlCenter(master)
	dlg.RunDialog()