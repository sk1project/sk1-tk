#!/usr/bin/env python
#
# Setup script for sK1 0.9.x
#
# Copyright (C) 2007-2015 Igor E. Novikov
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

"""
Usage: 
--------------------------------------------------------------------------
 to build package:       python setup.py build
 to install package:     python setup.py install
 to remove installation: python setup.py uninstall
--------------------------------------------------------------------------
 to create source distribution:   python setup.py sdist
--------------------------------------------------------------------------
 to create binary RPM distribution:  python setup.py bdist_rpm
--------------------------------------------------------------------------
 to create binary DEB distribution:  python setup.py bdist_deb
--------------------------------------------------------------------------.
 Help on available distribution formats: --help-formats
"""

import os, sys

import libutils
from libutils import make_source_list, DEB_Builder


############################################################
#
# Flags
#
############################################################
UPDATE_MODULES = False
DEB_PACKAGE = False
CLEAR_BUILD = False
LCMS2 = True

############################################################
#
# Package description
#
############################################################
NAME = 'sk1'
VERSION = '0.9.3'
DESCRIPTION = 'Vector graphics editor for prepress'
AUTHOR = 'Igor E. Novikov'
AUTHOR_EMAIL = 'igor.e.novikov@gmail.com'
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = 'LGPL v2'
URL = 'http://sk1project.org'
DOWNLOAD_URL = URL
CLASSIFIERS = [
'Development Status :: 5 - Stable',
'Environment :: Desktop',
'Intended Audience :: End Users/Desktop',
'License :: OSI Approved :: LGPL v2',
'Operating System :: POSIX',
'Programming Language :: Python',
'Programming Language :: Tcl',
'Programming Language :: C',
"Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
]
LONG_DESCRIPTION = '''
sK1 is an open source vector graphics editor similar to CorelDRAW, 
Adobe Illustrator, or Freehand. First of all sK1 is oriented for prepress 
industry, therefore works with CMYK colorspace and produces CMYK-based PDF 
and postscript output.
sK1 Project (http://sk1project.org),
Copyright (C) 2007-2015 by Igor E. Novikov 
'''
LONG_DEB_DESCRIPTION = ''' .
 sK1 is an open source vector graphics editor similar to CorelDRAW, 
 Adobe Illustrator, or Freehand. First of all sK1 is oriented for prepress 
 industry, therefore works with CMYK colorspace and produces CMYK-based PDF 
 and postscript output.
 . 
 sK1 Project (http://sk1project.org),
 Copyright (C) 2007-2015 by Igor E. Novikov 
 .
'''

############################################################
#
# Build data
#
############################################################
install_path = '/usr/lib/%s-tk-%s' % (NAME, VERSION)
os.environ["SK1_INSTALL_PATH"] = "%s" % (install_path,)
src_path = 'src'
include_path = '/usr/include'
modules = []
scripts = ['src/script/sk1', ]
deb_scripts = []
data_files = [
('/usr/share/applications', ['src/sk1.desktop', ]),
('/usr/share/pixmaps', ['src/sk1.png', 'src/sk1.xpm', ]),
]
deb_depends = 'libxcursor1, libxext6, python-tk, python-gtk2, python-imaging'
deb_depends += ', python-cairo, python-reportlab'

dirs = libutils.get_dirs_tree('src/sk1/share')
share_dirs = []
for item in dirs: share_dirs.append(os.path.join(item[8:], '*.*'))
share_dirs += ['GNU_GPL_v2', 'GNU_LGPL_v2', 'COPYRIGHTS']

dirs = libutils.get_dirs_tree('src/sk1sdk/tkstyle')
share_dirs_sdk = []
for item in dirs: share_dirs_sdk.append(os.path.join(item[11:], '*.*'))
share_dirs_sdk.append('tcl/*.*')

package_data = {
'sk1': share_dirs,
'sk1sdk.tkpng': ['pkgIndex.tcl', ],
'sk1sdk': share_dirs_sdk,
'uc':['cms/profiles/*.*'],
}

#Preparing start script
fileptr = open('src/script/sk1.tmpl', 'rb')
fileptr2 = open('src/script/sk1', 'wb')
while True:
	line = fileptr.readline()
	if line == '': break
	if '$SK1_INSTALL_PATH' in line:
		line = line.replace('$SK1_INSTALL_PATH', install_path)
	fileptr2.write(line)
