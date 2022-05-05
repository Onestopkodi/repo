# -*- coding: utf-8 -*-
from threading import Thread
from modules import service_functions
from modules.settings_reader import make_settings_dict, get_setting
from modules.kodi_utils import set_property, clear_property, sleep, xbmc_monitor, logger

class FenMonitor(xbmc_monitor):
	def __init__ (self):
		xbmc_monitor.__init__(self)
		logger('FEN', 'Main Monitor Service Starting')
		logger('FEN', 'Settings Monitor Service Starting')
		self.startUpServices()
	
	def startUpServices(self):
		threads = []
		functions = (service_functions.DatabaseMaintenance().run, service_functions.TraktMonitor().run)
		for item in functions: threads.append(Thread(target=item))
		while not self.abortRequested():
			try: service_functions.InitializeDatabases().run()
			except: pass
			try: service_functions.CheckSettingsFile().run()
			except: pass
			try: service_functions.SyncMyAccounts().run()
			except: pass
			[i.start() for i in threads]
			try: service_functions.ClearSubs().run()
			except: pass
			try: service_functions.ViewsSetWindowProperties().run()
			except: pass
			try: service_functions.AutoRun().run()
			except: pass
			try: service_functions.ReuseLanguageInvokerCheck().run()
			except: pass
			break

	def onScreensaverActivated(self):
		set_property('fen_pause_services', 'true')

	def onScreensaverDeactivated(self):
		clear_property('fen_pause_services')

	def onSettingsChanged(self):
		clear_property('fen_settings')
		sleep(50)
		make_settings_dict()
		set_property('fen_kodi_menu_cache', get_setting('kodi_menu_cache'))

	def onNotification(self, sender, method, data):
		if method == 'System.OnSleep': set_property('fen_pause_services', 'true')
		elif method == 'System.OnWake': clear_property('fen_pause_services')


FenMonitor().waitForAbort()

logger('FEN', 'Settings Monitor Service Finished')
logger('FEN', 'Main Monitor Service Finished')