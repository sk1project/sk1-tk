#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.


import sys, os

_pkgdir = __path__[0]
sys.path.insert(1, _pkgdir)
_ttkdir = os.path.join(_pkgdir, 'app/UI/lib-ttk')
sys.path.insert(1, _ttkdir)

import app
app.config.sk_command = sys.argv[0]
app.main.main()
