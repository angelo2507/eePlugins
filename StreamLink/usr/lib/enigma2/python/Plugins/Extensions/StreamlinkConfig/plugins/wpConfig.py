from streamlink.e2config import getE2config
import os

params = { 'login_url'        : 'https://pilot.wp.pl/api/v1/user_auth/login',
           'main_url'         : 'https://pilot.wp.pl/api/v1/channels/list?device=androidtv',
           'video_url'        : 'https://pilot.wp.pl/api/v1/channel/',
           'close_stream_url' : 'https://pilot.wp.pl/api/v1/channels/close',
          }

headers = { 'user-agent': 'ExoMedia 4.3.0 (43000) / Android 8.0.0 / foster_e',
            'accept': 'application/json',
            'x-version': 'pl.videostar|3.25.0|Android|26|foster_e',
            'content-type': 'application/json; charset=UTF-8'
          }

data = {'device': 'AndroidTV', 
        'login' : getE2config('WPusername'), 
        'password': getE2config('WPpassword')
      }

PreferDash = getE2config('WPpreferDASH', False)
videoDelay = getE2config('WPvideoDelay', 0)

def saveCookie(cookie):
    open("/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/pilotwppl.cookie", "w").write('%s' % cookie)
  
def getCookie():
    if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/pilotwppl.cookie"):
        return open("/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/pilotwppl.cookie", "r").read().strip()
    else:
        return None
