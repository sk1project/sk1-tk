# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000, 2001, 2002 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
#       Converters
#

import math
from app import config
from app.Lib.units import unit_dict, unit_names
from uc.utils import format

length_formats = {'mm': '%.1fmm',
					'cm': '%.2fcm',
					'pt': '%.1fpt',
					'in': '%.3f"'}

def conv_length(length):
	unit = config.preferences.default_unit
	factor = unit_dict[unit]
	return length_formats.get(unit, "%f") % (length / factor)

pos_format = '(%(x)[length], %(y)[length])'
def conv_position(position):
	x, y = position
	return format(pos_format, converters, locals())

size_format = '(%(width)[length] x %(height)[length])'
def conv_size(size):
	width, height = size
	return format(size_format, converters, locals())

factor_format = '%.1f%%'
def conv_factor(factor):
	return factor_format % (100 * factor)

angle_format = '%.1fº'
def conv_angle(angle):
	angle = angle * 180 / math.pi
	while angle > 180:
		angle = angle - 360
	return angle_format % angle

converters = {'length': conv_length,
				'position': conv_position,
				'size': conv_size,
				'factor': conv_factor,
				'angle': conv_angle,
				}

