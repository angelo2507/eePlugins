# -*- coding: utf-8 -*-
from enigma import eConsoleAppContainer, getDesktop
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
    
class OMBsystem: #Calling os.system is not recommended, it may fail due to lack of memory and blocks E2 mainthread
    def __init__(self, cmd, callBackFun=None):
        self.callBackFun = callBackFun
        self.cmd = cmd
        
        self.console = eConsoleAppContainer()
        if None != self.callBackFun:
            self.console_appClosed_conn = eConnectCallback(self.console.appClosed, self._cmdFinished)
            self.console_stdoutAvail_conn = eConnectCallback(self.console.stdoutAvail, self._dataAvail)
            self.outData     = ""
        self.console.execute( E2PrioFix( cmd ) )
        
    def terminate(self, doCallBackFun=False):
        self.kill(doCallBackFun)
        
    def kill(self, doCallBackFun=False):
        if None != self.console:
            if None != self.callBackFun:
                self.console_appClosed_conn = None
                self.console_stdoutAvail_conn = None
            else:
                doCallBackFun = False
            self.console.sendCtrlC()
            self.console = None
            if doCallBackFun:
                self.callBackFun(-1, self.outData)
                self.callBackFun = None

    def _dataAvail(self, data):
        if None != data:
            self.outData += data

    def _cmdFinished(self, code):
        self.console_appClosed_conn = None
        self.console_stdoutAvail_conn = None
        self.console = None
        self.callBackFun(code, self.outData)
        self.callBackFun = None

    def __del__(self):
        pass

class OMBconsole(Screen):
    def __init__(self, session, title = "Executing...", cmdlist = None, txtLines = 2, finishedCallback = None, closeOnSuccess = True):
        if getDesktop(0).size().width() == 1080:
            fontH = 18
            posY  = 1080 - 60 - fontH * txtLines
        else:
            fontH = 14
            posY  = 1080 - 40 - fontH * txtLines
        sizeY = fontH * txtLines
            
        self.skin = """
          <screen name="OMBconsole" position="60,%s" size="400,%s" title="%s">
            <widget name="text" position="0,0" size="400,%s" font="Console;%s" backgroundColor="background" transparent="1"/>
          </screen>""" % (posY,sizeY,sizeY,title,fontH)
        
        Screen.__init__(self, session)

        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.errorOcurred = False

        self["text"] = ScrollLabel("")
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"], 
        {
            "ok": self.cancel,
            "back": self.cancel,
            "up": self["text"].pageUp,
            "down": self["text"].pageDown
        }, -1)
        
        self.cmdlist = cmdlist
        #self.newtitle = title
        
        #self.onShown.append(self.updateTitle)
        
        self.container = eConsoleAppContainer()
        self.run = 0
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun) # dont start before gui is finished

    #def updateTitle(self):
    #    self.setTitle(self.newtitle)

    def startRun(self):
        self["text"].setText("" + "\n\n")
        with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n") #just in case for low memory tuners
        if self.container.execute(self.cmdlist[self.run]): #start of container application failed...
            self.runFinished(-1) # so we must call runFinished manual

    def runFinished(self, retval):
        if retval:
            self.errorOcurred = True
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]): #start of container application failed...
                self.runFinished(-1) # so we must call runFinished manual
        else:
            #lastpage = self["text"].isAtLastPage()
            str = self["text"].getText()
            self["text"].setText(str)
            #if lastpage:
            self["text"].lastPage()
            if self.finishedCallback is not None:
                self.finishedCallback()
            self.cancel()

    def cancel(self):
        if self.run == len(self.cmdlist):
            self.close()
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)

    def dataAvail(self, str):
        #self["text"].setText(self["text"].getText() + str)
        self["text"].setText(str)
        self["text"].lastPage()
