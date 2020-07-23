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
        self["back_wheel"] = j00zekAccellPixmap()
        self["back_plus_minus"] = j00zekAccellPixmap()
        self["set_temp"] = Label("?")
        self["auto_icon"] = j00zekAccellPixmap()
        self["cool_icon"] = j00zekAccellPixmap()
        self["heat_icon"] = j00zekAccellPixmap()
        self["fan_icon"] = j00zekAccellPixmap()
        self["dry_icon"] = j00zekAccellPixmap()
        #bottom part
        self["fan_speed_icon"] = j00zekAccellPixmap()
        self["fan_dir_icon"] = j00zekAccellPixmap()
        # Bottom Buttons
        self["key_red"] = Label(_("Fan"))
        self["key_green"] = Label("")
        self["key_yellow"] = Label(_("Direction"))
        self["key_blue"] = Label(_("Mode"))

        # Define Actions
        self["actions"] = ActionMap(["MSNweatherNPacControllers"],
            {
                "keyCancel": self.keyCancel,
                "keyOk":     self.keySave,
                "keyRed":    self.keyRed,
                "keyGreen":  self.keyGreen,
                "keyYellow": self.keyYellow,
                "keyBlue":   self.keyBlue,
                "keyLeft":   self.keyLeft,
                "keyRight":  self.keyRight,
            }
        )
        
        self.AC_MODES = {1: {'IconName': 'auto_icon', 'Name': 'Auto',       'IconOn': 'op_auto_slct_eu.png', 'IconOff': 'op_auto_eu.png', 'BackImg': 'co_back_auto.png'},
                         3: {'IconName': 'cool_icon', 'Name': 'Chłodzenie', 'IconOn': 'op_cool_slct_eu.png', 'IconOff': 'op_cool_eu.png', 'BackImg': 'co_back_cool.png'},
                         4: {'IconName': 'heat_icon' , 'Name': 'Ogrzewanie', 'IconOn': 'op_heat_slct_eu.png', 'IconOff': 'op_heat_eu.png', 'BackImg': 'co_back_heat.png'},
                         6: {'IconName': 'fan_icon' , 'Name': 'Wentylator', 'IconOn': 'op_fan_slct_eu.png',  'IconOff': 'op_fan_eu.png',  'BackImg': 'co_back_fan.png'},
                         2: {'IconName': 'dry_icon', 'Name': 'Osuszanie',  'IconOn': 'op_dry_slct_eu.png',  'IconOff': 'op_dry_eu.png',  'BackImg': 'co_back_dry.png'},
                        }
        self.AC_FANRATES = { 'A': 'op_btm_fanspeed_auto_eu.png',
                             'B': 'op_btm_fanspeed_silent_eu.png',
                             '3': 'op_btm_fanspeed_5_lv1_eu.png',
                             '4': 'op_btm_fanspeed_5_lv2_eu.png',
                             '5': 'op_btm_fanspeed_5_lv3_eu.png',
                             '6': 'op_btm_fanspeed_5_lv4_eu.png',
                             '7': 'op_btm_fanspeed_5_lv5_eu.png',
                            }
        
        self.InitTimer = eTimer()
        self.InitTimer.callback.append(self.getACstate)
        self.onShow.append(self._onShow)

    def _onShow(self):
        self.setTitle(_("Daikin A/C controller"))
        self.InitTimer.start(500, True)
        
    def getACstate(self):
        self.InitTimer.stop()
        sensor_info = self.AC.get_sensor_info()
        control_info = self.AC.get_control_info()

        self["ac_name"].setText( _("%sName:%s %s") % (clr['G'], clr['Gray'], str(self.AC.get_name()) ) )
        
        self["indoor_temp"].setText("%s°C" % int(sensor_info['htemp']))
        self["outdoor_temp"].setText("%s°C" % int(sensor_info['otemp']))
        
        self.AC_POWER        = control_info['pow']
        try:
            self.AC_SETTEMP  = int(control_info['stemp'])
        except Exception:
            self.AC_SETTEMP  = 0
        self.AC_MODE         = control_info['mode']
        self.AC_FANRATE      = str(control_info['f_rate'])
        self.AC_FANDIRECTION = str(control_info['f_dir'])
        
        if self.AC_SETTEMP == 0:
            self["set_temp"].setText(" ")
        else:
            self["set_temp"].setText("%s°C" % self.AC_SETTEMP)
        self.updateICON("fan_dir_icon", "op_btm_drction_ul_off_eu.png")
        
        if self.AC_POWER:
            self["key_green"].setText(_("Turn off"))
            self.updateICON("on_off_icon", "on_60x60.png")
            self.updateICON("back_wheel",  self.AC_MODES[self.AC_MODE]['BackImg'])
        else:
            self["key_green"].setText(_("Turn on"))
            self.updateICON("on_off_icon", "off_60x60.png")
            self.updateICON("back_wheel",  "co_back_off.png")
            #self.updateICON("fan_speed_icon",  "op_btm_fanspeed_off_eu.png")
        
        #off all
        for key, value in self.AC_MODES.items():
            self.updateICON(value['IconName'], value['IconOff'])
        #on the one
        self.updateICON(self.AC_MODES[self.AC_MODE]['IconName'], self.AC_MODES[self.AC_MODE]['IconOn'])
        
        self.updateICON("fan_speed_icon", self.AC_FANRATES[self.AC_FANRATE])

        if self.AC_FANDIRECTION == '1':
            self.updateICON("fan_dir_icon", "op_btm_drction_ul_eu.png")
        else:
            self.updateICON("fan_dir_icon", "op_btm_drction_ul_off_eu.png")
            
        if self.AC_MODE in (3,4):
            self.updateICON("back_plus_minus", "co_back_plus_minus.png")
        else:
            self.hideICON("back_plus_minus")
        
    def hideICON(self, iconName):
        self[iconName].hide()
        
    def updateICON(self, iconName, fileName):
        #self["on_off_icon"].hide()
        self[iconName].updateIcon("/usr/lib/enigma2/python/Plugins/Extensions/MSNweather/aircon_data/%s" % fileName)
        self[iconName].show()

    def keyCancel(self):
        self.close()
      
    def keySave(self):
        self.close()

    def keyRed(self): #fan
        if self.AC_FANRATE == 'A':   self.AC.set_control_info({'f_rate': 'B'})
        elif self.AC_FANRATE == 'B': self.AC.set_control_info({'f_rate': '3'})
        elif self.AC_FANRATE == '3': self.AC.set_control_info({'f_rate': '4'})
        elif self.AC_FANRATE == '4': self.AC.set_control_info({'f_rate': '5'})
        elif self.AC_FANRATE == '5': self.AC.set_control_info({'f_rate': '6'})
        elif self.AC_FANRATE == '6': self.AC.set_control_info({'f_rate': '7'})
        elif self.AC_FANRATE == '7': self.AC.set_control_info({'f_rate': 'A'})
        self.getACstate()

    def keyGreen(self):
        if self.AC_POWER: self.AC.set_power(False)
        else:             self.AC.set_power(True)
        self.getACstate()
      
    def keyYellow(self): #direction
        if self.AC_FANDIRECTION == '1': self.AC.set_control_info({'f_dir': '0'})
        else:                           self.AC.set_control_info({'f_dir': '1'})
        self.getACstate()

    def keyBlue(self): #mode
        if self.AC_MODE == 1:   self.AC.set_mode(3)
        elif self.AC_MODE == 3: self.AC.set_mode(4)
        elif self.AC_MODE == 4: self.AC.set_mode(6)
        elif self.AC_MODE == 6: self.AC.set_mode(2)
        elif self.AC_MODE == 2: self.AC.set_mode(1)
        self.getACstate()

    def setTemp(self, doIncrease):
        if self.AC_SETTEMP != 0:
            if doIncrease: self.AC_SETTEMP += 1
            else:          self.AC_SETTEMP -= 1
            if self.AC_SETTEMP < 18:   self.AC_SETTEMP
            elif self.AC_SETTEMP > 32: self.AC_SETTEMP
            self.AC.set_target_temp(self.AC_SETTEMP)
            self.getACstate()
        
    def keyLeft(self): #temp -
        self.setTemp(False)
        
    def keyRight(self): #tem +
        self.setTemp(True)
