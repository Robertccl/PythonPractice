# -*- coding: utf-8 -*-
# author : ccl
import hashlib
import re

"""
工具类 
"""

#把很长的url转换成md5字符串保存
def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

if __name__ == "__main__":
    print(get_md5("http://jbcdn2.b0.upaiyun.com/2017/05/77d80105fd15f2465894827e23cc4842.jpeg".encode("utf-8")))