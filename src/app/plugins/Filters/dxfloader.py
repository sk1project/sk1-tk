# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Barabash Maxim
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307	USA

###Sketch Config
#type = Import
#class_name='DXFLoader'
#rx_magic = r'^\x30|^\x20\x30|^\x09\x30|^\x20\x20\x30|999'
#tk_file_type=('DXF - acad file', ('.dxf', '.DXF'))
#format_name='DXF'
#unload = 1
#standard_messages = 1
###End

#
#    Import Filter for DXF files
#



import sys, os, string

from types import StringType, TupleType
from app import _, CreatePath, Style

from app.events.warn import INTERNAL, pdebug, warn_tb
from app.io.load import GenericLoader, SketchLoadError
import app

from string import strip, atoi

from math import sqrt, atan, atan2
from math import pi, cos, sin

degrees = pi / 180.0

from app import Document, Layer, CreatePath, ContSmooth, \
		SolidPattern, EmptyPattern, RadialGradient,\
		CreateRGBColor, Point, Polar, \
		StandardColors, GetFont, PathText, SimpleText, const, UnionRects, \
		Scale, Trafo, Translation, Rotation
		
from app import Scale, Trafo, Translation, Rotation

from app.conf.const import ArcArc, ArcChord, ArcPieSlice
##base_style = Style()
##base_style.fill_pattern = EmptyPattern
##base_style.fill_transform = 1
##base_style.line_pattern = SolidPattern(StandardColors.black)
##base_style.line_width = 0.0
##base_style.line_join = const.JoinMiter
##base_style.line_cap = const.CapButt
##base_style.line_dashes = ()
##base_style.line_arrow1 = None
##base_style.line_arrow2 = None
##base_style.font = None
##base_style.font_size = 12.0

def csscolor(str):
	str = str.strip()

	if str[0] == '#':
		if len(str) == 7:
			r = atoi(str[1:3], 16) / 255.0
			g = atoi(str[3:5], 16) / 255.0
			b = atoi(str[5:7], 16) / 255.0
		elif len(str) == 4:
			# According to the CSS rules a single HEX digit is to be
			# treated as a repetition of the digit, so that for a digit
			# d the value is (16 * d + d) / 255.0 which is equal to d / 15.0
			r = atoi(str[1], 16) / 15.0
			g = atoi(str[2], 16) / 15.0
			b = atoi(str[3], 16) / 15.0
		color = CreateRGBColor(r, g, b)
	elif namedcolors.has_key(str):
		color = namedcolors[str]
	else:
		color = StandardColors.black
	return color

