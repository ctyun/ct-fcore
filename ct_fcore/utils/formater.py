# -*- coding:utf-8 -*-
import datetime, time


def date2timestamp(datestr, formatstr="%a %b %d %Y %H:%M:%S "):
    '''
    将js产生的Date转换成时间戳.
    :param datestr: js的Date对象直接转换成的字符串
    :param formatstr: Datetime字符串的格式, 一般不需要传入
    :return: 时间戳
    '''
    if "GMT" in datestr:
        datestr = datestr.split("GMT")[0]
    ctime = datetime.datetime.strptime(datestr, formatstr)
    return time.mktime(ctime.timetuple())

def timestamp2str(timestamp, formatstr="%Y-%m-%d %H:%M:%S"):
    '''
    将时间戳转换成表示时间和日期的字符串
    :param timestamp: 时间戳
    :param formatstr: 时间和日期字符串格式
    :return: 时间和日期字符串
    '''
    return time.strftime(formatstr, time.localtime(timestamp))