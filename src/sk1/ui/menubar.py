
import wal


class SK1_MenuBar(wal.HBox):

	def __init__(self, master):
		wal.HBox.__init__(self, master, height=20)

		self.master.pack(self)
		self.master.pack(wal.HLine(self.master))