colors = {
		0: csscolor('#000000'),
		1: csscolor('#FF0000'),
		2: csscolor('#FFFF00'),
		3: csscolor('#00FF00'),
		4: csscolor('#00FFFF'),
		5: csscolor('#0000FF'),
		6: csscolor('#FF00FF'),
		7: csscolor('#FFFFFF'),
		8: csscolor('#414141'),
		9: csscolor('#808080'),
		10: csscolor('#FF0000'),
		11: csscolor('#FFAAAA'),
		12: csscolor('#BD0000'),
		13: csscolor('#BD7E7E'),
		14: csscolor('#810000'),
		15: csscolor('#815656'),
		16: csscolor('#680000'),
		17: csscolor('#684545'),
		18: csscolor('#4F0000'),
		19: csscolor('#4F3535'),
		20: csscolor('#FF3F00'),
		21: csscolor('#FFBFAA'),
		22: csscolor('#BD2E00'),
		23: csscolor('#BD8D7E'),
		24: csscolor('#811F00'),
		25: csscolor('#816056'),
		26: csscolor('#681900'),
		27: csscolor('#684E45'),
		28: csscolor('#4F1300'),
		29: csscolor('#4F3B35'),
		30: csscolor('#FF7F00'),
		31: csscolor('#FFD4AA'),
		32: csscolor('#BD5E00'),
		33: csscolor('#BD9D7E'),
		34: csscolor('#814000'),
		35: csscolor('#816B56'),
		36: csscolor('#683400'),
		37: csscolor('#685645'),
		38: csscolor('#4F2700'),
		39: csscolor('#4F4235'),
		40: csscolor('#FFBF00'),
		41: csscolor('#FFEAAA'),
		42: csscolor('#BD8D00'),
		43: csscolor('#BDAD7E'),
		44: csscolor('#816000'),
		45: csscolor('#817656'),
		46: csscolor('#684E00'),
		47: csscolor('#685F45'),
		48: csscolor('#4F3B00'),
		49: csscolor('#4F4935'),
		50: csscolor('#FFFF00'),
		51: csscolor('#FFFFAA'),
		52: csscolor('#BDBD00'),
		53: csscolor('#BDBD7E'),
		54: csscolor('#818100'),
		55: csscolor('#818156'),
		56: csscolor('#686800'),
		57: csscolor('#686845'),
		58: csscolor('#4F4F00'),
		59: csscolor('#4F4F35'),
		60: csscolor('#BFFF00'),
		61: csscolor('#EAFFAA'),
		62: csscolor('#8DBD00'),
		63: csscolor('#ADBD7E'),
		64: csscolor('#608100'),
		65: csscolor('#768156'),
		66: csscolor('#4E6800'),
		67: csscolor('#5F6845'),
		68: csscolor('#3B4F00'),
		69: csscolor('#494F35'),
		70: csscolor('#7FFF00'),
		71: csscolor('#D4FFAA'),
		72: csscolor('#5EBD00'),
		73: csscolor('#9DBD7E'),
		74: csscolor('#408100'),
		75: csscolor('#6B8156'),
		76: csscolor('#346800'),
		77: csscolor('#566845'),
		78: csscolor('#274F00'),
		79: csscolor('#424F35'),
		80: csscolor('#3FFF00'),
		81: csscolor('#BFFFAA'),
		82: csscolor('#2EBD00'),
		83: csscolor('#8DBD7E'),
		84: csscolor('#1F8100'),
		85: csscolor('#608156'),
		86: csscolor('#196800'),
		87: csscolor('#4E6845'),
		88: csscolor('#134F00'),
		89: csscolor('#3B4F35'),
		90: csscolor('#00FF00'),
		91: csscolor('#AAFFAA'),
		92: csscolor('#00BD00'),
		93: csscolor('#7EBD7E'),
		94: csscolor('#008100'),
		95: csscolor('#568156'),
		96: csscolor('#006800'),
		97: csscolor('#456845'),
		98: csscolor('#004F00'),
		99: csscolor('#354F35'),
		100: csscolor('#00FF3F'),
		101: csscolor('#AAFFBF'),
		102: csscolor('#00BD2E'),
		103: csscolor('#7EBD8D'),
		104: csscolor('#00811F'),
		105: csscolor('#568160'),
		106: csscolor('#006819'),
		107: csscolor('#45684E'),
		108: csscolor('#004F13'),
		109: csscolor('#354F3B'),
		110: csscolor('#00FF7F'),
		111: csscolor('#AAFFD4'),
		112: csscolor('#00BD5E'),
		113: csscolor('#7EBD9D'),
		114: csscolor('#008140'),
		115: csscolor('#56816B'),
		116: csscolor('#006834'),
		117: csscolor('#456856'),
		118: csscolor('#004F27'),
		119: csscolor('#354F42'),
		120: csscolor('#00FFBF'),
		121: csscolor('#AAFFEA'),
		122: csscolor('#00BD8D'),
		123: csscolor('#7EBDAD'),
		124: csscolor('#008160'),
		125: csscolor('#568176'),
		126: csscolor('#00684E'),
		127: csscolor('#45685F'),
		128: csscolor('#004F3B'),
		129: csscolor('#354F49'),
		130: csscolor('#00FFFF'),
		131: csscolor('#AAFFFF'),
		132: csscolor('#00BDBD'),
		133: csscolor('#7EBDBD'),
		134: csscolor('#008181'),
		135: csscolor('#568181'),
		136: csscolor('#006868'),
		137: csscolor('#456868'),
		138: csscolor('#004F4F'),
		139: csscolor('#354F4F'),
		140: csscolor('#00BFFF'),
		141: csscolor('#AAEAFF'),
		142: csscolor('#008DBD'),
		143: csscolor('#7EADBD'),
		144: csscolor('#006081'),
		145: csscolor('#567681'),
		146: csscolor('#004E68'),
		147: csscolor('#455F68'),
		148: csscolor('#003B4F'),
		149: csscolor('#35494F'),
		150: csscolor('#007FFF'),
		151: csscolor('#AAD4FF'),
		152: csscolor('#005EBD'),
		153: csscolor('#7E9DBD'),
		154: csscolor('#004081'),
		155: csscolor('#566B81'),
		156: csscolor('#003468'),
		157: csscolor('#455668'),
		158: csscolor('#00274F'),
		159: csscolor('#35424F'),
		160: csscolor('#003FFF'),
		161: csscolor('#AABFFF'),
		162: csscolor('#002EBD'),
		163: csscolor('#7E8DBD'),
		164: csscolor('#001F81'),
		165: csscolor('#566081'),
		166: csscolor('#001968'),
		167: csscolor('#454E68'),
		168: csscolor('#00134F'),
		169: csscolor('#353B4F'),
		170: csscolor('#0000FF'),
		171: csscolor('#AAAAFF'),
		172: csscolor('#0000BD'),
		173: csscolor('#7E7EBD'),
		174: csscolor('#000081'),
		175: csscolor('#565681'),
		176: csscolor('#000068'),
		177: csscolor('#454568'),
		178: csscolor('#00004F'),
		179: csscolor('#35354F'),
		180: csscolor('#3F00FF'),
		181: csscolor('#BFAAFF'),
		182: csscolor('#2E00BD'),
		183: csscolor('#8D7EBD'),
		184: csscolor('#1F0081'),
		185: csscolor('#605681'),
		186: csscolor('#190068'),
		187: csscolor('#4E4568'),
		188: csscolor('#13004F'),
		189: csscolor('#3B354F'),
		190: csscolor('#7F00FF'),
		191: csscolor('#D4AAFF'),
		192: csscolor('#5E00BD'),
		193: csscolor('#9D7EBD'),
		194: csscolor('#400081'),
		195: csscolor('#6B5681'),
		196: csscolor('#340068'),
		197: csscolor('#564568'),
		198: csscolor('#27004F'),
		199: csscolor('#42354F'),
		200: csscolor('#BF00FF'),
		201: csscolor('#EAAAFF'),
		202: csscolor('#8D00BD'),
		203: csscolor('#AD7EBD'),
		204: csscolor('#600081'),
		205: csscolor('#765681'),
		206: csscolor('#4E0068'),
		207: csscolor('#5F4568'),
		208: csscolor('#3B004F'),
		209: csscolor('#49354F'),
		210: csscolor('#FF00FF'),
		211: csscolor('#FFAAFF'),
		212: csscolor('#BD00BD'),
		213: csscolor('#BD7EBD'),
		214: csscolor('#810081'),
		215: csscolor('#815681'),
		216: csscolor('#680068'),
		217: csscolor('#684568'),
		218: csscolor('#4F004F'),
		219: csscolor('#4F354F'),
		220: csscolor('#FF00BF'),
		221: csscolor('#FFAAEA'),
		222: csscolor('#BD008D'),
		223: csscolor('#BD7EAD'),
		224: csscolor('#810060'),
		225: csscolor('#815676'),
		226: csscolor('#68004E'),
		227: csscolor('#68455F'),
		228: csscolor('#4F003B'),
		229: csscolor('#4F3549'),
		230: csscolor('#FF007F'),
		231: csscolor('#FFAAD4'),
		232: csscolor('#BD005E'),
		233: csscolor('#BD7E9D'),
		234: csscolor('#810040'),
		235: csscolor('#81566B'),
		236: csscolor('#680034'),
		237: csscolor('#684556'),
		238: csscolor('#4F0027'),
		239: csscolor('#4F3542'),
		240: csscolor('#FF003F'),
		241: csscolor('#FFAABF'),
		242: csscolor('#BD002E'),
		243: csscolor('#BD7E8D'),
		244: csscolor('#81001F'),
		245: csscolor('#815660'),
		246: csscolor('#680019'),
		247: csscolor('#68454E'),
		248: csscolor('#4F0013'),
		249: csscolor('#4F353B'),
		250: csscolor('#333333'),
		251: csscolor('#505050'),
		252: csscolor('#696969'),
		253: csscolor('#828282'),
		254: csscolor('#BEBEBE'),
		255: csscolor('#FFFFFF')
		}

