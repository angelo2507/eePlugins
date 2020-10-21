#!/usr/bin/python2.7
# j00zek 2020-2021

import os
os.environ["XDG_CONFIG_HOME"] = "/etc" #aby config streamlinka dzialal

def clearCache(): #zawsze dobrze oczyscic przed uruchomieniem os.system aby nie bylo GS-a
    with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")

def cleanCMD(): #czyszczenie smieci
    clearCache()
    os.system("""
if [ `ps -ef|grep -v grep|grep -c ffmpeg` -eq 0 ];then 
 rm -f /tmp/ffmpeg-*
fi
killall hlsdl 2>/dev/null
[ -e /tmp/stream.ts ] && rm -f /tmp/stream.ts
""")
