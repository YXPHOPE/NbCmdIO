import re
from unicodedata import east_asian_width


def getCharWidth(c: str):
    """返回字符宽度
    F W A ：全宽，Na、H：半宽，N：0
    """
    w = east_asian_width(c)
    if w == "N": 
        return 0
    return 2 if w in ("F", "W", "A") else 1


def getStringWidth(s: str):
    """返回字符串去除CSI转义序列、\n、\t后的显示长度"""
    raw = re.sub(r"\033\[[\d;\?]*[a-zA-Z]", "", s)  # 去除csi转义序列
    raw = re.sub(r"[\n\t]", "", raw)
    return sum(getCharWidth(c) for c in raw)


def getEscapeString(s: str):
    """将一些不可见的控制字符转为可见的转义字符，包括空格32之前的和127 Delete（Oct：177）"""
    res = ""
    for i in s:
        if ord(i) < ord(" ") or i == "\177":
            res += i.encode("unicode-escape").decode()
        else:
            res += i
    return res


def padString(s: str, width: int, mode=-1, fillchar=" "):
    """填充字符串s到宽度width （基于占位宽度）
    - mode: -1 左对齐右侧补充字符，0 居中对齐两边补充字符，1右对齐 左侧补充字符"""
    w = getStringWidth(s)
    if w >= width:
        return s
    width_fill_char = getStringWidth(fillchar)
    n = (width - w) // width_fill_char
    if mode == -1:
        s += fillchar * n
    elif mode == 0:
        h = n // 2
        s = fillchar * h + s + fillchar * (n - h)
    elif mode == 1:
        s = fillchar * n + s
    else:
        raise ValueError(f"Parameter mode must be in -1,0,1 (got {mode}).")
    return s


def splitLinesByWidth(s: str, width: int) -> list[str]:
    """按照显示宽度分割字符串，\\n 也会被分割，请不要包含 \\t 等字符，CSI转义序列会被保存但不计入宽度"""
    res, csi = [], []  # 结果，转义序列位置
    line, lwidth, i = "", 0, 0
    for match in re.finditer(r"\033\[[\d;\?]*[a-zA-Z]", s):
        csi.append(match.span())
    while i < len(s):
        chr = s[i]
        if csi and csi[0][0] == i:
            i = csi[0][1]
            line += s[csi[0][0] : csi[0][1]]
            csi.pop(0)
            continue
        if chr != "\n":
            line += chr
            lwidth += getCharWidth(chr)
        if lwidth >= width or chr == "\n":
            # ? 如果只剩1宽度，加入一个双宽字符，会溢出1宽度
            res.append(line)
            line = ""
            lwidth = 0
        i += 1
    if line:
        res.append(line)
    return res