def convert(code, value):
	"""Convert a string to the correct Python type based on its dxf code.
		code types:
		ints = 60-79, 170-179, 270-289, 370-389, 400-409, 1060-1070
		longs = 90-99, 420-429, 440-459, 1071
		floats = 10-39, 40-59, 110-139, 140-149, 210-239, 460-469, 1010-1059
		hex = 105, 310-379, 390-399
		strings = 0-9, 100, 102, 300-309, 410-419, 430-439, 470-479, 999, 1000-1009
		"""
	if type(code) == StringType:
		code = int(code)
	if 59 < code < 80 or 169 < code < 180 or 269 < code < 290 or 369 < code < 390 or 399 < code < 410 or 1059 < code < 1071:
		value = int(float(value))
	elif 89 < code < 100 or 419 < code < 430 or 439 < code < 460 or code == 1071:
		value = long(float(value))
	elif 9 < code < 60 or 109 < code < 150 or 209 < code < 240 or 459 < code < 470 or 1009 < code < 1060:
		value = float(value)
	elif code == 105 or 309 < code < 380 or 389 < code < 400:
		value = int(value, 16) # should be left as string?
	else: # it's already a string so do nothing
		pass
	return value

class DXFLoader(GenericLoader):

	functions={"$EXTMIN": 'read_EXTMIN',
				"$EXTMAX": 'read_EXTMAX',
				"$INSUNITS": 'read_INSUNITS',
				"TABLE": 'load_TABLE',
				"BLOCK": 'load_BLOCK',
				"LINE": 'line',
				"POLYLINE": 'polyline',
				"SEQEND": 'seqend',
				"VERTEX": 'vertex',
				"CIRCLE": 'circle',
				"ARC": 'arc',
				"ELLIPSE": 'ellips',
				"SOLID": 'solid',
				"LWPOLYLINE": 'lwpolyline'
					}

	def __init__(self, file, filename, match):
		GenericLoader.__init__(self, file, filename, match)
		
		self.file = file
		self.style_dict = {}
		self.last_record1 = None
		self.last_record2 = None
		self.EXTMIN = (-4.135358, -5.847957)
		self.EXTMAX = (4.135358, 5.847957)
		self.INSUNITS = 0
		self.unit_to_pt = 72
		self.close_path = 0
		self.update_trafo()
		
		self.curstyle = Style()


	def update_trafo(self):
		print self.INSUNITS, 'unit_to_pt', self.unit_to_pt
		x = - self.EXTMIN[0] * self.unit_to_pt
		y = - self.EXTMIN[1] * self.unit_to_pt
		self.trafo = Trafo(self.unit_to_pt, 0, 0, self.unit_to_pt, x, y)

	def read_EXTMIN(self):
		param={	'10': 0.0, # X coordinat
				'20': 0.0  # y coordinat
				}
		param = self.read_param(param)
		self.EXTMIN = (param['10'],param['20'])
		print self.EXTMIN
		self.update_trafo()

	def read_EXTMAX(self):
		param={	'10': 0.0, # X coordinat
				'20': 0.0  # y coordinat
				}
		param = self.read_param(param)
		self.EXTMAX = (param['10'],param['20'])
		print self.EXTMAX
		self.update_trafo()

	def read_INSUNITS(self):
		#	unit to pt
		unit = {	0:  72, # Unitless 
		1 : 72.0,# Inches
		2 : 72.0 * 12,# Feet
		3 : 72.0 * 63360,# Miles
		4 : 72 / 2.54 / 10,# Millimeters
		5 : 72 / 2.54,# Centimeters
		6 : 100 * 72 / 2.54,# Meters
		7 : 1000 * 100 * 72 / 2.54,# Kilometers
		8 : 1/1000000 * 72,# Microinches
		9 : 1/1000 * 72.0,# Mils
		10 : 72.0 * 36,# Yards
		11 : 0.00000000001 * 100 * 72 / 2.54,# Angstroms
		12 : 0.0000000001 * 100 * 72 / 2.54,# Nanometers
		13 : 0.0000001 * 100 * 72 / 2.54,# Microns
		14 : 10 * 72 / 2.54,# Decimeters
		15 : 10 * 100 * 72 / 2.54,# Decameters
		16 : 100 * 100 * 72 / 2.54,# Hectometers
		17 : 1000000 * 100 * 72 / 2.54,# Gigameters
		18 : 1.49600 * 1000000000000 * 100 * 72 / 2.54,# Astronomical units
		19 : 9.46050 * 10000000000000000 * 100 * 72 / 2.54,#  Light years
		20 : 3.08570 * 100000000000000000 * 100 * 72 / 2.54 # Parsecs
		}
		
		param={	'70': 0
				}
		
		param = self.read_param(param)
		self.INSUNITS = param['70']
		
		if self.INSUNITS in unit:
					self.unit_to_pt = unit[self.INSUNITS]
		else:
			self.unit_to_pt = 72.0
		
		self.update_trafo()


	def load_TABLE(self):
		param={	'2': '', # Table name
				'70': 0 # Maximum number of entries in table
				}
		param = self.read_param(param)
		table_name = param['2']
		table_number = param['70']
		print '****', table_name, table_number
		
		line1, line2 = self.read_record()
		while line1 or line2:
			if line1 == '0' and line2 == 'ENDTAB':
				break
			if table_name == 'LTYPE':
				self.load_LTYPE()
			line1, line2 = self.read_record()

	def load_LTYPE(self):
		param={ '2': '', # Linetype name
				'3': '', # Descriptive text for linetype
				'73': 0, # The number of linetype elements
				'40': 0, # Total pattern length
				'49': [], # Dash, dot or space length (one entry per element)
				}
		line1, line2 = self.read_record()
		while line1 or line2:
			if line1 == '0':
				self.push_record(line1, line2)
				break
			else:
				if line1 in param:
					value = convert(line1, line2)
					if line1 == '49':
						param[line1].append(abs(value))
					else:
						param[line1] = value
			line1, line2 = self.read_record()
		print param
		name = param['2']
