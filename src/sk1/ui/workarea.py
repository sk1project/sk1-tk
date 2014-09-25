
import wal

class SK1_WorkArea(wal.VBox):

	def __init__(self, master):
		wal.VBox.__init__(self, master)

		ctx = wal.HBox(self, height=35)
		self.pack(ctx, False, False)

		self.pack(wal.HLine(self))

		#----

		hbox = wal.HBox(self)
		self.pack(hbox, True, True)

		tools = wal.VBox(hbox, width=35)
		hbox.pack(tools, False, False)

		hbox.pack(wal.VLine(hbox))

		pal = wal.VBox(hbox, width=20)
		hbox.pack(pal, False, False, end=True)

		hbox.pack(wal.VLine(hbox), end=True)
		#---

		self.pack(wal.HLine(self))

		self.stbar = SK1_StatusBar(self)
		self.pack(self.stbar, False, False, end=True)

class SK1_StatusBar(wal.HBox):

	def __init__(self, master):
		wal.HBox.__init__(self, master, height=25)
