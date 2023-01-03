#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc, xbmcgui


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.cosmic.mod"}}')
xbmc.executebuiltin('SendClick(11)')
xbmc.sleep(500)
xbmc.executebuiltin( 'ActivateWindow(Home)' )