##		if param['3']:
##			name = param['3']
##		else:
##			name = param['2']
		style = Style()
		style.line_dashes = tuple(param['49'])
		style = style.AsDynamicStyle()
		style.SetName(name)
		self.style_dict[name] = style


	def load_BLOCK(self):
		param={	'2': '', # Block name
				'10': 0.0, # X Base point
				'20': 0.0, # Y Base point
				#'30': 0.0, # Z Base point 
				}
		param = self.read_param(param)
		block_name = param['2']
		print '****', block_name
		
		line1, line2 = self.read_record()
		while line1 or line2:
			if line1 == '0' and line2 == 'ENDBLK':
				break
			#FIXME
			pass
			
			line1, line2 = self.read_record()

	def line(self):
		param={	'10': None, # X coordinat
				'20': None, # y coordinat
				#'30': None, # Z coordinat
				
				'11': None, # X coordinat endpoint
				'21': None, # y coordinat endpoint
				#'31': None, # z coordinat endpoint
				}
		param = self.read_param(param)
##		print 'LINE param',param
		self.close_path = 0
		self.path = CreatePath()
		self.path.AppendLine(self.trafo(param['10'], param['20']))
		self.path.AppendLine(self.trafo(param['11'], param['21']))
		self.bezier(self.path,)
