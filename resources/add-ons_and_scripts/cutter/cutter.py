# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Maxim Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

__version__='0.1a'

from app import _
import app, os, string, sys
from app.UI.dialogs.dialog import ModalDialog

from app import dialogman

from Ttk import TButton, TLabel, TFrame, TNotebook, TLabelframe, TCombobox,TCheckbutton
from Tkinter import DoubleVar, StringVar, BooleanVar, IntVar
from app.UI.ttk_ext import TSpinbox, TEntryExt
from Tkinter import Text
from Tkinter import TOP,LEFT,RIGHT,BOTTOM,X,Y,BOTH,W,S,N,E,NORMAL,DISABLED,END

from app.UI.tkext import UpdatedButton, UpdatedCheckbutton, UpdatedRadiobutton


from app import CreatePath, PolyBezier
from app import Bezier, EmptyPattern, Point, Polar, Trafo


from math import pi, cos, sin

degrees = pi / 180.0

##import struct # - по окончании удалить

from app.conf.configurator import XMLPrefReader, ErrorHandler, EntityResolver, DTDHandler
from app.utils import os_utils
##from app.conf import const
from Tkinter import StringVar

##
##from math import pi, atan2


EXT_FILE_OPTIONS='.xml'
NAME_FILE_OPTIONS='Default Cutter'
EXT_OUTPUT_FILE='.plt'

cutter_options_types=(
						(_("sK1 xml cutter"), ('*.xml', '*.XML')),
						(_("All Files"),	 '*')
						)

cutter_types=			(
						(_("PLT - Plotter file"), ('*.plt', '*.PLT'))
						)

plt_options={
				'max_steps_across':'',
				'max_steps_down':'',
				'per_inch':'1016',
				'first_command':'IN',
				'final_command':'PU',
				'move_command':'PU',
				'draw_command':'PD',
				'XY_separator':',',
				'coordinate_separator':',',
				'command_terminator':';',
				'page_feed_command':'',
				'page_terminator_command':'',
				'name': 'Generic Cutter HPGL',
				'output': ''
			}

########### PLS

# Fault Tolerance for flattening Beziers.
# If you find the curves not smooth enough, lower this value.
EPS=0.5

def rndtoint(num):
	return int(round(num))

def cr(P1, P2):
	return P1.x * P2.y - P1.y * P2.x

def FlattenPath(P0, P1, P2, P3):

	P4=(P0 + P1) / 2
	P5=(P1 + P2) / 2
	P6=(P2 + P3) / 2
	P7=(P4 + P5) / 2
	P8=(P5 + P6) / 2
	P9=(P7 + P8) / 2

	B=P3 - P0
	S=P9 - P0
	C1=P1 - P0
	C2=P2 - P3

	# I couldn't find an example of a flattening algorithm so I came up
	# with the following criteria for deciding to stop the approximation
	# or to continue.

	# if either control vector is larger than the base vector continue
	if abs(C1) > abs(B) or abs(C2) > abs(B):
		return FlattenPath(P0, P4, P7, P9) + FlattenPath(P9, P8, P6, P3)

	# otherwise if the base is smaller than half the fault tolerance stop.
	elif abs(B) < EPS / 2:
		return (P9, P3)
	else:

		# if neither of the above applies, check for the following conditions.
		# if one of them is true continue the approximation otherwise stop
		#
		# The first constrol vector goes too far before the base
		# The seconde control vector goes too far behind the base
		# Both control vectors lie on either side of the base.
		# The midpoint is too far from base.

		N=B.normalized()
		if ((C1 * N) < -EPS or (C2 * N) > EPS or cr(C1,B)*cr(C2,B) < 0
			or abs(cr(N,S)) > EPS):
			return FlattenPath(P0, P4, P7, P9) + FlattenPath(P9, P8, P6, P3)
		else:
			return (P9, P3)


