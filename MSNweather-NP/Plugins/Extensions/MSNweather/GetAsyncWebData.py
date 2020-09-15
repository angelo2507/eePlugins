# @j00zek 2020
#This script resolves issue with freezing E2 in case of network problems

import os
import sys
import time
import urllib, urllib2

from debug import printDEBUG

def GetAsyncWebDataDEBUG(myFUNC = '' , myText = '' ):
    printDEBUG( myFUNC , myText, 'GetAsyncWebData.log' )

def downloadWebPage( webURL, webFileName ):
    GetAsyncWebDataDEBUG('\t', "webURL = '%s'\n\twebFileName = '%s'" % (webURL , webFileName))
    try:
        webContent = urllib2.urlopen(webURL).read()
        retCode = 0
    except Exception as e:
        GetAsyncWebDataDEBUG('\t', str(e))
        webContent = ''
        retCode = 1
    #saving to file
    with open('/tmp/.MSNdata/%s' % webFileName, "w") as f:
        f.write(webContent)
    
    
if __name__ == '__main__':
    GetAsyncWebDataDEBUG('GetAsyncWebDataDEBUG', '.__name__')
    if len(sys.argv) -1 == 0:
        GetAsyncWebDataDEBUG('ERROR', 'NO arguments provided !!!')
        sys.exit(1)
    GetAsyncWebDataDEBUG('\t', 'Arguments (%s):' % (len(sys.argv) -1) )
    for myArg in sys.argv:
        if '=' in myArg:
            myArg = myArg.split('=')
            param = myArg[0].strip()
            value = myArg[1].strip()
            GetAsyncWebDataDEBUG('\t\t', "%s = '%s'" % (param, value))
            exec("%s = '%s'" % (param, value))

    try:
        if weatherSearchFullName != '':
            #XML
            url = 'http://weather.service.msn.com/data.aspx?src=windows&weadegreetype=%s&culture=%s&wealocations=%s' % (degreetype, language, urllib.quote(locationcode))
            downloadWebPage( url, 'data_msn.xml' )
            #web
            url = 'https://www.msn.com/%s/weather?culture=%ss&weadegreetype=%s&form=PRWLAS&q=%s' % (language, language, degreetype, urllib.quote(weatherSearchFullName))
            downloadWebPage( url, 'data_msn.web' )
        
        #thingspeak
        if thingSpeakChannelID != '':
            url = 'https://thingspeak.com/channels/%s/feeds.xml?average=10&results=1' % thingSpeakChannelID
            downloadWebPage( url, 'data_thingSpeak.xml' )
        #airly
    except Exception as e:
        GetAsyncWebDataDEBUG('EXCEPTION', str(e))
    