##		print 'Create LINE'

	def polyline(self):
		param={	'70': 0, # bit codes for Polyline entity
				'40': 0.01, 
				'62': None #color
				}
		param = self.read_param(param)
		self.close_path = 0
		self.path = CreatePath()
		self.curstyle.line_width=param['40']*72
		if param['62'] is not None:
			self.curstyle.line_pattern = SolidPattern(colors[param['62']])
		# if Group 70 Flag bit value set 1 This is a closed Polyline
		self.close_path = param['70'] & 1 == 1


	def vertex(self):
		param={#'62': 7, # color
				#'6': 'CONTINUOUS', # style
				'10': None, # X coordinat
				'20': None, # y coordinat
				'42': 0.0  # Bulge 
				}
		param = self.read_param(param)
		if param['10'] == None:
			print '%%%%%%%%%%'
			return
		if param['42']==0:
			# print 'AppendLine',param
			self.path.AppendLine(self.trafo(param['10'], param['20']))
		else:
			
##			if self.path.len==0:
##				print 'first vertex'
##				self.path.AppendLine(self.trafo(param['10'], param['20']))
##				return
##				
##			print 'AppendBezier', param
##			x, y = param['10']*72, param['20']*72
##			
##			p1=self.path.Node(-1)
##			p2=Point(param['10']*72, param['20']*72)
##			bulge=param['42']
##			
##			x1 =p1[0]
##			y1 =p1[1]
##			x2 =p2[0]
##			y2 =p2[1]
##			print x1, x2, y1, y2
##			chorda=sqrt((x2-x1)**2+(y2-y1)**2)
##			s = bulge * chorda / 2
##			if s == 0:
##				return
##			radius = abs(((chorda / 2)**2 + s**2) / (2 * s))
##			angle = abs((4*atan(bulge)))
##			delta = (180 - angle)/2
##			angle2=abs(atan2(y2-y1, x2-x1))
##			begin_angle=angle+angle2
##			end_angle=-1*(angle+angle2)
##			print '#########', angle2
##			if bulge > 0:
##				delta = -delta
##			radial = chorda * radius
####			rmat = Rotation(delta, 3)
##
##			print chorda, s, radius, angle
##			print
##			self.ellipse(radius, 0, 0, radius, x, y, begin_angle, end_angle,ArcArc)
			self.path.AppendLine(self.trafo(param['10'], param['20']))
