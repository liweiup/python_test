import os
import sys
from itertools import groupby
from operator import itemgetter


def split_group(dict_list, key):
    dict_list.sort(key=itemgetter(key))
    tmps = groupby(dict_list, itemgetter(key))
    result = []
    for key, group in tmps:
        result.append({key: list(group)})
    return result


if getattr(sys, 'frozen', False):
    # PyInstaller 打包后的路径
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))