class PLTSaver:

	def __init__(self, file, pathname, options=None):
		self.file=file
		self.pathname=pathname
		if options is None:
			options=plt_options
		else:
			self.options=options


	def write_headers(self):
		self.file.write(self.options['first_command']+self.options['command_terminator'])

	def write_terminator(self):
		self.file.write(self.options['final_command']+self.options['command_terminator'])

	def putpolyrec(self, seq):
		self.file.write(self.options['move_command']+str(seq[0])+','+str(seq[1])+self.options['command_terminator'])
		l=len(seq)
		i=2
		while i < l:
			self.file.write(self.options['draw_command']+str(seq[i])+','+str(seq[i+1])+self.options['command_terminator'])
			i=2 + i

	def PathToSeq(self, Path):
		parlst=()
		for i in range(Path.len):
			type, control, p, cont=Path.Segment(i)
			if type==Bezier:
				p1, p2=control
				tmplst=FlattenPath(p0, p1, p2, p)
				for tp in tmplst:
					parlst=parlst + tuple(self.trafo(tp))
			else:
				parlst=parlst + tuple(self.trafo(p))
			p0=p
		return parlst

	def PolyBezier(self, Paths, Properties):
		line_pattern=Properties.line_pattern
		path=Paths[0]
		if line_pattern is EmptyPattern and self.options['remove_empty_lines']=='yes':
##			print 'line_pattern is EmptyPattern'
			pass
		else:
##			print 'line_pattern is NOT EmptyPattern'
			for path in Paths:
				lst=self.PathToSeq(path)
				self.putpolyrec(map(rndtoint , lst))

	def close(self):
		self.file.close()

	def SaveObjects(self, Objects):
		for object in Objects:
			if object.is_Compound:
				self.SaveObjects(object.GetObjects())
			elif object.is_Bezier or object.is_Rectangle or object.is_Ellipse or \
					object.is_Text:
				self.PolyBezier(object.Paths(), object.Properties())

	def SaveLayers(self, Layers):
		for layer in Layers:
			if not layer.is_SpecialLayer and layer.Printable():
				self.SaveObjects(layer.GetObjects())

	def SaveDocument(self, doc):
		left, bottom, right, top=doc.PageRect()
		width=right - left
		height=top - bottom
		inch=int(self.options['per_inch'])
		sc=inch / 72.0
##		self.trafo=Trafo(sc, 0, 0, -sc, - sc * left, sc * top)
		if self.options['rotation']=='yes':
			self.trafo=Trafo(cos(90*degrees), sin(90*degrees), -sin(90*degrees), cos(90*degrees), 0, bottom*sc)
		else:
			self.trafo=Trafo(sc, 0, 0, sc, 0, bottom*sc)
		self.Scale=sc
		self.inch=inch
		self.extend=map(rndtoint, tuple(self.trafo(left,bottom))
									+ tuple(self.trafo(right,top)))

		# Header
		self.write_headers()
		self.SaveLayers(doc.Layers())
		self.write_terminator()
		#end

def save(document, file, filename, options={}):
	saver=PLTSaver(file, filename, options)
	saver.SaveDocument(document)
	saver.close()
	
######## END PLS



from xml.sax import make_parser, handler



class CutterOptions:

	def __init__(self):
		self.options={}
		self.options.update(plt_options)

	def load(self, filename=None):
		
		class FancyCounter(handler.ContentHandler):
		
			def __init__(self, options):
				
				self._options=options
				self._parent=None
				self._text=''
				
			def startElement(self, name, attrs):
				if name=='preferences':
					self._parent=name
				self._text=''
			
			def characters(self, content):
				self._text=self._text + content
			
			def endElement(self, name):
				if name=='preferences':
					if self._parent=='preferences':
						self._parent==None
				else:
					if self._parent=='preferences':
						self._options[name]=self._text.encode('utf-8')

		
		parser=make_parser()
		
		# Create the handler
		dh=FancyCounter(self.options)
		
		# Tell the parser to use our handler
		parser.setContentHandler(dh)
		
		# Parse the input
		try:
			parser.parse(filename)
		except (IOError, os.error), value:
			return


	def save(self, filename=None):
		
		if len(self.options)==0 or filename==None:
			return
		from xml.sax.saxutils import XMLGenerator
		
		try:
			file=open(filename, 'w')
		except (IOError, os.error), value:
			import sys
			sys.stderr(_('cannot write preferences into %s: %s'% (`filename`, value[1])))
			return
		
		writer=XMLGenerator(out=file,encoding='utf-8')
		writer.startDocument()
		defaults=plt_options
		items=self.options.items()

		writer.startElement('preferences',{})
		writer.characters('\n')
		for key, value in items:
			if defaults.has_key(key) and defaults[key]==value:
				continue
			writer.characters('	')
			writer.startElement('%s' % key,{})
			writer.characters('%s' % unicode(value,'utf-8'))
			writer.endElement('%s' % key)
			writer.characters('\n')
		writer.endElement('preferences')
		writer.endDocument()
		file.close