fileptr.close()
fileptr2.close()

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
	if sys.argv[1] == 'bdist_rpm':
		CLEAR_BUILD = True

	if sys.argv[1] == 'build_update':
		UPDATE_MODULES = True
		CLEAR_BUILD = True
		sys.argv[1] = 'build'

	if sys.argv[1] == 'bdist_deb':
		DEB_PACKAGE = True
		CLEAR_BUILD = True
		sys.argv[1] = 'build'

	if len(sys.argv) > 2 and '--lcms2' in sys.argv:
		LCMS2 = True
		sys.argv.remove('--lcms2')

	if len(sys.argv) > 2 and '--lcms1' in sys.argv:
		LCMS2 = False
		sys.argv.remove('--lcms1')

	if sys.argv[1] == 'uninstall':
		if os.path.isdir(install_path):
			#removing sk1 folder
			print 'REMOVE: ' + install_path
			os.system('rm -rf ' + install_path)
			#removing scripts
			for item in scripts:
				filename = os.path.basename(item)
				print 'REMOVE: /usr/bin/' + filename
				os.system('rm -rf /usr/bin/' + filename)
			#removing data files
			for item in data_files:
				location = item[0]
				file_list = item[1]
				for file_item in file_list:
					filename = os.path.basename(file_item)
					filepath = os.path.join(location, filename)
					print 'REMOVE: ' + filepath
					os.system('rm -rf ' + filepath)
			print 'Desktop database update: ',
			os.system('update-desktop-database')
			print 'DONE!'
		else:
			print 'sK1 installation is not found!'
		sys.exit(0)


from distutils.core import setup, Extension

macros = [('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')]

paxtkinter_src = os.path.join(src_path, 'extensions', 'paxtkinter')
files = make_source_list(paxtkinter_src, ['paxtkinter.c'])
paxtkinter_module = Extension('app.paxtkinter',
			include_dirs=tcl_include_dirs,
			libraries=['tk' + tcl_ver, 'tcl' + tcl_ver],
			define_macros=macros, sources=files)
modules.append(paxtkinter_module)

filter_src = os.path.join(src_path, 'extensions', 'filter')
files = ['streamfilter.c', 'filterobj.c', 'linefilter.c',
		'subfilefilter.c', 'base64filter.c', 'nullfilter.c',
		'stringfilter.c', 'binfile.c', 'hexfilter.c']
files = make_source_list(filter_src, files)
filter_module = Extension('streamfilter',
		define_macros=macros, sources=files)
modules.append(filter_module)

type1mod_src = os.path.join(src_path, 'extensions', 'type1mod')
files = make_source_list(type1mod_src, ['_type1module.c', ])
type1mod_module = Extension('app._type1module',
		define_macros=macros, sources=files)
modules.append(type1mod_module)

skread_src = os.path.join(src_path, 'extensions', 'skread')
files = make_source_list(skread_src, ['skreadmodule.c', ])
skread_module = Extension('app.skreadmodule',
		define_macros=macros, sources=files)
modules.append(skread_module)

pstokenize_src = os.path.join(src_path, 'extensions', 'pstokenize')
files = make_source_list(pstokenize_src, ['pstokenize.c', 'pschartab.c'])
pstokenize_module = Extension('app.pstokenize',
		define_macros=macros, sources=files)
modules.append(pstokenize_module)

pax_src = os.path.join(src_path, 'extensions', 'pax')
pax_include_dirs = ['/usr/include/cairo'] + tcl_include_dirs
pax_libs = ['X11', 'Xext', 'tk' + tcl_ver, 'tcl' + tcl_ver, 'cairo']
files = ['borderobject.c', 'clipmask.c', 'cmapobject.c', 'fontobject.c',
	'gcobject.c', 'imageobject.c', 'intl.c', 'paxmodule.c', 'paxutil.c',
	'pixmapobject.c', 'regionobject.c', 'tkwinobject.c']
files = make_source_list(pax_src, files)
pax_module = Extension('paxmodule',
		include_dirs=pax_include_dirs, libraries=pax_libs,
		define_macros=macros, sources=files)
modules.append(pax_module)

skmod_src = os.path.join(src_path, 'extensions', 'skmod')
files = ['curvedraw.c', 'curvefunc.c', 'curvelow.c', 'curvemisc.c',
	'curveobject.c', 'skaux.c', 'skcolor.c', 'skdither.c', '_sketchmodule.c',
	'skfm.c', 'skimage.c', 'skpoint.c', 'skrect.c', 'sktrafo.c']
