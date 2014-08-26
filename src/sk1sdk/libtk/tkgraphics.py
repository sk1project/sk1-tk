# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

class NumWriter:
	
	def __init__(self, canvas = None):
		self.canvas = canvas
		self.x=0
		self.y=0
		self.color = 'black'
		
	def write(self, text=None, color=None, x=0, y=0):
		if text is None:
			return
		if color is not None:
			self.color=color
		self.x=x
		self.y=y
		for num in text:						
			if num=='0':
				self.canvas.create_rectangle (self.x, self.y, self.x+3, self.y+4, outline=self.color)
				self.x+=5
			elif num=='.':
				self.canvas.create_line (self.x, self.y+4, 
										 self.x+1, self.y+4, 
										 fill=self.color)
				self.x+=2
			elif num=='1':
				self.canvas.create_line (self.x, self.y, 
										 self.x+1, self.y, 
										 self.x+1, self.y+5, 
										 fill=self.color)
				self.x+=3
			elif num=='2':
				self.canvas.create_line (self.x, self.y, 
										 self.x+3, self.y,
										 self.x+3, self.y+2,
										 self.x, self.y+2,
										 self.x, self.y+4,
										 self.x+4, self.y+4,
										 fill=self.color)
				self.x+=5
			elif num=='3':
				self.canvas.create_line (self.x, self.y, 
										 self.x+3, self.y,
										 self.x+3, self.y+2,
										 self.x, self.y+2,
										 self.x+3, self.y+2,
										 self.x+3, self.y+4,
										 self.x, self.y+4,
										 fill=self.color)
				self.x+=5
			elif num=='4':
				self.canvas.create_line (self.x, self.y, 
										 self.x, self.y+3,
										 self.x+3, self.y+3,
										 self.x+3, self.y,
										 self.x+3, self.y+5,
										 fill=self.color)
				self.x+=5
			elif num=='5':
				self.canvas.create_line (self.x+4, self.y,
										 self.x, self.y, 
										 self.x, self.y+2,
										 self.x+3, self.y+2,
										 self.x+3, self.y+4,
										 self.x, self.y+4,
										 fill=self.color)
				self.x+=5	
			elif num=='6':
				self.canvas.create_line (self.x+3, self.y,
										 self.x, self.y, 
										 self.x, self.y+2,
										 self.x+3, self.y+2,
										 self.x+3, self.y+4,
										 self.x, self.y+4,
										 self.x, self.y,
										 fill=self.color)
				self.x+=5		
			elif num=='7':
				self.canvas.create_line (self.x, self.y, 
										 self.x+3, self.y,
										 self.x+3, self.y+1,
										 self.x+1, self.y+3,
										 self.x+1, self.y+5,
										 fill=self.color)
				self.x+=5
			elif num=='8':
				self.canvas.create_rectangle (self.x, self.y, self.x+3, self.y+4, outline=self.color)
				self.canvas.create_rectangle (self.x, self.y, self.x+3, self.y+2, outline=self.color)
				self.x+=5
			elif num=='9':
				self.canvas.create_line (self.x+1, self.y+4,
										 self.x+3, self.y+4,
										 self.x+3, self.y,
										 self.x, self.y,
										 self.x, self.y+2,
										 self.x+3, self.y+2,
										 fill=self.color)
				self.x+=5					
			elif num=='-':
				self.canvas.create_line (self.x+3, self.y+2,
										 self.x, self.y+2,
										 fill=self.color)
				self.x+=4
			else:
				return
			
	def writeVertically(self, text=None, color=None, x=0, y=0):
		if text is None:
			return
		if color is not None:
			self.color=color
		self.x=x
		self.y=y
		for num in text:
			if num=='0':
				self.canvas.create_rectangle (self.x, self.y, self.x+4, self.y-3, outline=self.color)
				self.y-=5
			elif num=='.':
				self.canvas.create_line (self.x+4, self.y+1, 
										 self.x+4, self.y, 
										 fill=self.color)
				self.y-=2
			elif num=='1':
				self.canvas.create_line (self.x, self.y+1, 
										 self.x, self.y-1, 
										 self.x+5, self.y-1, 
										 fill=self.color)
				self.y-=3
			elif num=='2':
				self.canvas.create_line (self.x, self.y+1, 
										 self.x, self.y-3,
										 self.x+2, self.y-3,
										 self.x+2, self.y,
										 self.x+4, self.y,
										 self.x+4, self.y-3,
										 fill=self.color)
				self.y-=5
			elif num=='3':
				self.canvas.create_line (self.x, self.y+1, 
										 self.x, self.y-3,
										 self.x+2, self.y-3,
										 self.x+2, self.y,
										 self.x+2, self.y-3,
										 self.x+4, self.y-3,
										 self.x+4, self.y+1,
										 fill=self.color)
				self.y-=5
			elif num=='4':
				self.canvas.create_line (self.x, self.y, 
										 self.x+3, self.y,
										 self.x+3, self.y-3,
										 self.x, self.y-3,
										 self.x+5, self.y-3,
										 fill=self.color)
				self.y-=5
			elif num=='5':
				self.canvas.create_line (self.x, self.y-3,
										 self.x, self.y, 
										 self.x+2, self.y,
										 self.x+2, self.y-3,
										 self.x+4, self.y-3,
										 self.x+4, self.y+1,
										 fill=self.color)
				self.y-=5	
			elif num=='6':
				self.canvas.create_line (self.x, self.y-2,
										 self.x, self.y, 
										 self.x+2, self.y,
										 self.x+2, self.y-3,
										 self.x+4, self.y-3,
										 self.x+4, self.y,
										 self.x, self.y,
										 fill=self.color)
				self.y-=5		
			elif num=='7':
				self.canvas.create_line (self.x, self.y+1, 
										 self.x, self.y-3,
										 self.x+1, self.y-3,
										 self.x+3, self.y-1,
										 self.x+5, self.y-1,
										 fill=self.color)
				self.y-=5
			elif num=='8':
				self.canvas.create_rectangle (self.x, self.y, self.x+4, self.y-3, outline=self.color)
				self.canvas.create_rectangle (self.x, self.y, self.x+2, self.y-3, outline=self.color)
				self.y-=5
			elif num=='9':
				self.canvas.create_line (self.x+4, self.y,
										 self.x+4, self.y-3,
										 self.x, self.y-3,
										 self.x, self.y,
										 self.x+2, self.y,
										 self.x+2, self.y-2,
										 fill=self.color)
				self.y-=5
			elif num=='-':
				self.canvas.create_line (self.x+2, self.y-2,
										 self.x+2, self.y+1,
										 fill=self.color)
				self.y-=4
			else:
				return
