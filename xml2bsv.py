import re
from datetime import datetime,timedelta
import time


def xml2utc(xml):
    match = re.search(r'([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}) ([+-])([0-9]{2})([0-9]{2})',xml)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))
        sign = match.group(7)
        hours = int(match.group(8))
        minutes = int(match.group(9))
        dt = datetime(year,month,day,hour,minute,second)
        td = timedelta(hours=hours,minutes=minutes)
        if sign == '+':
            dt = dt - td
        else:
            dt = dt + td
        return dt
    return ''


def utc2local (utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
    return utc + offset
    
def xml_channels():


    import xml.etree.ElementTree as ET
    f = open("xmltv.xml")
    xml = f.read()
    tree = ET.fromstring(xml)
    order = 0
    channels_file = open("channels.bsv","w")
    for channel in tree.findall(".//channel"):
        id = channel.attrib['id']
        display_name = channel.find('display-name').text
        try:
            icon = channel.find('icon').attrib['src']
        except:
            icon = ''
        write_str = "%s\n" %'|'.join((display_name,id,icon,"%06d" % order))
        #write_str = "%s=\n" % (id)
        channels_file.write(write_str.encode("utf8"))
        order = order + 1
        
    programmes_file = open("programmes.bsv","w")
    for programme in tree.findall(".//programme"):
        start = programme.attrib['start']
        start = xml2utc(start)
        start = utc2local(start)
        channel = programme.attrib['channel']
        title = programme.find('title').text
        match = re.search(r'(.*?)"}.*?\(\?\)$',title) #BUG in webgrab
        if match:
            title = match.group(1)
        try:
            sub_title = programme.find('sub-title').text
        except:
            sub_title = ''
        try:
            date = programme.find('date').text
        except:
            date = ''
        try:
            desc = programme.find('desc').text
        except:
            desc = ''
        try:
            episode_num = programme.find('episode-num').text
        except:
            episode_num = ''
        series = 0
        episode = 0
        match = re.search(r'(.*?)\.(.*?)[\./]',episode_num)
        if match:
            try:
                series = int(match.group(1)) + 1
                episode = int(match.group(2)) + 1
            except:
                pass
        series = str(series)
        episode = str(episode)
        categories = ''
        for category in programme.findall('category'):
            categories = ','.join((categories,category.text)).strip(',')
        
        #programmes = plugin.get_storage(channel)
        total_seconds = time.mktime(start.timetuple())
        line = "%s\n" % '|'.join((channel,str(int(total_seconds)),title,sub_title,date,series,episode,categories,desc)).encode("utf8")
        programmes_file.write(line)
        
xml_channels()        