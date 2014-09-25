
import wal

from sk1 import config
from sk1.ui.menubar import SK1_MenuBar
from sk1.ui.toolbar import SK1_ToolBar
from sk1.ui.workarea import SK1_WorkArea

class SK1_MainWindow(wal.MainWindow):

	def __init__(self, app):
		self.app = app
		wal.MainWindow.__init__(self)

	def build(self):

		self.menubar = SK1_MenuBar(self)
		self.toolbar = SK1_ToolBar(self)

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