##		print param

	def seqend(self):
		if self.path.len > 1:
			#print 'CREAT PATH'
			if self.close_path:
				if self.path.Node(0)!=self.path.Node(-1):
					#print 'add last node!!!!!!!!!!!'
					#print self.path.Node(0)
					#print self.path.Node(-1)
					self.path.AppendLine(self.path.Node(0))
				self.path.ClosePath()
				self.close_path = 0
			self.prop_stack.AddStyle(self.curstyle.Duplicate())
			self.bezier(self.path,)


	def circle(self):
		param={	'10': None, # X coordinat center
				'20': None, # Y coordinat center
				#'30': None, # Z coordinat center
				'40': 0.0  # radius
				}
		param = self.read_param(param)
		
		x = param['10']
		y = param['20']
		r = param['40']
		
		t = self.trafo(Trafo(r,0,0,r,x,y))
		
		apply(self.ellipse, t.coeff())

	def arc(self):
		param={	'10': None, # X coordinat center
				'20': None, # Y coordinat center
				#'30': None, # Z coordinat center
				'40': 0.0, # radius
				'50': 0.0, # Start angle
				'51': 0.0 # End angle
				}
		param = self.read_param(param)
		
		x = param['10']
		y = param['20']
		r = param['40']
		start_angle = param['50'] * degrees
		end_angle = param['51'] * degrees
		
		t = self.trafo(Trafo(r,0,0,r,x,y))
		
		r, w1, w2, r, x, y = t.coeff()
		
		apply(self.ellipse, (r, w1, w2, r, x, y, start_angle, end_angle, ArcArc))
		

	def ellips(self):
		param={	'10': 0.0, # X coordinat center
				'20': 0.0, # Y coordinat center
				#'30': 0.0, # Z coordinat center
				'11': 0.0, # Endpoint of major axis, relative to the center
				'21': 0.0,
				#'31': 0.0,
				'40': 0.0, # Ratio of minor axis to major axis
				'41': 0.0, # Start parameter (this value is 0.0 for a full ellipse)
				'42': 0.0, # End parameter (this value is 2pi for a full ellipse)
				}
		param = self.read_param(param)
		
		cx = param['10']
		cy = param['20']
		
		rx = sqrt(param['21']**2 + param['11']**2)
		ry = rx * param['40']
		
		start_angle = param['41']
		end_angle = param['42']
		
		angle=atan2(param['21'], param['11'])
		
		center = self.trafo(cx, cy)
		radius = self.trafo.DTransform(rx, ry)
		trafo = Trafo(radius.x, 0, 0, radius.y)
		trafo = Rotation(angle)(trafo)
		trafo = Translation(center)(trafo)
		rx, w1, w2, ry, cx, cy = trafo.coeff()
		apply(self.ellipse, (rx, w1, w2, ry, cx, cy, start_angle, end_angle, ArcArc))


	def solid(self):
		param={	'10': None, 
				'20': None, 
				#'30': None, 
				'11': None, 
				'21': None, 
				#'31': None,
				'12': None, 
				'22': None, 
				#'32': None,
				'13': None, 
				'23': None,
				#'33': None, 
				}
		param = self.read_param(param)
		
		self.path = CreatePath()
		self.path.AppendLine(self.trafo(param['10'], param['20']))
		self.path.AppendLine(self.trafo(param['11'], param['21']))
		self.path.AppendLine(self.trafo(param['12'], param['22']))
		self.path.AppendLine(self.trafo(param['13'], param['23']))
		
		self.path.ClosePath()
		
		self.bezier(self.path,)

	def lwpolyline(self):
		param={ '90': 0, # Number of vertices
				'70': 0, # bit codes for Polyline entity
				'40': None, # Starting width
				'43': 0
				}
		param = self.read_param(param,[10])
		
		self.close_path = 0
		self.path = CreatePath()
		
		if param['40'] is not None:
			line_width = param['40']*72
		else:
			line_width = param['43']
		
		self.curstyle.line_width = line_width 
		
		# if Group 70 Flag bit value set 1 This is a closed Polyline
		self.close_path = param['70'] & 1 == 1
		
		for i in xrange(param['90']):
			vertex={ '10': None,
					'20': None,
					'42': 0.0
					}
			line1, line2 = self.read_record()
			vertex[line1] = convert(line1, line2)
			
			line1, line2 = self.read_record()
			vertex[line1] = convert(line1, line2)
			
			line1, line2 = self.read_record()
			if line1 == '42':
				vertex[line1] = convert(line1, line2)
			else:
				self.push_record(line1, line2)
			
			x = vertex['10']
			y = vertex['20']
			
			self.path.AppendLine(self.trafo(x, y))
			
		self.seqend()
		

