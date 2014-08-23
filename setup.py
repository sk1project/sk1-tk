#!/usr/bin/env python
#
# Setup script for sK1
#
# Copyright (C) 2007-2010 Igor E. Novikov
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
# --------------------------------------------------------------------------
#  to create binary DEB package:  python setup.py bdist_deb
# --------------------------------------------------------------------------
#  to update localization .pot file: python setup.py build_pot_file (Linux only)
# --------------------------------------------------------------------------
#  to create localization .mo files: python setup.py build_locales (Linux only)
# --------------------------------------------------------------------------
#
#  help on available distribution formats: python setup.py bdist --help-formats
#

import os, shutil, sys

COPY = False
DEBIAN = False
VERSION = '0.9.1pre2'

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
			mo_file = os.path.join('src', 'share', 'locales', lang, 'LC_MESSAGES', 'sk1.mo')
			if not os.path.lexists(os.path.join('src', 'share', 'locales', lang, 'LC_MESSAGES')):
				os.makedirs(os.path.join('src', 'share', 'locales', lang, 'LC_MESSAGES'))
			print po_file, '==>', mo_file
			os.system('msgfmt -o ' + mo_file + ' ' + po_file)


############################################################
#
# Main build procedure
#
############################################################

if __name__ == "__main__":

	if len(sys.argv) > 1 and sys.argv[1] == 'build_pot_file':
		build_pot_resource()
		sys.exit(0)

	if len(sys.argv) > 1 and sys.argv[1] == 'build_locales':
		generate_locales()
		sys.exit(0)

	if len(sys.argv) > 1 and sys.argv[1] == 'build&copy':
		build_pot_resource()
		COPY = True
		sys.argv[1] = 'build'

	if len(sys.argv) > 1 and sys.argv[1] == 'bdist_deb':
		DEBIAN = True
		sys.argv[1] = 'build'
		generate_locales()

	if len(sys.argv) > 1 and sys.argv[1] == 'bdist_rpm':
		generate_locales()

	if len(sys.argv) > 1 and not sys.argv[1] == 'sdist':
		generate_locales()

	from distutils.core import setup, Extension
	print 'Source tree scan...'
	dirs = get_dirs_tree('src/share')
	share_dirs = []
	for item in dirs:
		share_dirs.append(os.path.join(item[4:], '*.*'))
	for item in ['GNU_GPL_v2', 'GNU_LGPL_v2', 'COPYRIGHTS', 'share/*.*']:
		share_dirs.append(item)

	src_path = 'src/sk1/'

	filter_src = src_path + 'extensions/filter/'

	filter_module = Extension('sk1.app.modules.streamfilter',
			define_macros=[('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources=[filter_src + 'streamfilter.c', filter_src + 'filterobj.c', filter_src + 'linefilter.c',
					filter_src + 'subfilefilter.c', filter_src + 'base64filter.c', filter_src + 'nullfilter.c',
					filter_src + 'stringfilter.c', filter_src + 'binfile.c', filter_src + 'hexfilter.c'])

	#Fix for Debian based distros
	tcl_include_dirs = []
	tcl_ver = ''
	if os.path.isdir('/usr/include/tcl8.5'):
		tcl_include_dirs = ['/usr/include/tcl8.5']
		tcl_ver = '8.5'

	if os.path.isdir('/usr/include/tcl8.6'):
		tcl_include_dirs = ['/usr/include/tcl8.6']
		tcl_ver = '8.6'

	#Fix for OpenSuse
	if not tcl_ver:
		if os.path.isfile('/usr/lib/libtcl8.5.so'):
			tcl_ver = '8.5'
		if os.path.isfile('/usr/lib/libtcl8.6.so'):
			tcl_ver = '8.6'

	#Fix for Fedora
	if not tcl_ver:
		if os.path.isfile('/usr/lib64/libtcl8.5.so'):
			tcl_ver = '8.5'
		if os.path.isfile('/usr/lib64/libtcl8.6.so'):
			tcl_ver = '8.6'

	if not tcl_ver:
		print 'System tcl/tk =>8.5 libraries have not found!'
		sys.exit(1)


 	type1mod_src = src_path + 'extensions/type1mod/'
	type1mod_module = Extension('sk1.app.modules._type1module',
			define_macros=[('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources=[type1mod_src + '_type1module.c'])

 	skread_src = src_path + 'extensions/skread/'
	skread_module = Extension('sk1.app.modules.skreadmodule',
			define_macros=[('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources=[skread_src + 'skreadmodule.c'])

 	pstokenize_src = src_path + 'extensions/pstokenize/'
	pstokenize_module = Extension('sk1.app.modules.pstokenize',
			define_macros=[('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources=[pstokenize_src + 'pstokenize.c', pstokenize_src + 'pschartab.c'])

 	pax_src = src_path + 'extensions/pax/'
 	pax_include_dirs = ['/usr/include/cairo']
 	pax_include_dirs.extend(tcl_include_dirs)
	pax_module = Extension('sk1.app.modules.paxmodule',
			define_macros=[('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources=[pax_src + 'borderobject.c', pax_src + 'clipmask.c', pax_src + 'cmapobject.c',
					pax_src + 'fontobject.c', pax_src + 'gcobject.c',#pax_src+'gcmethods.c',
					pax_src + 'imageobject.c', pax_src + 'intl.c', pax_src + 'paxmodule.c',
					pax_src + 'paxutil.c', pax_src + 'pixmapobject.c', pax_src + 'regionobject.c',
					pax_src + 'tkwinobject.c'],
			include_dirs=pax_include_dirs,
			libraries=['X11', 'Xext', 'tk' + tcl_ver, 'tcl' + tcl_ver, 'cairo'])

 	skmod_src = src_path + 'extensions/skmod/'
	skmod_module = Extension('sk1.app.modules._sketchmodule',
			define_macros=[('MAJOR_VERSION', '0'),
						('MINOR_VERSION', '9')],
			sources=[skmod_src + 'curvedraw.c', skmod_src + 'curvefunc.c', skmod_src + 'curvelow.c',
					skmod_src + 'curvemisc.c', skmod_src + 'curveobject.c', skmod_src + 'skaux.c',
					skmod_src + 'skcolor.c', skmod_src + 'skdither.c', skmod_src + '_sketchmodule.c',
					skmod_src + 'skfm.c', skmod_src + 'skimage.c', skmod_src + 'skpoint.c',
					skmod_src + 'skrect.c', skmod_src + 'sktrafo.c'],
			include_dirs=['/usr/include/cairo'],
			libraries=['m', 'X11', 'cairo'])

	setup (name='sk1',
			version=VERSION,
			description='Vector graphics editor for prepress',
			author='Igor E. Novikov',
			author_email='igor.e.novikov@gmail.com',
			maintainer='Igor E. Novikov',
			maintainer_email='igor.e.novikov@gmail.com',
			license='LGPL v2, GPL v2 (some packages)',
			url='http://sk1project.org',
			download_url='http://sk1project.org/modules.php?name=Products',
			long_description='''
sK1 is an open source vector graphics editor similar to CorelDRAW, Adobe Illustrator, or Freehand. 
First of all sK1 is oriented for prepress industry, therefore works with CMYK colorspace and
produces CMYK-based PDF and postscript output.
sK1 Team (http://sk1project.org), copyright (C) 2003-2010 by Igor E. Novikov.
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

			packages=['sk1',
				'sk1.app',
				'sk1.app.conf',
				'sk1.app.events',
				'sk1.app.Graphics',
				'sk1.app.io',
				'sk1.app.Lib',
				'sk1.app.managers',
				'sk1.app.modules',
				'sk1.app.Scripting',
				'sk1.app.scripts',
				'sk1.app.tcl',
				'sk1.app.UI',
				'sk1.app.UI.widgets',
				'sk1.app.UI.pluginpanels',
				'sk1.app.UI.pluginpanels.effects',
				'sk1.app.UI.pluginpanels.extensions',
				'sk1.app.UI.pluginpanels.layout',
				'sk1.app.UI.pluginpanels.properties',
				'sk1.app.UI.pluginpanels.transform',
				'sk1.app.UI.pluginpanels.shaping',
				'sk1.app.UI.context',
				'sk1.app.UI.dialogs',
				'sk1.app.UI.cc',
				'sk1.app.UI.cc.panels',
				'sk1.app.utils',
				'sk1.app.X11'
			],

			package_dir={'sk1': 'src/sk1',
			'sk1.app': 'src/sk1/app',
			'sk1.app.modules': 'src/sk1/app/modules',
			},

			package_data={'sk1.app': ['VERSION', 'tcl/*.tcl'],
			'sk1': share_dirs,
			'sk1.app.modules': ['descr.txt', ]
			},

			scripts=['src/script/sk1'],

			data_files=[
					('/usr/share/applications', ['src/sk1.desktop', ]),
					('/usr/share/pixmaps', ['src/sk1.png', 'src/sk1.xpm', ]),
					],

			ext_modules=[filter_module, type1mod_module, skread_module,
						pstokenize_module, skmod_module, pax_module])



#################################################
# .py source compiling
#################################################
if sys.argv[1] == 'build':
	import compileall
	compileall.compile_dir('build/')

##############################################
# This section for developing purpose only
# Command 'python setup.py build&copy' allows
# automating build and native extension copying
# into package directory
##############################################

if COPY:
	import string, platform
	version = (string.split(sys.version)[0])[0:3]

	shutil.copy('build/lib.linux-' + platform.machine() + '-' + version + '/sk1/app/modules/paxmodule.so', 'src/app/modules/')
	print '\n paxmodule.so has been copied to src/ directory'

	shutil.copy('build/lib.linux-' + platform.machine() + '-' + version + '/sk1/app/modules/pstokenize.so', 'src/app/modules/')
	print '\n pstokenize.so has been copied to src/ directory'

	shutil.copy('build/lib.linux-' + platform.machine() + '-' + version + '/sk1/app/modules/_sketchmodule.so', 'src/app/modules/')
	print '\n _sketchmodule.so has been copied to src/ directory'

	shutil.copy('build/lib.linux-' + platform.machine() + '-' + version + '/sk1/app/modules/skreadmodule.so', 'src/app/modules/')
	print '\n skreadmodule.so has been copied to src/ directory'

	shutil.copy('build/lib.linux-' + platform.machine() + '-' + version + '/sk1/app/modules/streamfilter.so', 'src/app/modules/')
	print '\n streamfilter.so has been copied to src/ directory'

	shutil.copy('build/lib.linux-' + platform.machine() + '-' + version + '/sk1/app/modules/_type1module.so', 'src/app/modules/')
	print '\n _type1module.so has been copied to src/ directory'

	os.system('rm -rf build')

#################################################
# Implementation of bdist_deb command
#################################################
if DEBIAN:
	print '\nDEBIAN PACKAGE BUILD'
	print '===================='
	import string, platform
	version = (string.split(sys.version)[0])[0:3]

	arch, bin = platform.architecture()
	if arch == '64bit':
		arch = 'amd64'
	else:
		arch = 'i386'

	target = 'build/deb-root/usr/lib/python' + version + '/dist-packages'

	if os.path.lexists(os.path.join('build', 'deb-root')):
		os.system('rm -rf build/deb-root')
	os.makedirs(os.path.join('build', 'deb-root', 'DEBIAN'))

	os.system("cat DEBIAN/control |sed 's/<PLATFORM>/" + arch + "/g'|sed 's/<VERSION>/" + VERSION + "/g'> build/deb-root/DEBIAN/control")

	os.makedirs(target)
	os.makedirs('build/deb-root/usr/bin')
	os.makedirs('build/deb-root/usr/share/applications')
	os.makedirs('build/deb-root/usr/share/pixmaps')

	os.system('cp -R build/lib.linux-' + platform.machine() + '-' + version + '/sk1 ' + target)
	os.system('cp src/sk1.desktop build/deb-root/usr/share/applications')
	os.system('cp src/sk1.png build/deb-root/usr/share/pixmaps')
	os.system('cp src/sk1.xpm build/deb-root/usr/share/pixmaps')
	os.system('cp src/sk1 build/deb-root/usr/bin')
	os.system('chmod +x build/deb-root/usr/bin/sk1')

	if os.path.lexists('dist'):
		os.system('rm -rf dist/*.deb')
	else:
		os.makedirs('dist')

	os.system('dpkg --build build/deb-root/ dist/python-sk1-' + VERSION + '_' + arch + '.deb')










