#!/usr/bin/env python
#
# Setup script for sK1 0.9
#
# Copyright (C) 2007 Igor E. Novikov
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
#
# Usage: 
# --------------------------------------------------------------------------
#  to build package:   python setup.py build
#  to install package:   python setup.py install
# --------------------------------------------------------------------------
#  to create source distribution:   python setup.py sdist
# --------------------------------------------------------------------------
#  to create binary RPM distribution:  python setup.py bdist_rpm
#
#  to create deb package just use alien command (i.e. rpm2deb)
#
#  help on available distribution formats: python setup.py bdist --help-formats
#

from distutils.core import setup, Extension
import os, sys
########################
#
# Main build procedure
#
########################

#Return directory list for provided path
def get_dirs(path='.'):
	list=[]
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
	list=[]
	names=[]
	if os.path.isdir(path):
		try:
			names = os.listdir(path)
		except os.error:
			return names
	names.sort()
	for name in names:
		if os.path.isdir(os.path.join(path, name)) and not name=='.svn':
			list.append(os.path.join(path, name))
	return list

#Return file list for provided path
def get_files(path='.', ext='*'):	
	list=[]
	if path:
		if os.path.isdir(path):
			try:
				names = os.listdir(path)
			except os.error:
				return []
		names.sort()
		for name in names:
			if not os.path.isdir(os.path.join(path, name)):
				if ext=='*':
					list.append(name)
				elif '.'+ext==name[-1*(len(ext)+1):]:
					list.append(name)				
	return list

#Return full file names list for provided path
def get_files_withpath(path='.', ext='*'):
	import glob
	list = glob.glob(os.path.join(path, "*."+ext))
	list.sort()
	return list

#Return recursive directories list for provided path
def get_dirs_tree(path='.'):
	tree=get_dirs_withpath(path)
	for node in tree:
		subtree=get_dirs_tree(node)
		tree+=subtree
	return tree		
	
#Return recursive files list for provided path
def get_files_tree(path='.', ext='*'):
	tree=[]
	dirs=[path,]	
	dirs+=get_dirs_tree(path)
	for dir in dirs:
		list = get_files_withpath(dir,ext)
		list.sort()
		tree+=list
	return tree



def make_manifest():
	proc = os.popen('cat MANIFEST.pre.in>MANIFEST.in')
	proc.close()

def file_scan(cat):
	proc = os.popen("find "+cat+" -type f|grep -v \.svn|grep -v \.xvpics|grep -v \.py$|grep -v \.c$|sed 's/^/include /g'>>MANIFEST.in")
	proc.close()

