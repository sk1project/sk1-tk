#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

'''
USAGE: sk1 [INPUT FILE]
sk1 command without parameters just launches sK1 with new document.

sK1 is an open source vector graphics editor similar to CorelDRAW(tm), 
Adobe (R) Illustrator(tm), or Adobe (R)Freehand(tm). 
First of all sK1 is oriented for prepress industry.
sK1 Team (http://sk1project.org), copyright (C) 2007 by Igor E. Novikov.

Allowed input formats:
     AI  - Adobe Illustrator files (postscript based)
     CDR - CorelDRAW Graphics files (7-X3 versions)
     CDT - CorelDRAW templates files (7-X3 versions)
     CCX - Corel Compressed Exchange files
     CMX - Corel Presentation Exchange files (CMX1 format)
     SVG - Scalable Vector Graphics files
     FIG - XFig files
     CGM - Computer Graphics Metafile files
     AFF - Draw files
     WMF - Windows Metafile files
     SK  - Sketch/Skencil files
     SK1 - sK1 vector graphics files

Example: sk1 drawing.cdr
'''

import sys, os

if sys.argv[1]=='--help':
	print __doc__
	sys.exit(0)

_pkgdir = __path__[0]
sys.path.insert(1, _pkgdir)
_ttkdir = os.path.join(_pkgdir, 'app/lib-ttk')
sys.path.insert(1, _ttkdir)

import sys, app
app.config.sk_command = sys.argv[0]
app.main.main()
