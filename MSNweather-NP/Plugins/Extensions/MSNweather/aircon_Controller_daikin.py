# -*- coding: utf-8 -*-
#######################################################################
#
#    Plugin for Enigma2
#    Coded by j00zek (c)2020
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem konwertera
#    Please respect my work and don't delete/change name of the converter author
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#     
#######################################################################
 
from __init__ import _

from Components.ActionMap import ActionMap
from Components.config import config
from Components.j00zekAccellPixmap import j00zekAccellPixmap
from Components.j00zekModHex2strColor import Hex2strColor, clr
#from Components.Pixmap import Pixmap
from Components.Label import Label
#from Components.Sources.StaticText import StaticText
from enigma import eTimer
from Screens.Screen import Screen

from daikin_aircon import *

import os

######################################################################################################
class DaikinController(Screen):
    def __init__(self, session, AC_IP, AC_PORT, AC_info):
        self.skin = open("/usr/lib/enigma2/python/Plugins/Extensions/MSNweather/aircon_data/aircon_Controller_daikin.xml", "r").read()
        Screen.__init__(self, session )
        
        self.AC_ADDR = '.'.join((str(i) for i in AC_IP))
        if AC_PORT != 80:
          self.AC_ADDR += ':%s' % AC_PORT
        self.AC_info = AC_info
        self.AC = Aircon(self.AC_ADDR)
        
        # Top info
        self["ac_config_info"] = Label("%s%s%s (%s)" % (clr['G'], self.AC_info, clr['Gray'], self.AC_ADDR))
        self["ac_name"] = Label("")
        #middle part
        self["indoor_temp"] = Label("?")
        self["outdoor_temp"] = Label("?")
        self["on_off_icon"] = j00zekAccellPixmap()
        # Bottom Buttons
        self["key_red"] = Label(_("Fan"))
        self["key_green"] = Label("")
        self["key_yellow"] = Label(_("Direction"))
        self["key_blue"] = Label(_("Mode"))

        # Define Actions
        self["actions"] = ActionMap(["MSNweatherNPacControllers"],
            {
                "keyCancel": self.keyCancel,
                "keyRed": self.keyCancel,
                "keyOk": self.keySave,
                "keyGreen": self.keyGreen,
            }
        )
        self.InitTimer = eTimer()
        self.InitTimer.callback.append(self.getACstate)
        self.onShow.append(self._onShow)

    def _onShow(self):
        self.setTitle(_("Daikin A/C controller"))
        self.InitTimer.start(1000, True)
        
    def getACstate(self):
        self.InitTimer.stop()
        self["ac_name"].setText( _("%sName:%s %s") % (clr['G'], clr['Gray'], str(self.AC.get_name()) ) )
        self["indoor_temp"].setText(str(self.AC.get_indoor_temp()))
        self["outdoor_temp"].setText(str(self.AC.get_outdoor_temp()))
        
        self.POWER = self.AC.get_power()
        if self.POWER:
            self["key_green"].setText(_("Turn off"))
            self.updateICON("on_off_icon", "on_60x60.png")
        else:
            self["key_green"].setText(_("Turn on"))
            self.updateICON("on_off_icon", "off_60x60.png")
    
    def updateICON(self, iconName, fileName):
        #self["on_off_icon"].hide()
        self[iconName].updateIcon("/usr/lib/enigma2/python/Plugins/Extensions/MSNweather/aircon_data/%s" % fileName)
        self[iconName].show()

    def keyCancel(self):
        self.close()
      
    def keySave(self):
        self.close()

    def keyGreen(self):
        self.AC.set_power(True)
        self.getACstate()
      
        