class CreateCutterDlg(ModalDialog):
	def __init__(self, master, context, dlgname='__dialog__'):
		self.master=master
		self.context=context
		self.title=_("sK1 Cutter ver.%s")%__version__
		ModalDialog.__init__(self, master, name=dlgname)
		
	
	def build_dlg(self):
		self.root=TFrame(self.top, style='FlatFrame', borderwidth=5)
		self.root.pack(side=TOP, fill=BOTH, expand=1)
		
		panel=TFrame(self.root, style='FlatFrame', borderwidth=5)		
		panel.pack(side=TOP, fill=X)
		
		self.nb=TNotebook(self.root, height=250, width=550, padding=5)
		self.nb.pack(side=TOP, fill=BOTH, expand=1)
		
		# vars
		self.var_activepage=StringVar(self.root)
		self.var_rotation=StringVar(self.root)
		self.var_rotation.set('no')
		self.var_mirror=StringVar(self.root)
		self.var_mirror.set('no')
		self.var_remove_empty_lines=StringVar(self.root)
		self.var_remove_empty_lines.set('yes')
		self.var_origin_check=StringVar(self.root)
		self.var_origin_check.set('no')
		
		self.var_name=StringVar(panel)
		self.var_max_steps_across=StringVar(panel)
		self.var_max_steps_down=StringVar(panel)
		self.var_per_inch=StringVar(panel)
		self.var_first_command=StringVar(panel)
		self.var_final_command=StringVar(panel)
		self.var_move_command=StringVar(panel)
		self.var_draw_command=StringVar(panel)
		self.var_XY_separator=StringVar(panel)
		self.var_coordinate_separator=StringVar(panel)
		self.var_command_terminator=StringVar(panel)
		self.var_page_feed_command=StringVar(panel)
		self.var_page_terminator_command=StringVar(panel)
		self.var_output=StringVar(panel)
		self.init_setup()
		
		# build_tab
		self.build_tab_general()
		self.build_tab_setup()
		
		ok=TButton(self.root, text=_("Cut!"), command=self.ok)
		ok.pack(side=RIGHT, padx=5,pady=5)
		
		self.focus_widget=ok
		
		cancel=TButton(self.root, text=_("Cancel"), command=self.cancel)
		cancel.pack(side=RIGHT, padx=5,pady=5)
		
		self.top.bind('<Escape>', self.cancel)
		self.top.protocol('WM_DELETE_WINDOW', self.cancel)
	
	def build_tab_general(self):
		panel=TFrame(self.root, style='FlatFrame', borderwidth=10)
		self.nb.add(panel, text=_("General"))
		
		frame=TFrame(panel, style='FlatFrame', borderwidth=0)
		frame.pack(side=TOP, fill=BOTH)
		
		label=TLabel(frame, style='FlatLabel', text=_("Name "))
		label.pack(side=LEFT)
		
		entry=TEntryExt(frame, state='readonly', textvariable=self.var_name,width=50)
		entry.pack(side=LEFT)
		b=TButton(frame, image="toolbar_open",style='Toolbutton',command=self.LoadOptions)
		b.pack(side=LEFT)
		
		label=TLabel(panel, style='FlatLabel', text="")
		label.pack(side=TOP)
		
		active_page=self.context.document.active_page + 1
		self.var_activepage.set(_("Current page: %g") % active_page)
		label=TLabel(panel, style='FlatLabel', text=self.var_activepage.get())
		label.pack(side=LEFT)
		
		rel_frame=TLabelframe(panel, labelwidget=label, style='Labelframe', borderwidth=4)
		rel_frame.pack(side=LEFT, padx=5, pady=2, anchor=N)
		
		remove_empty_lines_check=TCheckbutton(rel_frame, text=_("Remove empty style lines"), onvalue='yes', offvalue='no', 
										variable=self.var_remove_empty_lines, command=self.SetRotation)
		remove_empty_lines_check.pack(side=TOP, anchor=W)
		
		origin_check=TCheckbutton(rel_frame, text=_("Plotter origin page center"), onvalue='yes', offvalue='no', 
										variable=self.var_origin_check, command=self.SetRotation)
		origin_check.pack(side=TOP, anchor=W)
		
		rotation_check=TCheckbutton(rel_frame, text=_("Rotation 90°"), onvalue='yes', offvalue='no', 
										variable=self.var_rotation, command=self.SetRotation)
		rotation_check.pack(side=TOP, anchor=W)
		
		mirror_check=TCheckbutton(rel_frame, text=_("Mirror"), onvalue='yes', offvalue='no', 
										variable=self.var_mirror, command=self.SetRotation)
		mirror_check.pack(side=TOP, anchor=W)
		
		frame=TFrame(panel, style='FlatFrame', borderwidth=0)
		frame.pack(side=TOP, fill=X)
		
		self.image_cutter=TLabel(frame, style='FlatLabel', image='cutter')
		self.image_cutter.pack(side=TOP, anchor='center')
		
	
	def build_tab_setup(self):	
		panel=TFrame(self.root, style='FlatFrame', borderwidth=10)
		self.nb.add(panel, text=_("Setup"))
		
		frame=TFrame(panel, style='FlatFrame', borderwidth=0)
		frame.pack(side=TOP, fill=BOTH)
		
		label=TLabel(frame, style='FlatLabel', text=_("Name "))
		label.pack(side=LEFT)
		
		entry=TEntryExt(frame, textvariable=self.var_name,width=50)
		entry.pack(side=LEFT)
		
		b=TButton(frame, image="toolbar_open",style='Toolbutton',command=self.LoadOptions)
		b.pack(side=LEFT)
		b=TButton(frame, image="toolbar_saveas",style='Toolbutton',command=self.SaveOptions)
		b.pack(side=LEFT)
		
		label=TLabel(panel, style='FlatLabel', text="")
		label.pack(side=TOP)
		
		frame=TFrame(panel, style='FlatFrame', borderwidth=0)
		frame.pack(side=TOP, fill=X)
		
		# 1
		label=TLabel(frame, style='FlatLabel', text=_("Maximum steps across page "))
		label.grid(row=1, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_max_steps_across,width=10)
		entry.grid(row=1, column=1, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Maximum steps down page "))
		label.grid(row=2, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_max_steps_down,width=10)
		entry.grid(row=2, column=1, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Steps per inch "))
		label.grid(row=3, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_per_inch,width=10)
		entry.grid(row=3, column=1, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("First command to plotter "))
		label.grid(row=4, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_first_command,width=10)
		entry.grid(row=4, column=1, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Final command to plotter "))
		label.grid(row=5, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_final_command,width=10)
		entry.grid(row=5, column=1, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Move command "))
		label.grid(row=6, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_move_command,width=10)
		entry.grid(row=6, column=1, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Draw command "))
		label.grid(row=7, column=0, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_draw_command,width=10)
		entry.grid(row=7, column=1, sticky='ew')
		
		# 2
		
		label=TLabel(frame, style='FlatLabel', text='    ')
		label.grid(row=1, column=3, sticky='ew')
		
		# 3
		label=TLabel(frame, style='FlatLabel', text=_("X Y separator "))
		label.grid(row=1, column=4, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_XY_separator,width=10)
		entry.grid(row=1, column=5, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Coordinate separator "))
		label.grid(row=2, column=4, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_coordinate_separator,width=10)
		entry.grid(row=2, column=5, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Command terminator "))
		label.grid(row=3, column=4, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_command_terminator,width=10)
		entry.grid(row=3, column=5, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Page feed command "))
		label.grid(row=4, column=4, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_page_feed_command,width=10)
		entry.grid(row=4, column=5, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Page terminator "))
		label.grid(row=5, column=4, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_page_terminator_command,width=10)
		entry.grid(row=5, column=5, sticky='ew')
		
		label=TLabel(frame, style='FlatLabel', text=_("Output "))
		label.grid(row=6, column=4, sticky='ew')
		entry=TEntryExt(frame, textvariable=self.var_output,width=10)
		entry.grid(row=6, column=5, sticky='ew')
		
		
###############################################################################

################### def SetRotation(self):
	def SetRotation(self):
		if self.var_rotation.get()=='no':
			if self.var_mirror.get()=='no':
				self.image_cutter['image']='cutter'
			else:
				self.image_cutter['image']='cutterM'
		else:
			if self.var_mirror.get()=='no':
				self.image_cutter['image']='cutterR'
			else:
				self.image_cutter['image']='cutterMR'

	def SaveOptions(self,filename=''):
		if not filename:
			filename=self.var_name.get()+EXT_FILE_OPTIONS
			directory=app.config.user_plugins
			if not directory:
				directory=os_utils.gethome()
			
			from app.managers.dialogmanager import DialogManager
			dialogman=DialogManager(self.root)
			filename, sysfilename=dialogman.getGenericSaveFilename(_("Save Cutter Options File"), 
										cutter_options_types, initialdir=directory, initialfile=filename)
		
		if not filename:
			return
		
		self.Cutter.options['name']=self.var_name.get()
		self.Cutter.options['output']=self.var_output.get()
		self.Cutter.options['max_steps_across']=self.var_max_steps_across.get()
		self.Cutter.options['max_steps_down']=self.var_max_steps_down.get()
		self.Cutter.options['per_inch']=self.var_per_inch.get()
		self.Cutter.options['first_command']=self.var_first_command.get()
		self.Cutter.options['final_command']=self.var_final_command.get()
		self.Cutter.options['move_command']=self.var_move_command.get()
		self.Cutter.options['draw_command']=self.var_draw_command.get()
		self.Cutter.options['XY_separator']=self.var_XY_separator.get()
		self.Cutter.options['coordinate_separator']=self.var_coordinate_separator.get()
		self.Cutter.options['command_terminator']=self.var_command_terminator.get()
		self.Cutter.options['page_feed_command']=self.var_page_feed_command.get()
		self.Cutter.options['page_terminator_command']=self.var_page_terminator_command.get()
		
		self.Cutter.save(filename)

	def LoadOptions(self, filename=None):
		if not filename:
			directory=app.config.user_plugins
			if not directory:
				directory=os_utils.gethome()
			from app.managers.dialogmanager import DialogManager
			dialogman=DialogManager(self.root)
			filename, sysfilename=dialogman.getGenericOpenFilename(_("Load Cutter Options File"), 
										cutter_options_types, initialdir=directory, initialfile=filename)
		
		if not filename:
			return
		
		self.Cutter.load(filename)
		
		self.var_name.set(self.Cutter.options['name'])
		self.var_output.set(self.Cutter.options['output'])
		self.var_max_steps_across.set(self.Cutter.options['max_steps_across'])
		self.var_max_steps_down.set(self.Cutter.options['max_steps_down'])
		self.var_per_inch.set(self.Cutter.options['per_inch'])
		self.var_first_command.set(self.Cutter.options['first_command'])
		self.var_final_command.set(self.Cutter.options['final_command'])
		self.var_move_command.set(self.Cutter.options['move_command'])
		self.var_draw_command.set(self.Cutter.options['draw_command'])
		self.var_XY_separator.set(self.Cutter.options['XY_separator'])
		self.var_coordinate_separator.set(self.Cutter.options['coordinate_separator'])
		self.var_command_terminator.set(self.Cutter.options['command_terminator'])
		self.var_page_feed_command.set(self.Cutter.options['page_feed_command'])
		self.var_page_terminator_command.set(self.Cutter.options['page_terminator_command'])

	def ok(self, *arg):
		self.SaveOptions(os.path.join(app.config.user_plugins, NAME_FILE_OPTIONS+EXT_FILE_OPTIONS ))
		if not self.Cutter.options['output']:
			filename=self.context.document.meta.filename+EXT_OUTPUT_FILE
			directory=os_utils.gethome()
			from app.managers.dialogmanager import DialogManager
			dialogman=DialogManager(self.root)
			self.Cutter.options['output'], sysfilename=dialogman.getGenericSaveFilename(_("Save Cutter File"), 
										cutter_types, initialdir=directory, initialfile=filename)
		if self.Cutter.options['output']:
			command={
					'rotation' : 			self.var_rotation.get(),
					'mirror' : 				self.var_mirror.get(),
					'remove_empty_lines' : 	self.var_remove_empty_lines.get(),
					'origin' : 				self.var_origin_check.get()
					}
			self.Cutter.options.update(command)
			print self.Cutter.options
			self.close_dlg(self.Cutter.options)

	def cancel(self, *arg):
		self.close_dlg(None)

	def init_setup(self):
		# Load options cuttet
		self.Cutter=CutterOptions()
		self.LoadOptions(os.path.join(app.config.user_plugins, NAME_FILE_OPTIONS + EXT_FILE_OPTIONS))





###############################################################################

def create_cutter(context):
	# Instantiate the modal dialog...
	root=context.application.root
	dlg=CreateCutterDlg(root,context)
	# ... and run it.
	result=dlg.RunDialog()
	if result is not None:
		filename=result['output']
		try:
			file=open(filename, 'w')
		except (IOError, os.error), value:
			import sys
			sys.stderr(_('cannot write into %s: %s'% (`filename`, value[1])))
			return

		save(context.document,file,filename,result)



app.Scripting.AddFunction('create_cutter', _("CUTTER..."),
								create_cutter,
								script_type=app.Scripting.AdvancedScript)

