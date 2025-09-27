import re
from typing import Union
from PIL import Image
from unicodedata import east_asian_width
import time

# ------------------------------字符类处理函数---------------------------------
TabWidth = 4
Tab = " " * TabWidth

def getCharWidth(c: str):
    """返回字符宽度
    F W A ：全宽，Na、H：半宽，N：0
    """
    w = east_asian_width(c)
    if w == "N":
        # \t 应该返回多少宽度？
        return 0
    return 2 if w in ("F", "W", "A") else 1


def getStringWidth(s: str):
    """返回字符串去除CSI转义序列、\n、\t后的显示长度"""
    raw = re.sub(r"\033\[[\d;\?]*[a-zA-Z]", "", s)  # 去除csi转义序列
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


# textwrap.wrap()的简化版，但是该方法不会解析转义序列，因此不采用
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


# ------------------------------颜色类处理函数---------------------------------

RGB = Union[list[int], tuple[int, int, int]]


def hex2RGB(hex: str):
    """hex color to RGB color"""
    if hex[0] == "#":
        hex = hex[1:]
    hexes = []
    if len(hex) == 6:
        hexes = [hex[:2], hex[2:4], hex[4:]]
    elif len(hex) == 3:
        hexes = [hex[:1] * 2, hex[1:2] * 2, hex[2:] * 2]
    else:
        raise ValueError("Hex color should be like #F0F or #00FFFF")
    return [int(i, 16) for i in hexes]


def genGradient(color_start, color_end, num):
    """生成两个RGB颜色之间的渐变色列表
    - color_start: 起始颜色，格式为 (r, g, b)
    - color_end: 结束颜色，格式为 (r, g, b)
    - num: 总共要生成的渐变色数量（包括起始和结束颜色）

    Returns:
        包含起始颜色、渐变色和结束颜色的列表
    """
    # 将颜色值转换为浮点数以便计算
    r_start, g_start, b_start = color_start
    r_end, g_end, b_end = color_end

    # 计算每个通道的步长
    num -= 1
    r_step = (r_end - r_start) / num
    g_step = (g_end - g_start) / num
    b_step = (b_end - b_start) / num

    # 生成渐变色
    gradient = []
    for i in range(num + 1):
        r = int(r_start + r_step * i)
        g = int(g_start + g_step * i)
        b = int(b_start + b_step * i)
        gradient.append((r, g, b))

    return gradient


def getIMG(img_path:str, width:int, height=0x7FFFFFFF, resample=1):
    try:
        if isinstance(img_path,str):
            img = Image.open(img_path)
        elif isinstance(img_path, Image.Image):
            img = img_path
        else:
            raise TypeError("Invalid type!")
    except Exception as e:
        raise ValueError(f"Parameter img_path({img_path}) is not "
                         "a valid image path or instance of Image: {e}.")
    # 计算缩放比例
    img_width, img_height = img.size
    ratio_width = width / img_width
    ratio_height = height / img_height
    ratio = min(ratio_width, ratio_height)
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    if new_height % 2:
        new_height += 1
    # 缩放图片
    img = img.resize((new_width, new_height), resample)
    img = img.convert("RGB")
    return img

# 通过耗时测试性能（本身也耗时，自测耗0.015s左右）
class Timer:
    def __init__(self) -> None:
        self.t1 = 0
        self.t2 = 0

    def __enter__(self):
        self.t1 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t2 = time.time()
        print(f"{self.t2 - self.t1:.4f}")

TIMER = Timer()
