

import wal

class SK1_ToolBar(wal.HBox):

	def __init__(self, master):
		wal.HBox.__init__(self, master, height=35)

		self.master.pack(self)
		self.master.pack(wal.HLine(self.master))