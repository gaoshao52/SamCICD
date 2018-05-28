#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang

import time


def sec_to_time(s):
    t = ""
    (hour, sec) = divmod(s, 3600)
    if hour < 10:
        t += "0"
    t += str(hour)+"小时"
    (minute, sec) = divmod(sec, 60)
    if minute <10:
        t += "0"
    t += str(minute)+ "分"
    if sec <10:
        t += "0"
    t += str(sec) + "秒"
    return t



if __name__ == '__main__':
    (hour, minute) = divmod(3600012, 3600)
    print(type(hour))
    print(type(minute))