if __name__ == "__main__":
	print 'Source tree scan...'
	make_manifest()
	file_scan('src/share')
	file_scan('src/extentions')
	print 'MANIFEST.in is created'
	dirs=get_dirs_tree('src/share')
	share_dirs=[]
	for item in dirs:
		share_dirs.append(os.path.join(item[4:],'*.*'))
	for item in ['GNU_GPL_v2', 'GNU_LGPL_v2', 'COPYRIGHTS', 'share/*.*']:
		share_dirs.append(item)
 
	src_path='src/'
	
	filter_src=src_path+'extentions/filter/'
				
	filter_module = Extension('sk1.app.modules.streamfilter',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],	
			sources = [filter_src+'streamfilter.c', filter_src+'filterobj.c', filter_src+'linefilter.c', 
					filter_src+'subfilefilter.c', filter_src+'base64filter.c', filter_src+'nullfilter.c', 
					filter_src+'stringfilter.c', filter_src+'binfile.c', filter_src+'hexfilter.c'])
 
 	type1mod_src=src_path+'extentions/type1mod/'				
	type1mod_module = Extension('sk1.app.modules._type1module',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [type1mod_src+'_type1module.c'])
 
 	skread_src=src_path+'extentions/skread/'				
	skread_module = Extension('sk1.app.modules.skreadmodule',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [skread_src+'skreadmodule.c'])

 	pstokenize_src=src_path+'extentions/pstokenize/'				
	pstokenize_module = Extension('sk1.app.modules.pstokenize',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],			
			sources = [pstokenize_src+'pstokenize.c', pstokenize_src+'pschartab.c'])
			
 	paxtkinter_src=src_path+'extentions/paxtkinter/'				
	paxtkinter_module = Extension('sk1.app.modules.paxtkinter',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [paxtkinter_src+'paxtkinter.c'],
			libraries=['X11', 'tk8.5', 'tcl8.5'])
			
 	ft2_src=src_path+'extentions/freetype2/'				
	ft2_module = Extension('sk1.app.modules.ft2',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [ft2_src+'ft2module.c'],
			include_dirs=['/usr/include/freetype2'],
			libraries=['freetype'],
			extra_compile_args=["-Wall"])
			
 	pax_src=src_path+'extentions/pax/'				
	pax_module = Extension('sk1.app.modules.paxmodule',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [pax_src+'borderobject.c', pax_src+'clipmask.c', pax_src+'cmapobject.c', 
					pax_src+'fontobject.c', pax_src+'gcobject.c',  #pax_src+'gcmethods.c',
					pax_src+'imageobject.c', pax_src+'intl.c', pax_src+'paxmodule.c', 
					pax_src+'paxutil.c', pax_src+'pixmapobject.c', pax_src+'regionobject.c', 
					pax_src+'tkwinobject.c'],
			include_dirs=['/usr/include/cairo'],
			libraries=['X11', 'Xext', 'tk8.5', 'tcl8.5', 'cairo'])
			
 	skmod_src=src_path+'extentions/skmod/'	
	skmod_module = Extension('sk1.app.modules._sketchmodule',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [skmod_src+'curvedraw.c', skmod_src+'curvefunc.c', skmod_src+'curvelow.c', 
					skmod_src+'curvemisc.c', skmod_src+'curveobject.c', skmod_src+'skaux.c', 
					skmod_src+'skcolor.c', skmod_src+'skdither.c', skmod_src+'_sketchmodule.c', 
					skmod_src+'skfm.c', skmod_src+'skimage.c', skmod_src+'skpoint.c', 
					skmod_src+'skrect.c', skmod_src+'sktrafo.c'],
			include_dirs=['/usr/include/cairo'],
			libraries=['m', 'X11', 'Xext', 'tk8.5', 'tcl8.5', 'cairo'])
			
 	tkpng_src=src_path+'extentions/tkpng/'
	tkpng_module = Extension('sk1.app.modules.libtkpng',
			define_macros = [('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources = [tkpng_src+'tkImgPNG.c', tkpng_src+'tkImgPNGInit.c'],
			libraries=['tk8.5', 'tcl8.5', 'z'])

			
	setup (name = 'sK1',
			version = '0.9.0',
			description = 'Vector graphics editor for prepress',
			author = 'Igor E. Novikov',
			author_email = 'igor.e.novikov@gmail.com',
			maintainer = 'Igor E. Novikov',
			maintainer_email = 'igor.e.novikov@gmail.com',
			license = 'LGPL v2, GPL v2 (some packages)',
			url = 'http://sk1project.org',
			download_url = 'http://sk1project.org/modules.php?name=Products',
			long_description = '''
sK1 is an open source vector graphics editor similar to CorelDRAW, Adobe Illustrator, or Freehand. 
First of all sK1 is oriented for prepress industry, therefore works with CMYK colorspace and
produces CMYK-based postscript output.
sK1 Team (http://sk1project.org), copyright (C) 2007 by Igor E. Novikov.
			''',
		classifiers=[
			'Development Status :: 5 - Stable',
			'Environment :: Desktop',
			'Intended Audience :: End Users/Desktop',
			'License :: OSI Approved :: LGPL v2',
			'License :: OSI Approved :: GPL v2',
			'Operating System :: POSIX',
			'Operating System :: MacOS :: MacOS X',
			'Programming Language :: Python',
			'Programming Language :: Tcl',
			'Programming Language :: C',
			"Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
			],

			packages = ['sk1',
				'sk1.app',
				'sk1.app.conf',
				'sk1.app.events', 
				'sk1.app.Graphics', 
				'sk1.app.io', 
				'sk1.app.Lib', 
				'sk1.app.managers', 
				'sk1.app.modules', 
				'sk1.app.plugins', 
				'sk1.app.Scripting', 
				'sk1.app.scripts', 
				'sk1.app.tcl', 
				'sk1.app.UI', 
				'sk1.app.UI.context', 
				'sk1.app.UI.widgets', 
				'sk1.app.UI.pluginpanels', 
				'sk1.app.UI.context',
				'sk1.app.UI.dialogs'
				'sk1.app.UI.pathutils',
				'sk1.app.utils', 
				'sk1.app.X11'
			],
			
			package_dir = {'sk1': 'src',
			'sk1.app': 'src/app',
			'sk1.app.plugins': 'src/app/plugins',
			'sk1.app.modules': 'src/app/modules',
			},
			
			package_data={'sk1.app': ['VERSION', 'tkdefaults', 'tcl/*.tcl'],			
			'sk1.app.plugins': ['Filters/*.py','Objects/*.py','Objects/Lib/multilinetext/*.py'],
			'sk1': share_dirs,
			'sk1.app.modules': ['pkgIndex.tcl', 'descr.txt']
			},

			scripts=['src/sk1'],

			ext_modules = [filter_module, type1mod_module, skread_module, 
						pstokenize_module, skmod_module, paxtkinter_module,
						pax_module, tkpng_module, ft2_module])
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