files = make_source_list(skmod_src, files)
skmod_module = Extension('app._sketchmodule',
		include_dirs=['/usr/include/cairo'], libraries=['m', 'X11', 'cairo'],
		define_macros=macros, sources=files)
modules.append(skmod_module)

#--- sk1sdk extensions

tkpng_src = os.path.join(src_path, 'sk1sdk', 'tkpng', 'libtkpng')
files = make_source_list(tkpng_src, ['tkImgPNG.c', 'tkImgPNGInit.c'])
tkpng_module = Extension('sk1sdk.tkpng.libtkpng',
			include_dirs=tcl_include_dirs,
			libraries=['tk' + tcl_ver, 'tcl' + tcl_ver, 'z'],
			define_macros=macros, sources=files)
modules.append(tkpng_module)

tkXcursor_src = os.path.join(src_path, 'sk1sdk', 'tkXcursor')
files = make_source_list(tkXcursor_src, ['_tkXcursor.c'])
tkXcursor_module = Extension('sk1sdk.tkXcursor._tkXcursor',
			include_dirs=['/usr/include/X11/Xcursor'] + tcl_include_dirs,
			libraries=['tk' + tcl_ver, 'tcl' + tcl_ver, 'Xcursor'],
			define_macros=macros, sources=files)
modules.append(tkXcursor_module)

tkcairo_src = os.path.join(src_path, 'sk1sdk', 'tkcairo')
files = make_source_list(tkcairo_src, ['_tkcairo.c'])
tkcairo_module = Extension('sk1sdk.tkcairo._tkcairo',
			include_dirs=['/usr/include/cairo'] + tcl_include_dirs,
			libraries=['tk' + tcl_ver, 'tcl' + tcl_ver, 'cairo'],
			define_macros=macros, sources=files)
modules.append(tkcairo_module)

#--- uc extensions

cms_src = os.path.join(src_path, 'uc', 'cms')
libs = ['lcms2', ]
if LCMS2:
 	files = make_source_list(cms_src, ['_cms2.c', ])
	deb_depends = 'liblcms2-2, ' + deb_depends
else:
 	files = make_source_list(cms_src, ['_cms.c', ])
	deb_depends = 'liblcms1, ' + deb_depends
	libs = ['lcms', ]

cms_module = Extension('uc.cms._cms',
		define_macros=macros, sources=files,
		libraries=libs, extra_compile_args=["-Wall"])
modules.append(cms_module)

cairo_src = os.path.join(src_path, 'uc', 'libcairo')
files = make_source_list(cairo_src, ['_libcairo.c', ])
include_dirs = make_source_list(include_path, ['cairo', 'pycairo'])
cairo_module = Extension('uc.libcairo._libcairo',
		define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
		sources=files, include_dirs=include_dirs,
		libraries=['cairo'])
modules.append(cairo_module)

#---

setup(name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	maintainer=MAINTAINER,
	maintainer_email=MAINTAINER_EMAIL,
	license=LICENSE,
	url=URL,
	download_url=DOWNLOAD_URL,
	long_description=LONG_DESCRIPTION,
	classifiers=CLASSIFIERS,
	packages=libutils.get_source_structure(),
	package_dir=libutils.get_package_dirs(),
	package_data=package_data,
	data_files=data_files,
	scripts=scripts,
	ext_modules=modules)

#################################################
# .py source compiling
#################################################
libutils.compile_sources()


##############################################
# This section for developing purpose only
# Command 'python setup.py build_update' allows
# automating build and native extension copying
# into package directory
##############################################
if UPDATE_MODULES: libutils.copy_modules(modules)


#################################################
# Implementation of bdist_deb command
#################################################
if DEB_PACKAGE:
	bld = DEB_Builder(name=NAME,
					version=VERSION,
					maintainer='%s <%s>' % (AUTHOR, AUTHOR_EMAIL),
					depends=deb_depends,
					homepage=URL,
					description=DESCRIPTION,
					long_description=LONG_DEB_DESCRIPTION,
					package_dirs=libutils.get_package_dirs(),
					package_data=package_data,
					scripts=scripts,
					data_files=data_files,
					deb_scripts=deb_scripts,
					dst=install_path)
	bld.build()

if CLEAR_BUILD:
	libutils.clear_build()

os.system('rm -rf MANIFEST')
os.system('rm -rf src/script/sk1')
