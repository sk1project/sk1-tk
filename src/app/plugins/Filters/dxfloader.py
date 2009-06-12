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
#rx_magic = r'^\x30|^\x20\x30|^\x09\x30|^\x20\x20\x30'
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

from math import sqrt, degrees, atan, atan2



from app import Document, Layer, CreatePath, ContSmooth, \
		SolidPattern, EmptyPattern, LinearGradient, RadialGradient,\
		CreateRGBColor, CreateCMYKColor, MultiGradient, Trafo, Point, Polar, \
		StandardColors, GetFont, PathText, SimpleText, const, UnionRects, Rotation 
		
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
				"LINE": 'line',
				"POLYLINE": 'polyline',
				"SEQEND": 'seqend',
				"VERTEX": 'vertex',
				"CIRCLE": 'circle'
					}

	def __init__(self, file, filename, match):
		GenericLoader.__init__(self, file, filename, match)
		
		self.file = file
		self.last_record1 = None
		self.last_record2 = None
		self.EXTMIN = (-4.135358, -5.847957)
		self.EXTMAX = (4.135358, 5.847957)
		self.close_path = 0
		self.trafo = Trafo(72, 0, 0, 72, 0, 0)
		
		self.curstyle = Style()

	def read_EXTMIN(self):
		param={	'10': 0.0, # X coordinat
				'20': 0.0  # y coordinat
				}
		param = self.read_param(param)
		self.EXTMIN = (param['10'],param['20'])
		print self.EXTMIN

	def read_EXTMAX(self):
		param={	'10': 0.0, # X coordinat
				'20': 0.0  # y coordinat
				}
		param = self.read_param(param)
		self.EXTMAX = (param['10'],param['20'])
		print self.EXTMAX

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
				'40': 0.01
				}
		param = self.read_param(param)
		self.close_path = 0
		self.path = CreatePath()
		self.curstyle.line_width=param['40']*72
		
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
			print 'AppendLine',param
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
			print 'CREAT PATH'
			if self.close_path:
				if self.path.Node(0)!=self.path.Node(-1):
					print 'add last node!!!!!!!!!!!'
					print self.path.Node(0)
					print self.path.Node(-1)
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

	def read_param(self, param):
		# read data and fill in the dictionary
		line1, line2 = self.read_record()
		while line1 or line2:
			if int(line1) == 0 or int(line1) == 9:
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

	def load_HEADER(self):
		#load section HEADER
		##print '**** HEADER'
		line1,line2 = self.read_record()
		while line1 or line2:
			if line1 == '0' and line2 == 'ENDSEC':
				##print '**** END HEADER'
				return True
			else:
				self.run(line2)
			line1,line2 = self.read_record()
		##print 'false'
		return False

	def load_ENTITIES(self):
		#load section ENTITIES
		##print '**** ENTITIES'
		line1, line2 = self.read_record()
		while line1 or line2:
			if line1 == '0' and line2 == 'ENDSEC':
				##print '**** END HEADER'
				return True
			else:
				self.run(line2)
			line1, line2 = self.read_record()
		##print 'false'
		return False

	def load_section(self):
		return_code = False
		param={	'2': '', # name section
				}
		param = self.read_param(param)
		name=param['2']
		print '**',name
		if name == 'HEADER':
			return_code = self.load_HEADER()
##		elif name == 'CLASSES':
##			pass
##		elif name == 'TABLES':
##			pass
##		elif name == 'BLOCKS':
##			pass
		elif name == 'ENTITIES':
			return_code = self.load_ENTITIES()
##		elif name == 'OBJECTS':
##			pass
##		elif name == 'THUMBNAILIMAGE':
##			pass
		else:
			return_code = self.find_record('0','ENDSEC')
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
					##print keyword
					if len(args):
						i = 0
						while i<len(args):
							apply(method, args[i:argc+i])
							i+=argc
					else:
						method()
						
				except:
					warn_tb(INTERNAL, 'DXFLoader: error')


	def Load(self):
		import time
		start_time = time.clock()
		#print '		************ "DXF_objects" **************'
		self.funclist = self.get_compiled()
		self.document()
		self.layer(name = _("DXF_objects"))
		self.interpret()
		self.end_all()
		self.object.load_Completed()
		print 'times',time.clock() - start_time
		return self.object