###########################################################################

	def get_compiled(self):
		funclist={}
		for char, name in self.functions.items():
			method = getattr(self, name)
			argc = method.im_func.func_code.co_argcount - 1
			funclist[char] = (method, argc)
		return funclist

	def push_record(self, line1, line2):
		# save data in buffer
		self.last_record1 = line1
		self.last_record2 = line2

	def pop_record(self):
		# restore data of buffer
		line1 = self.last_record1
		line2 = self.last_record2
		self.last_record1 = None
		self.last_record2 = None
		return line1, line2

	def read_record(self):
		# if the buffer is empty read two lines from a file
		if self.last_record1 is None:
			line1 = self.file.readline().strip()
			line2 = self.file.readline().strip()
		else:
			line1, line2 = self.pop_record()
		return line1, line2

	def read_param(self, param, stop=None):
		# read data and fill in the dictionary
		if stop is None:
			stop = [0, 9]
		line1, line2 = self.read_record()
		while line1 or line2:
			if int(line1) in stop:
				self.push_record(line1, line2)
				return param
			else:
				if line1 in param:
					param[line1] = convert(line1, line2)
			line1,line2 = self.read_record()
#		##print '##false'
		return False

	def find_record(self, code1, code2):
		# read data until to not overlap line1 == code1 and line2 == code2
		# return True
		# else return False
		
		line1, line2 = self.read_record()
		while line1 or line2:
			if line1 == code1 and line2 == code2:
				return True
			line1, line2 = self.read_record()
