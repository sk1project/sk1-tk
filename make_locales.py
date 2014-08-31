#!/usr/bin/env python
#
# Script to compile locales files for sK1
#
# Copyright (C) 2007-2014 Igor E. Novikov
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA


"""
Usage: 
--------------------------------------------------------------------------
 to build POT file:     python make_locales.py build_pot_file
--------------------------------------------------------------------------
 to generate locales:   python make_locales.py build_locales
--------------------------------------------------------------------------
"""

import os, shutil, sys

#Return directory list for provided path
def get_dirs(path='.'):
	list = []
	if path:
		if os.path.isdir(path):
			try:
				names = os.listdir(path)
			except os.error:
				return []
		names.sort()
		for name in names:
			if os.path.isdir(os.path.join(path, name)):
				list.append(name)
		return list

#Return full  directory names list for provided path
def get_dirs_withpath(path='.'):
	list = []
	names = []
	if os.path.isdir(path):
		try:
			names = os.listdir(path)
		except os.error:
			return names
	names.sort()
	for name in names:
		if os.path.isdir(os.path.join(path, name)) and not name == '.svn':
			list.append(os.path.join(path, name))
	return list

#Return file list for provided path
def get_files(path='.', ext='*'):
	list = []
	if path:
		if os.path.isdir(path):
			try:
				names = os.listdir(path)
			except os.error:
				return []
		names.sort()
		for name in names:
			if not os.path.isdir(os.path.join(path, name)):
				if ext == '*':
					list.append(name)
				elif '.' + ext == name[-1 * (len(ext) + 1):]:
					list.append(name)
	return list

#Return full file names list for provided path
def get_files_withpath(path='.', ext='*'):
	import glob
	list = glob.glob(os.path.join(path, "*." + ext))
	list.sort()
	result = []
	for file in list:
		if os.path.isfile(file):
			result.append(file)
	return result

#Return recursive directories list for provided path
def get_dirs_tree(path='.'):
	tree = get_dirs_withpath(path)
	res = [] + tree
	for node in tree:
		subtree = get_dirs_tree(node)
		res += subtree
	return res

#Return recursive files list for provided path
def get_files_tree(path='.', ext='*'):
	tree = []
	dirs = [path, ]
	dirs += get_dirs_tree(path)
	for dir in dirs:
		list = get_files_withpath(dir, ext)
		list.sort()
		tree += list
	return tree

#Collects messages for localization resources
def build_pot_resource():
	print 'POT FILE UPDATE...'
	files = get_files_tree('src', 'py')
	res = open('messages/locale.in', 'w')
	for file in files:
		res.write(file + '\n')
	res.close()
	os.system('xgettext -f messages/locale.in -L Python -p po 2>messages/warnings.log')
	os.system('rm -f po/sk1.pot;mv po/messages.po po/sk1.pot')


#Generates *.mo files
def generate_locales():
	print 'LOCALES BUILD'
	files = get_files('po', 'po')
	if len(files):
		for file in files:
			lang = file.split('.')[0]
			po_file = os.path.join('po', file)
			mo_file = os.path.join('src', 'sk1', 'share', 'locales', lang, 'LC_MESSAGES', 'sk1.mo')
			if not os.path.lexists(os.path.join('src', 'sk1', 'share', 'locales', lang, 'LC_MESSAGES')):
				os.makedirs(os.path.join('src', 'sk1', 'share', 'locales', lang, 'LC_MESSAGES'))
			print po_file, '==>', mo_file
			os.system('msgfmt -o ' + mo_file + ' ' + po_file)

############################################################
#
# Main build procedure
#
############################################################

if len(sys.argv) == 1:
	print 'Please specify build options!'
	print __doc__
	sys.exit(0)

if len(sys.argv) > 1:

	if sys.argv[1] == 'build_pot_file':
		build_pot_resource()
		sys.exit(0)

	if sys.argv[1] == 'build_locales':
		generate_locales()
		sys.exit(0)
