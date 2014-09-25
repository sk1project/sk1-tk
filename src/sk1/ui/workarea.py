
import wal

class SK1_WorkArea(wal.VBox):

	def __init__(self, master):
		wal.VBox.__init__(self, master)

		self.pack(wal.HLine(self))

		ctx = wal.HBox(self, height=35)
		self.pack(ctx, False, False)

		self.pack(wal.HLine(self))

		hbox = wal.HBox(self, bg='red')
		self.pack(hbox, True, True)

		tools = wal.VBox(hbox, width=35, bg='blue')
		hbox.pack(tools, False, False)

		pal = wal.VBox(hbox, width=20, bg='green')
		hbox.pack(pal, False, False, end=True)

		self.pack(wal.HLine(self))

		self.stbar = SK1_StatusBar(self)
		self.pack(self.stbar, False, False, end=True)

class SK1_StatusBar(wal.HBox):

	def __init__(self, master):
		wal.HBox.__init__(self, master, height=25)