#		##print '#false',code2
		return False



	def load_section(self):
		return_code = False
		param={	'2': '', # name section
				}
		param = self.read_param(param)
		name=param['2']
		print '**',name
##		if name == 'HEADER':
##			return_code = self.load_subsection()
####		elif name == 'CLASSES':
####			pass
##		elif name == 'TABLES':
##			return_code = self.load_subsection()
####		elif name == 'BLOCKS':
####			pass
##		elif name == 'ENTITIES':
##			return_code = self.load_subsection()
####		elif name == 'OBJECTS':
####			pass
####		elif name == 'THUMBNAILIMAGE':
####			pass
##		else:
##			return_code = self.find_record('0','ENDSEC')
##		return return_code
		line1, line2 = self.read_record()
		while line1 or line2:
			if line1 == '0' and line2 == 'ENDSEC':
				return_code = True
				break
			else:
				if line1 == '0' or line1 == '9':
					self.run(line2)
			line1, line2 = self.read_record()
		return return_code


	def interpret(self):
		file = self.file
		if type(file) == StringType:
			file = open(file, 'r')
		file.seek(0)
		readline = file.readline
		fileinfo = os.stat(self.filename)
		totalsize = fileinfo[6]
		
		section = self.find_record('0','SECTION')
		if section:
			while section:
				if not self.load_section():
					warn_tb(INTERNAL, _('DXFLoader: error. Non find end of sections'))
					return
				else:
					section = self.find_record('0', 'SECTION')
		else:
			warn_tb(INTERNAL, _('DXFLoader: error. Non find any sections'))

	def run(self,keyword, *args):
		if keyword is None:
			return
		unknown_operator = (None, None)
		funclist = self.funclist
		if keyword is not None:
			method, argc = funclist.get(keyword, unknown_operator)
			if method is not None:
				try:
					##print '******', keyword
					if len(args):
						i = 0
						while i<len(args):
							apply(method, args[i:argc+i])
							i+=argc
					else:
						method()
						
				except:
					warn_tb(INTERNAL, 'DXFLoader: error')
			else:
				print 'Warning not interpreted', keyword



	def Load(self):
		import time
		start_time = time.clock()
		#print '		************ "DXF_objects" **************'
		self.funclist = self.get_compiled()
		self.document()
		self.layer(name = _("DXF_objects"))
		self.interpret()
		self.end_all()
		for style in self.style_dict.values():
			self.object.load_AddStyle(style)
		self.object.load_Completed()
		print 'times',time.clock() - start_time
		return self.object

