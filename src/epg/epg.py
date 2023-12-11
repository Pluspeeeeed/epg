from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
import time
import unittest

from dateutil.relativedelta import relativedelta

class Catchup(Enum):
    NONE = 0
    DEFAULT =1
    APPEND = 2
    SHIFT = 3

#When processing an XMLTV file the addon will attempt to find a channel loaded from the M3U that matches the EPG channel. It will cycle through the full set of M3U channels checking for one condition on each pass. The first channel found to match is the channel chosen for this EPG channel data.
#1st pass: Does theid attribute of the <channel> element from the XMLTV match the tvg-id from the M3U channel. If yes we have a match, don't continue.
#Before the second pass: Was a value provided, if not skip this channels EPG data.
#2nd pass: Does the as it is or with spaces replaced with '_''s match tvg-name from the M3U channel. If yes we have a match, don't continue.
#3rd pass: Does the match the M3U channel name. If yes we have a match, phew, eventually found a match.

@dataclass
class EPG:
    channel_id: str     #match Channel.id, Channel.name or Channel.display_name
    start_time: datetime
    end_time: datetime
    title: str
    crawl_time: datetime
    source: str
    desc: str = ''

@dataclass
class Channel:
    id: str             
    display_name: str
    stream_url: str
    catchup_type: Catchup
    name: str = '' 
    icon_src: str = ''
    group: list = []
    catchup_source: str = ''

    def __str__(self) -> str:
        base = f'#EXTINF:-1 tvg-id-\"{self.id}\"'
        if self.name != '':
            base = base + f' tvg-name=\"{self.name}\"'
        if self.icon_src != '':
            base = base + f' tvg-logo=\"{self.icon_src}\"'
        if self.group != []:
            base = base + f' group-title=\"{";".join(str(i) for i in self.group)}\"'
        if(self.catchup_type.value != 0):
            base = base + f' catchup=\"{self.catchup_type.name.lower()}\" catchup-source=\"{self.catchup_source}\"'
        base = base + f',{self.display_name}\n{self.stream_url}'
        return base
    
class TestEPGClass(unittest.TestCase):
    def setup(self):
        NOW = datetime.now()
        self.epg = EPG('CCTV1', NOW, NOW+relativedelta(minutes=+62), '新闻联播', NOW+relativedelta(microseconds=-1551), 'local')

class TestChannelClass(unittest.TestCase):
    def setup(self):
        self.channel = Channel('CCTV1', 'CCTV-1 综合', 'http://cntv.cn/live/cctv1', Catchup.NONE)
