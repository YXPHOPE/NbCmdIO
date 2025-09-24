import re
from unicodedata import east_asian_width

def getCharWidth(c: str):
    return 2 if east_asian_width(c) in ("F", "W", "A") else 1

def getStringWidth(s: str):
    """返回字符串去除CSI转义序列、\n、\t后的显示长度"""
    raw = re.sub(r"\033\[[\d;\?]*[a-zA-Z]", "", s)  # 去除csi转义序列
    raw = re.sub(r"[\n\t]", "", raw)
    return sum(getCharWidth(c) for c in raw)

def getEscapeString(s: str):
    """将一些不可见的控制字符转为可见的转义字符"""
    res = ''
    for i in s:
        if ord(i)<31:
            res += i.encode('unicode-escape').decode()
        else: res += i
    return res

def padString(s: str, width: int, mode=-1, fillchar=' '):
    """ 填充字符串s到宽度width （基于占位宽度） 
    - mode: -1 左对齐右侧补充字符，0 居中对齐两边补充字符，1右对齐 左侧补充字符"""
    w = getStringWidth(s)
    if w >= width:
        return s
    width_fill_char = getStringWidth(fillchar)
    n = (width-w)//width_fill_char
    if mode == -1:
        s += fillchar * n
    elif mode == 0:
        h = n//2
        s = fillchar*h + s + fillchar*(n-h)
    elif mode == 1:
        s = fillchar * n + s
    else: raise ValueError(f"Parameter mode must be in -1,0,1 (got {mode}).")
    return s