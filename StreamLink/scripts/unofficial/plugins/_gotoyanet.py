import logging
import re

from streamlink.plugin import Plugin
from streamlink.plugin.api import useragents
from streamlink.utils import update_scheme
from streamlink.stream._ffmpegmux import FFMPEGMuxer
from streamlink.stream import HLSStream

log = logging.getLogger(__name__)


class gotoyanet(Plugin):
    #### Przykladowy link do kamery
    #https://go.toya.net.pl/25-kamery/13758-lodz/444413758155-piotrkowska-narutowicza/play
    #### kawalek kodu strony gdzie jest adres strumienia
    #class="player" data-stream="https://cdn-3-go.toya.net.pl:8081/kamery/lodz_piotrkowskanarutowicza.m3u8?p=474f43414d005f5e0ff.bd9750ac468f5d2d573a00637374" data-mode="cam"
    #### adres z powyzszego kawalka
    #https://cdn-3-go.toya.net.pl:8081/kamery/lodz_piotrkowskanarutowicza.m3u8?p=474f43414d005f5e0ff.bd9750ac468f5d2d573a00637374
    
    _url_re = re.compile(r"https?://go\.toya\.net\.pl")
    _addr_re = re.compile(r'[ ]*data-stream="([^"]+)"')
    #_addr_re = re.compile(r'[ ]*src="blob:([^"]+)"')

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None

    def _get_streams(self):
        #self.session.set_option('hls-live-edge', 10)
        self.session.http.headers.update({'Referer': 'https://go.toya.net.pl'})
        self.session.http.headers.update({'User-Agent': useragents.ANDROID})
        res = self.session.http.get(self.url)
        log.debug(res.text)
        
        try:
            address = self._addr_re.search(res.text).group(1)
            address = address.split('?p')[0]
            log.debug("Found address: %s" % address)
        except Exception as e:
            log.debug(str(e))
            return

        for s in HLSStream.parse_variant_playlist(self.session, address).items():
            yield s
            
        #return {"rtsp_stream": FFMPEGMuxer(self.session, *(address,), is_muxed=False, format='mpegts', vcodec = 'copy', acodec = 'copy' )}

__plugin__ = gotoyanet
