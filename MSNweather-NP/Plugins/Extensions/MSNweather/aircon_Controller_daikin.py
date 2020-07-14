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
from Components.Label import Label
#from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen

######################################################################################################
class DaikinController(Screen):
    def __init__(self, session):
        self.skin = """
<screen position="center,center" size="640,500" title="Daikin A/C controller" backgroundColor="#20606060" >
<!-- Configuration section and buttons do not change -->
    <eLabel position="10,120" size="620,350" zPosition="-1" backgroundColor="#00222222" /> 
    <widget name="key_red" position="0,470" zPosition="5" size="320,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
    <widget name="key_green" position="320,470" zPosition="5" size="320,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
<!-- Configuration section and buttons do not change -->
</screen> 
"""
        Screen.__init__(self, session, AC_IP, AC_PORT, AC_info )
        
        self.AC_IP = AC_IP
        self.AC_PORT = AC_PORT
        self.AC_info = AC_info
        
        # Buttons
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label("OK")

        # Define Actions
        self["actions"] = ActionMap(["MSNweatherNPacControllers"],
            {
                "keyCancel": self.keyCancel,
                "keyRed": self.keyCancel,
                "keyOk": self.keySave,
                "keyGreen": self.keySave,
            }
        )

        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        #self.setTitle(self.setup_title)
        pass

    def changed(self):
        pass

    def keyCancel(self):
        self.close()
      
    def keySave(self):
        self.close()
 