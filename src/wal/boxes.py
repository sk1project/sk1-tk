import Tkinter

class Frame(Tkinter.Frame):

	def __init__(self, master, cnf={}, **kw):
		Tkinter.Frame.__init__(self, master=master, cnf=cnf, **kw)

class HLine(Tkinter.Frame):

	def __init__(self, master):
		self.master = master
		Tkinter.Frame.__init__(self, master=master, height=2)
		self.config(relief=Tkinter.SUNKEN)
		self.config(border=1)

	def pack(self, cnf={}, **kw):
		kw['expand'] = False
		kw['fill'] = Tkinter.X
		Tkinter.Frame.pack(self, cnf=cnf, **kw)

class VLine(Tkinter.Frame):

	def __init__(self, master):
		self.master = master
		Tkinter.Frame.__init__(self, master=master, width=2)
		self.config(relief=Tkinter.SUNKEN)
		self.config(border=1)

	def pack(self, cnf={}, **kw):
		kw['expand'] = False
		kw['fill'] = Tkinter.Y
		Tkinter.Frame.pack(self, cnf=cnf, **kw)


class VBox(Tkinter.Frame):

	def __init__(self, master, cnf={}, **kw):
		self.master = master
		Tkinter.Frame.__init__(self, master=master, cnf=cnf, **kw)

	def pack(self, child=None, expand=False, fill=False,
			padding=0, end=False, cnf={}, **kw):
		if child:
			side = Tkinter.TOP
			anchor = Tkinter.N
			if end:
				side = Tkinter.BOTTOM
				anchor = Tkinter.S
			if not fill: fill = Tkinter.NONE
			else: fill = Tkinter.X
			if expand:fill = Tkinter.BOTH
			child.pack(anchor=anchor, side=side,
					expand=expand, pady=padding, fill=fill)
		else:
			kw['expand'] = expand
			kw['fill'] = Tkinter.Y
			if expand:kw['fill'] = Tkinter.BOTH
			Tkinter.Frame.pack(self, cnf=cnf, **kw)

class HBox(Tkinter.Frame):

	def __init__(self, master, cnf={}, **kw):
		self.master = master
		Tkinter.Frame.__init__(self, master=master, cnf=cnf, **kw)

	def pack(self, child=None, expand=False, fill=False,
			padding=0, end=False, cnf={}, **kw):
		if child:
			side = Tkinter.LEFT
			anchor = Tkinter.W
			if end:
				side = Tkinter.RIGHT
				anchor = Tkinter.E
			if not fill: fill = Tkinter.NONE
			else: fill = Tkinter.Y
			if expand:fill = Tkinter.BOTH
			child.pack(anchor=anchor, side=side,
					expand=expand, pady=padding, fill=fill)
		else:
			kw['expand'] = expand
			kw['fill'] = Tkinter.X
			if expand:kw['fill'] = Tkinter.BOTH
			Tkinter.Frame.pack(self, cnf=cnf, **kw)
