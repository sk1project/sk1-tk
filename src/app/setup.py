#! /usr/bin/env python
	
# sK1 - A Python & Tcl/Tk based vector graphics editor for prepress.
# sK1 is a fork of Sketch/Skencil.
# Copyright (C) 2003-2007 by Igor E. Novikov

# Skencil - A Python-based interactive drawing program
# Copyright (C) 1998-2005 by Bernhard Herzog 

import sys, os

from string import split, join, strip, atoi

class ColorOutput:
	havecolor=1
	dotitles=1
	
	codes={}
	codes["reset"]="\x1b[0m"
	codes["bold"]="\x1b[01m"
	
	codes["teal"]="\x1b[36;06m"
	codes["turquoise"]="\x1b[36;01m"
	
	codes["fuscia"]="\x1b[35;01m"
	codes["purple"]="\x1b[35;06m"
	
	codes["blue"]="\x1b[34;01m"
	codes["darkblue"]="\x1b[34;06m"
	
	codes["green"]="\x1b[32;01m"
	codes["darkgreen"]="\x1b[32;06m"
	
	codes["yellow"]="\x1b[33;01m"
	codes["brown"]="\x1b[33;06m"
	
	codes["red"]="\x1b[31;01m"
	codes["darkred"]="\x1b[31;06m"
	
	def __init__(self):
		pass
	
	def xtermTitle(self, mystr):
		if havecolor and dotitles and os.environ.has_key("TERM"):
			myt=os.environ["TERM"]
			if myt in ["xterm","Eterm","aterm","rxvt"]:
				sys.stderr.write("\x1b]1;\x07\x1b]2;"+str(mystr)+"\x07")
				sys.stderr.flush()
	
	def xtermTitleReset(self):
		if havecolor and dotitles and os.environ.has_key("TERM"):
			myt=os.environ["TERM"]
			xtermTitle(os.environ["TERM"])	
	
	def notitles(self):
		"turn off title setting"
		self.dotitles=0
	
	def nocolor(self):
		"turn off colorization"
		self.havecolor=0
		for x in self.codes.keys():
			self.codes[x]=""
	
	def resetColor(self):
		return self.codes["reset"]
	
	def ctext(self, color,text):
		return self.codes[ctext]+text+self.codes["reset"]
	
	def bold(self, text):
		return self.codes["bold"]+text+self.codes["reset"]
	def white(self, text):
		return self.bold(text)
	
	def teal(self, text):
		return self.codes["teal"]+text+self.codes["reset"]
	def turquoise(self, text):
		return self.codes["turquoise"]+text+self.codes["reset"]
	def darkteal(self, text):
		return self.turquoise(text)
	
	def fuscia(self, text):
		return self.codes["fuscia"]+text+self.codes["reset"]
	def purple(self, text):
		return self.codes["purple"]+text+self.codes["reset"]
	
	def blue(self, text):
		return self.codes["blue"]+text+self.codes["reset"]
	def darkblue(self, text):
		return self.codes["darkblue"]+text+self.codes["reset"]
	
	def green(self, text):
		return self.codes["green"]+text+self.codes["reset"]
	def darkgreen(self, text):
		return self.codes["darkgreen"]+text+self.codes["reset"]
	
	def yellow(self, text):
		return self.codes["yellow"]+text+self.codes["reset"]
	def brown(self, text):
		return self.codes["brown"]+text+self.codes["reset"]
	def darkyellow(self, text):
		return self.brown(text)
	
	def red(self, text):
		return self.codes["red"]+text+self.codes["reset"]
	def darkred(self, text):
		return self.codes["darkred"]+text+self.codes["reset"]
	
class CmdLineParser:
	
	command = 'help'
	sk1_re = '/usr/local/lib/sK1_RE'
	argv = ''
	
	def __init__(self):
		argv = sys.argv[1:]
		for arg in argv:
			value = None
			if '=' in arg:
				arg, value = split(arg, '=',1)
			if arg == '--with-sK1_RE':
				if value is None:
					self.error_state(1)
				elif not os.path.isdir(value):
					self.error_state(1)
				else:
					self.sk1_re = value
			elif arg in ('-h', '--help'):
				command = 'help'
			elif arg == 'configure':
				command = 'configure'
			elif arg == 'build':
				command = 'build'
			elif arg == 'install':
				command = 'install'
			else:
				self.error_state(2, arg)
	
	def error_state(self, state=1, arg=None):
		output = ColorOutput()
		if state == 1:
			print '\n',output.yellow('ERROR:'),'Please specify correct path for option --with-sK1_RE'
			sys.exit(1)
		elif state ==2:
			print '\n',output.yellow('ERROR:'), 'Unknown option %s\n' % arg
			sys.exit(1)			
		else:
			pass

		
def main():
	parser=CmdLineParser()
	print parser.command
	print parser.sk1_re

if __name__ == '__main__':
		main()