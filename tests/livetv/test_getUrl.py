import os, sys; sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import lib.patch_sys_path
from unittest.mock import patch

def mock_request_handler(url):
    class MockRequestHandler:
        def __init__(self, sUrl):
            self.__sUrl = sUrl
        def request(self):
            pass
        def getRealUrl(self):
            return self.__sUrl
    return MockRequestHandler(url)

@patch('resources.lib.handler.requestHandler.cRequestHandler', side_effect=mock_request_handler)
def test_src_semicolon(mock_request_handler):
    from resources.sites.livetv import getUrl
    referer = 'https://nextstream.click/steam.php?stream=4eLyr2RZq7v'
    html = "src: 'https://onestream.click/hls/4eLyr2RZq7v/index.m3u8?st=1lBXj7w1EFwxOdJCYpSACA&e=1743871416',"
    result = getUrl(html, referer)
    assert result == f'https://onestream.click/hls/4eLyr2RZq7v/index.m3u8?st=1lBXj7w1EFwxOdJCYpSACA&e=1743871416|referer={referer}'

def test():
    test_src_semicolon()