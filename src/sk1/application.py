
from uc2.application import UCApplication

from sk1 import config
from sk1.ui.mainwindow import SK1_MainWindow


class SK1_Application(UCApplication):

	appdata = None
	mw = None

	def __init__(self, appdata):
		UCApplication.__init__(self)
		self.appdata = appdata

		self.mw = SK1_MainWindow(self)

	def run(self):
		self.mw.run()

	def exit_request(self):
		self.update_config()
		return True

	def update_config(self):
		config.resource_dir = ''
		if config.mw_keep_maximized:return
		if config.mw_store_size:
			if not self.mw.is_maximized():
				config.mw_size = self.mw.get_size()
			config.mw_maximized = self.mw.is_maximized()
		config.save(self.appdata.app_config)
