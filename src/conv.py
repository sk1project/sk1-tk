# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2002, 2006 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import sys, os

def print_info():
	print '\nUSAGE: uniconvertor.sh [INPUT FILE] [OUTPUT FILE]\n'	
	print 'Converts one vector graphics format to another using sK1 engine.'
	print '\n Allowed input formats: '
	print '     AI  - Adobe Illustrator files (postscript based)'
	print '     CDR - CorelDRAW Graphics files (7-X3 versions)'
	print '     CMX - Corel Presentation Exchange files (CMX1 format)'
	print '     SVG - Scalable Vector Graphics files'
	print '     FIG - XFig files'
	print '     CGM - Computer Graphics Metafile files'
	print '     AFF - Draw files'
	print '     WMF - Windows Metafile files'
	print '     SK  - Sketch/Skencil files'
	print '     SK1 - sK1 vector graphics files'
	print '\n Allowed output formats:'
	print '     AI  - Adobe Illustrator files (postscript based)'
	print '     SVG - Scalable Vector Graphics files'
	print '     CGM - Computer Graphics Metafile files'
	print '     WMF - Windows Metafile files'
	print '     SK  - Sketch/Skencil files'
	print '     SK1 - sK1 vector graphics files'
	print '\nExample: uniconvertor.sh drawing.cdr drawing.svg\n'


if sys.argv[1]=='--help':
	print_info()
	sys.exit(0)
if os.path.isfile(sys.argv[1])==0:
	print '\nERROR: %s file is not found!\n' % sys.argv[1]
	sys.exit(1)
if len(sys.argv) != 3 or os.path.isfile(sys.argv[1])==0:
	print '\nERROR: incorrect arguments!\n'
	print_info()
	sys.exit(1)

from app.io import load
from app.plugins import plugins
import app

app.init_lib()

doc = load.load_drawing(sys.argv[1])
extension = os.path.splitext(sys.argv[2])[1]
fileformat = plugins.guess_export_plugin(extension)
if fileformat:
	saver = plugins.find_export_plugin(fileformat)
	saver(doc, sys.argv[2])
else:
	sys.stderr.write('ERROR: unrecognized extension %s\n' % extension)
	sys.exit(1)
doc.Destroy()
sys.exit(0)