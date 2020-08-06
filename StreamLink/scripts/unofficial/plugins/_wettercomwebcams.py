import logging
import re

from streamlink.plugin import Plugin
from streamlink.plugin.api import useragents
from streamlink.utils import update_scheme
from streamlink.stream._ffmpegmux import FFMPEGMuxer

log = logging.getLogger(__name__)


class wettercomwebcams(Plugin):
    #http://www.wetter.com/hd-live-webcams/deutschland/roettenbach-deutschland/560d13e66ad05/
    #data-video-url-rtmp="rtmp://94.228.211.161:1935/live/livecam012.stream"
    #data-video-url-mp4=""
    #data-video-url-hls="https://5811bd721519c.streamlock.net:1936/live/livecam012.stream/playlist.m3u8"
    
    _url_re = re.compile(r"https?://www.wetter.com/hd-live-webcams")
    _addr_re = re.compile(r'[ ]*data-video-url-hls="([^"]+)"')

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None

    def _get_streams(self):
        self.session.set_option('hls-live-edge', 10)
        res = self.session.http.get(self.url)
        #log.debug(res.text)
        
        try:
            address = self._addr_re.search(res.text).group(1)
            log.debug("Found address: %s" % address)
        except Exception as e:
            log.debug(str(e))
            return
        
        return {"rtsp_stream": FFMPEGMuxer(self.session, *(address,), is_muxed=False)}

__plugin__ = wettercomwebcams
