# -*- coding: utf-8 -*-
#
#    j00zekGetWebPic
#
#    Coded by j00zek (c)2020
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem konwertera
#    Please respect my work and don't delete/change name of the renderer author
#
#    Nie zgadzam sie na wykorzystywanie tego skryptu w projektach platnych jak np. Graterlia!!!
#
#    Prosze NIE dystrybuowac tego skryptu w formie archwum zip, czy tar.gz
#    Zgadzam sie jedynie na dystrybucje z repozytorium opkg
#    

from Components.Console import Console
from Components.Element import cached
from Components.j00zekComponents import isINETworking
from Converter import Converter
from enigma import eTimer
import os, urllib, urllib2

DBG = False
if DBG: 
    try: from Components.j00zekComponents import j00zekDEBUG
    except Exception: DBG = False

class j00zekGetWebPic(Converter, object):
    def __init__(self, type):
        if DBG: j00zekDEBUG('[j00zekGetWebPic:__init__] >>>')
        Converter.__init__(self, type)
        self.refreshTimer = eTimer()
        self.refreshTimer.callback.append(self.getPic)
        self.myConsole = Console()
        
        self.isSuspended = False
        self.RefreshTimeMS   = 10000
        self.downloadCommand = 'curl -L https://picsum.photos/800 -o /tmp/randomWebPic.jpg'
        self.downloadToFile  = '/tmp/randomWebPic.jpg'
        if os.path.exists(type):
            with open(type, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or line == '' or not '=' in line:
                        continue
                    else:
                        cfg = line.split('=')
                        if cfg[0] == 'RefreshTime':
                            self.RefreshTimeMS = int(cfg[1]) * 1000
                        elif cfg[0] == 'downloadCommand':
                            self.downloadCommand = cfg[1]
                        elif cfg[0] == 'downloadToFile':
                            self.downloadToFile = cfg[1]
                f.close()
        elif type == '/etc/enigma2/user_webCam1.cfg':
            from Components.Language import language
            with open(type, 'w') as f:
                if language.getLanguage() == 'pl_PL':
                    f.write("#Przykladowa konfiguracja WebCam-a\n")
                    f.write("#  RefreshTime -  czas w sekundach do odswierzenia obrazka\n")
                    f.write("#  downloadCommand -komenda basha pobierajaca obrazek\n")
                    f.write("#    Np. dla kamer dahua:curl --user 'usr:passwd' 'http://192.168.1.102:80/cgi-bin/snapshot.cgi' --digest -o /tmp/WebCamSpanshot.jpg\n")
                    f.write("#  downloadToFile - nazwa pliku do ktorego jest pobrany obrazek\n")
                else:
                    f.write("#:Example webCam configuration\n")
                    f.write("#  RefreshTime -  time in seconds to refresh picture\n")
                    f.write("#  downloadCommand - bash command to download picture\n")
                    f.write("#    E.g. for dahua:curl --user 'usr:passwd' 'http://192.168.1.102:80/cgi-bin/snapshot.cgi' --digest -o /tmp/WebCamSpanshot.jpg\n")
                    f.write("#  downloadToFile - filename of downloaded picture\n")
                f.write("RefreshTime=10\n")
                f.write("downloadCommand=curl -L https://picsum.photos/800 -o /tmp/randomWebPic.jpg\n")
                f.write("downloadToFile=/tmp/randomWebPic.jpg\n")
                f.close()
        if DBG: j00zekDEBUG('\n\t read params: type="%s"\n\t\t self.RefreshTimeMS=%s, self.downloadCommand=%s,\n\t\t self.downloadToFile=%s' % (type,self.RefreshTimeMS,self.downloadCommand,self.downloadToFile)) 
        self.refreshTimer.start(100)         

    def getPic(self):
        if DBG: j00zekDEBUG('[j00zekGetWebPic:getPic] >>>')
        self.refreshTimer.stop()
        if isINETworking():
            try:
                with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
                self.myConsole.ePopen('rm -f %s;%s' % (self.downloadToFile, self.downloadCommand))
                #os.system('rm -f %s;%s &' % (self.downloadToFile, self.downloadCommand))
            except Exception as e:
                if DBG: j00zekDEBUG('j00zekGetWebPic:getPic] got Exception: %s' % str(e))
        self.refreshTimer.start(self.RefreshTimeMS)
        
    def doSuspend(self, suspended): 
        if suspended == 1: 
            self.refreshTimer.stop()
            self.isSuspended = True
        else: 
              if self.isSuspended:
                  if DBG: j00zekDEBUG('[j00zekGetWebPic:doSuspend] initiates refreshTimer')
                  self.refreshTimer.start(100)
                  self.isSuspended = False
            
    @cached
    def getText(self):
        retVal = ''
        if os.path.exists(self.downloadToFile):
            retVal = self.downloadToFile
        if DBG: j00zekDEBUG('[j00zekGetWebPic:getText] = %s' % self.downloadToFile)
        return retVal
        
    text = property(getText)
