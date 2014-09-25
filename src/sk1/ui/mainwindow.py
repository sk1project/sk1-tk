
import wal

from sk1 import config

class SK1_MainWindow(wal.MainWindow):

	def __init__(self, app):
		self.app = app
		wal.MainWindow.__init__(self)

	def build(self):

		self.menubar = SK1_MenuBar(self)
		self.pack(self.menubar)

		self.pack(wal.HLine(self))

		self.toolbar = SK1_ToolBar(self)
		self.pack(self.toolbar)

		self.workarea = SK1_WorkArea(self)
		self.pack(self.workarea, True, True)

		self.set_win_title()
		self.set_min_size(*config.mw_min_size)
		if config.mw_store_size: self.set_size(*config.mw_size)

#		self.set_icon_from_file(rc.get_image_path(rc.IMG_APP_ICON))
		self.center()

		if config.mw_maximized: self.maximize()

	def destroy(self, *args):
		if self.app.exit_request(): self.exit()
		return False

	def set_win_title(self, docname=''):
		if docname:
			title = '[%s] - %s' % (docname, self.app.appdata.app_name)
			self.set_title(title)
		else:
			self.set_title(self.app.appdata.app_name)

class SK1_MenuBar(wal.HBox):

	def __init__(self, master):
		wal.HBox.__init__(self, master, height=20)

class SK1_ToolBar(wal.HBox):

	def __init__(self, master):
		wal.HBox.__init__(self, master, height=35)

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
		wal.HBox.__init__(self, master, height=15)
