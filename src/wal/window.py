
import sys
import Tkinter

class MainWindow(Tkinter.Toplevel):

	actions = {}

	def __init__(self, action_entries=[], horizontal=False):
		self.horizontal = horizontal
		self.root = Tkinter.Tk()
		self.root.withdraw()
		Tkinter.Toplevel.__init__(self)
		self.create_actions(action_entries)
		self.build()
		self.protocol("WM_DELETE_WINDOW", self.destroy)

	def run(self):
		self.update()
		self.mainloop()

	def build(self):pass

	def destroy(self, *args):
		print "event"
		self.exit()

	def exit(self):
		self.withdraw()
		self.quit()
		sys.exit()

	def pack(self, child, expand=False, fill=False, padding=0, end=False):
		if self.horizontal:
			if end:
				side = Tkinter.RIGHT
				anchor = Tkinter.E
			else:
				side = Tkinter.LEFT
				anchor = Tkinter.W
			if fill:
				fill = Tkinter.Y
			else:
				fill = Tkinter.NONE
			if expand:
				expand = expand
				fill = Tkinter.BOTH
				anchor = Tkinter.CENTER
			child.pack(anchor=anchor, side=side,
					expand=expand, pady=padding, fill=fill)
		else:
			if end:
				side = Tkinter.BOTTOM
				anchor = Tkinter.S
			else:
				side = Tkinter.TOP
				anchor = Tkinter.N
			if fill:
				fill = Tkinter.X
			else:
				fill = Tkinter.NONE
			if expand:
				expand = expand
				fill = Tkinter.BOTH
				anchor = Tkinter.CENTER
			child.pack(anchor=anchor, side=side,
					expand=expand, pady=padding, fill=fill)

	def center(self):
		w = self.winfo_screenwidth()
		h = self.winfo_screenheight()
		rootsize = self.get_size()
		x = w / 2 - rootsize[0] / 2
		y = h / 2 - rootsize[1] / 2
		geometry = "%dx%d+%d+%d" % (rootsize + (x, y))
		self.geometry(geometry)

	def set_title(self, title): self.title(title)

	def set_size(self, w, h):
		geometry = '{}x{}'.format(w, h)
		self.geometry(geometry)
		self.update()

	def get_size(self):
		return (self.winfo_width(), self.winfo_height())

	def set_min_size(self, w, h): self.minsize(w, h)
	def maximize(self): self.attributes('-zoomed', True)
	def is_maximized(self):return self.attributes('-zoomed')

	#TODO: implement win icon
	def set_icon(self, icon):pass

	def create_actions(self, entries):pass
