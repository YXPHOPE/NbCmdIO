"""
Author: Cipen
Date:   2024/05/27
Desc:   提供一个基于控制台输出的任意位置输出RGB色彩文字，只需设置一次Style，即可用于在任意loc的文字输出，直到reset
参见：https://www.man7.org/linux/man-pages/man4/console_codes.4.html
致谢：少部分内容借鉴colorama、curses
"""

from typing import Any, Union
from platform import system as getOS
from os import system, get_terminal_size
from unicodedata import east_asian_width
import re
from .style import Style

# window cmd 默认禁用ANSI 转义序列，可通过以下3种方法启用
# 1. cls
# 2. reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
# 3. kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Output:
    __cls = "cls"
    CSI = '\033['
    OSC = '\033]'
    RESET = '\033[0m'
    __version__ = '1.8.3'

    def __init__(self, auto_reset=True) -> None:
        """只需通过链式调用设置一次Style，即可用于在with上下文中任意loc的文字输出，直到reset"""
        self.auto_reset = auto_reset
        self.size_row = 0
        self.size_col = 0
        self.getsize()
        self.origin_row = 0
        self.origin_col = 0
        self.width = self.size_col
        self.height = self.size_row
        self.str = ''
        """用于保存已配置style直至打印内容或reset前"""

        os = getOS()
        if os == "Windows":
            self.__cls = "cls"
            try:
                import ctypes

                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                # -11 是 stdout 句柄
            except:
                self.cls()
        elif os == "Linux":
            self.__cls = "clear"
    
    def setTitle(self, title: str):
        print(f'\033]2;{title}\a', end="")
        return self

    # 清除相关
    def cls(self):
        """调用系统命令清屏"""
        system(self.__cls)
        return self

    def clearAll(self):
        """输出CSI转义序列清屏"""
        return self.loc(0).__p('2J')
    
    def clearAllBeforeCursor(self):
        return self.__p("1J")
    
    def clearAllAfterCursor(self):
        return self.__p("0J")

    def reset(self):
        """重置所有样式"""
        self.str = ''
        return self.__p("0m")

    def clearLine(self):
        return self.__p("2K")
    
    def clearLineBefore(self, col=-1):
        if col>=0:
            self.col(col)
        return self.__p("1K")

    def clearLineAfter(self, col=-1):
        if col>=0:
            self.col(col)
        return self.__p("K")

    def end(self):
        """重置颜色，并打印换行结尾"""
        self.reset()
        print("\n", end="")
        return self

    # 执行 内部打印通道
    def __p(self, s: str, *args):
        s = self.CSI + s
        self.str += s
        print(s, end="")
        if args:
            self.print(*args)
        return self

    # 打印输出的3种方式：prt(*arg)、prt>=value、prt.print(*arg)
    def __call__(self, *args: Any, **kwds: Any):
        return self.print(*args, **kwds)

    def __ge__(self, s):
        print(s, end="")

    def print(self, *args, **kwds):
        """
        ### 以已加载样式输出所有内容
        - 默认end=""
        - 将会清除self.str中保存的样式
        - 默认自动reset重置样式
        """
        if 'end' not in kwds:
            kwds['end'] = ""
        self.str = ''
        print(*args, **kwds)
        return self.reset() if self.auto_reset else self

    def auto_reset_on(self):
        self.auto_reset = True
        return self

    def auto_reset_off(self):
        """不建议关闭自动重置Style，可以使用with上下文管理器来使其中的prt不自动重置"""
        self.auto_reset = False
        return self

    # 光标相对定位：^n|n>n<n>>n<<n
    # 优先级：<<>>  ^ | <>
    # 比较运算符 < > 无法连续运算
    def __xor__(self, n: int):
        return self.up(n)

    def __or__(self, n: int):
        return self.down(n)

    def updown(self, n: int):
        if n > 0:
            ud = "A"
        else:
            n = -n
            ud = "B"
        return self.__p(f"{n}{ud}")

    def up(self, n: int, col=-1):
        if n > 0:
            if col>=0:
                self.__p(f"{n}F").col(col)
            self.__p(f"{n}A")
        elif n==0:
            if col>=0: self.col(col)
        else:
            return self.down(-n, col=col)
        return self

    def down(self, n: int, col=-1):
        if n>0:
            if col>=0:
                self.__p(f"{n}E").col(col)
            self.__p(f"{n}B")
        elif n == 0:
            if col>=0: self.col(col)
        else:
            return self.up(-n,col)
        return self

    def __lt__(self, n: int):
        return self.left(n)

    def __lshift__(self, n: int):
        return self.left(n)

    def left(self, n: int):
        if n == 0:
            return self
        return self.__p(f"{n}D") if n >= 0 else self.right(-n)

    def __gt__(self, n: int):
        return self.right(n)

    def __rshift__(self, n: int):
        return self.right(n)

    def right(self, n: int):
        if n == 0:
            return self
        return self.__p(f"{n}C") if n >= 0 else self.left(-n)

    def __getitem__(self, key:Union[tuple,int]):
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            return self.loc(row, col)
        elif isinstance(key, int):
            return self.loc(key, 0) # col的默认值0、1对原始终端无影响，但对自己设定的origin有影响
        else:
            raise TypeError("Location index must be row, col.")

    # 绝对定位
    def loc(self, row: int, col=0):
        """
        ### 光标定位到 row,col\n
        - col: 0 by default
        - 左上角为 1,1
        - 自动添加set_origin设置的新坐标原点
        """
        row += self.origin_row
        col += self.origin_col
        return self.__p(f"{row};{col}H")
    
    def col(self, n: int):
        n += self.origin_col
        return self.__p(f"{n}G")
    
    def gotoHead(self):
        """回到本行行首（基于坐标原点）"""
        return self.col(0)

    # 光标相关
    def saveCursor(self):
        return self.__p("s")

    def restoreCursor(self):
        return self.__p("u")

    def hideCursor(self):
        return self.__p("?25l")

    def showCursor(self):
        return self.__p("?25h")

    # 其他效果（可能没啥效果）
    def bold(self, *args):
        return self.__p("1m", *args)

    def dim(self, *args):
        return self.__p("2m", *args)
    
    def italics(self, *args):
        return self.__p("3m", *args)

    def underline(self, *args):
        return self.__p("4m", *args)

    def blink(self, *args):
        return self.__p("5m", *args)

    def blinking(self, *args):
        return self.__p("6m", *args)
    
    def invert(self, *args):
        return self.__p("7m", *args)
    
    def invisible(self, *args):
        return self.__p("8m", *args)
    
    def strike(self, *args):
        return self.__p("9m", *args)

    # 控制台自带颜色
    def fg_black(self, *args):
        return self.__p("30m", *args)

    def bg_black(self, *args):
        return self.__p("40m", *args)

    def fg_red(self, *args):
        return self.__p("31m", *args)

    def bg_red(self, *args):
        return self.__p("41m", *args)

    def fg_green(self, *args):
        return self.__p("32m", *args)

    def bg_green(self, *args):
        return self.__p("42m", *args)

    def fg_yellow(self, *args):
        return self.__p("33m", *args)

    def bg_yellow(self, *args):
        return self.__p("43m", *args)

    def fg_blue(self, *args):
        return self.__p("34m", *args)

    def bg_blue(self, *args):
        return self.__p("44m", *args)

    def fg_magenta(self, *args):
        return self.__p("35m", *args)

    def bg_magenta(self, *args):
        return self.__p("45m", *args)

    def fg_cyan(self, *args):
        return self.__p("36m", *args)

    def bg_cyan(self, *args):
        return self.__p("46m", *args)

    def fg_grey(self, *args):
        return self.__p("37m", *args)

    def bg_grey(self, *args):
        return self.__p("47m", *args)

    # 任意颜色
    def fg_rgb(self, rgb: Union[list, tuple], bg: Union[bool, int] = False):
        """
        ### 设置前景文字rgb颜色
        rgb: [0,128,255]
        """
        rgb_err_info = "Argument rgb needs a list or a tuple, len=3, value between 0~255"
        if not rgb.__len__:
            raise TypeError(rgb_err_info)
        if len(rgb) != 3:
            raise ValueError(rgb_err_info)
        bf = '4' if bg else '3'
        return self.__p(f"{bf}8;2;{rgb[0]};{rgb[1]};{rgb[2]}m")

    def bg_rgb(self, rgb: Union[list, tuple]):
        """
        ### 设置背景rgb颜色
        rgb: [0,128,255]
        """
        return self.fg_rgb(rgb, 1)

    def fg_hex(self, hex: str, bg: Union[bool, int] = False):
        """
        ### 设置前景文字hex颜色
        hex: 0F0, #CCF, 008AFF, #CCCCFF
        """
        if hex[0] == "#":
            hex = hex[1:]
        hexes = []
        if len(hex) == 6:
            hexes = [hex[:2], hex[2:4], hex[4:]]
        elif len(hex) == 3:
            hexes = [hex[:1] * 2, hex[1:2] * 2, hex[2:] * 2]
        else:
            raise ValueError("Hex color should be like #F0F or #00FFFF")
        rgb = [int(i, 16) for i in hexes]
        return self.fg_rgb(rgb, bg)

    def bg_hex(self, hex: str):
        """
        ### 设置背景hex颜色
        hex: 0F0, #CCF, 008AFF, #CCCCFF
        """
        return self.fg_hex(hex, 1)
    
    def __str__(self):
        s = self.str
        self.str = ''
        return s

    def makeStyle(self,fg_color: Union[list, tuple, str]="", bg_color: Union[list, tuple, str]="",bold=False, italics=False, undefline=False, strike=False)->Style:
        """
        ### 生成Style样式类
        #### 参数
        - fg_color: 前景色，可rgb、hex
        - bg_color: 前景色，可rgb、hex
        - bold: bool=False 是否加粗
        - italics: bool=False 是否斜体
        - underline: bool=False 是否下划线
        - strike: bool=False 是否删除线
        #### 参数无有效样式时使用前面积累的self.str作为样式
        """
        sty = self.CSI
        if bold: sty+='1;'
        if italics: sty+='3;'
        if undefline: sty+='4;'
        if strike: sty += '9;'
        if sty != self.CSI:
            sty = sty[:-1]+'m'
        else: sty = ''
        if fg_color:
            if type(fg_color)==str:
                self.fg_hex(fg_color)
            elif type(fg_color)==list or type(fg_color)==tuple:
                self.fg_rgb(fg_color)
            sty+=self.str
        if bg_color:
            if type(bg_color)==str:
                self.bg_hex(bg_color)
            elif type(bg_color)==list or type(bg_color)==tuple:
                self.bg_rgb(bg_color)
            sty+=self.str
        if not sty:
            sty = re.sub(r'\033\[0m','',self.str) # 没有参数，则使用前面已写入的样式，头部自带reset
        self.reset()
        return Style(sty)
    
    def use(self, style: Style):
        """使用Style样式"""
        print(str(style), end="")
        return self

    def getsize(self):
        """返回终端大小（rows，columns）"""
        try:
            size = get_terminal_size()
            self.size_col = columns = size.columns
            self.size_row = rows = size.lines
        except OSError:
            return 30, 120
        return rows, columns

    def goto_center_offset(self, len_str: int):
        """ 光标到基于原点、使所给文本长度居中的 offset 位置 """
        width = self.width or self.size_col
        if len_str >= width:
            offset = 0
        else:
            offset = (width - len_str) // 2
        if self.width!=self.size_col:
            offset+=1 # 在新的origin中，第0列被|占据
        return self.col(offset)
    
    def alignCenter(self, s:str):
        """ 使文本居中对齐显示 """
        return self.goto_center_offset(self.get_string_width(s))(s)
    
    def alignRight(self, s:str, col=-1):
        """
        ### 使文本右对齐
        - col: -1: 默认方形最右侧对齐，其他：不占用该格，前一格处右对齐 """
        if col>0: col+=self.origin_col
        else: col = self.origin_col+self.width+1
        offset = col-self.get_string_width(s)
        if offset<0: offset=0
        return self.col(offset)(s)

    def get_string_width(self, s:str):
        """ 返回字符串去除CSI转义序列、\n、\t后的显示长度 """
        raw = re.sub(r'\033\[[\d;\?]*\w', '', s) # 去除csi转义序列
        raw = re.sub(r'[\n\t]', '', raw)
        return sum(2 if east_asian_width(c) in ('F', 'W', 'A') else 1 for c in raw)

    def set_origin(self, row: int, col: int, width=0, height=0, base = 0):
        """
        ### 设定新的坐标原点与宽高
        - width, height：未设定则使用终端剩余所有大小
        - base: 0基于Terminal左上角，1基于当前origin位置
        """
        if base:
            row += self.origin_row
            col += self.origin_col
        if row + height >= self.size_row and col + width >= self.size_col:
            raise ValueError("Given size is bigger than terminal size!")
        self.origin_row = row
        self.origin_col = col
        self.width = width or self.size_col - self.origin_col
        self.height = height or self.size_row - self.origin_row
        return self

    def set_origin_zero(self):
        """回复终端左上角位置为原点"""
        self.origin_row = 0
        self.origin_col = 0
        self.getsize()
        self.width = self.size_col
        self.height = self.size_row

    def hline(self, row: int, col: int, length: int, mark="─"):
        """在给定位置生成给定长度的**横线**"""
        self[row, col] >= mark * length
        return self

    def vline(self, row: int, col: int, length: int, mark="│"):
        """在给定位置生成给定长度的**竖线**"""
        for i in range(length):
            self[row + i, col] >= mark
        return self

    def rectangle(self, row: int, col: int, width: int, height: int, as_origin=True):
        """ 产生一个方形，并设定新的坐标原点 """
        if as_origin:
            self.set_origin(row, col, width, height)
            row = col = 0
        self[row, col] >= "┌"
        self.hline(row, col + 1, width) >= "┐"
        self.vline(row + 1, col, height).vline(row + 1, col + width + 1, height)
        self[row + height + 1, col] >= "└"
        self.hline(row + height + 1, col + 1, width)
        self[row + height + 1, col + width + 1] >= "┘"
        if self.auto_reset: self.reset()
        return self[1,1]
    

    def __enter__(self):
        self._in_chain = True
        self.__auto_reset = self.auto_reset
        self.auto_reset_off()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._in_chain = False
        self.reset()
        if self.__auto_reset:
            self.auto_reset_on()
        return True

    # 日志记录
    # def log(self):
    #     pass

    def test(self):
        """测试终端能显示的指令\033[0-99m"""
        n=0
        for i in range(10):
            for j in range(10):
                n = (10 * i) + j;
                print("\033[%dm  %3d  \033[0m"%(n, n),end='')
            print()


prt = Output()

def NbCmdIO():
    # 清屏并设置终端标题
    prt.cls().setTitle('NbCmdIO')
    prt[2].fg_yellow().bg_hex("#ccf").alignCenter(" NbCmdIO by Cipen version "+prt.__version__+' ')
    Width = 40
    Height = 10
    centerOffset = (prt.size_col - Width) // 2
    # 设定新区域
    prt.fg_hex('#CCF').rectangle(3, centerOffset, Width, Height)
    b2 = '  '
    # 进入prt上下文（关闭自动重置样式），在区域的4个角添加方形色块
    with prt.bg_hex('#ccf'):
        prt[1,1](b2)[1,Width-1](b2)
        prt[Height,1](b2)[Height,Width-1](b2)
    # 字符串内添加样式
    line1 = f"Welcome to {prt.bold().bg_hex('#ccf').fg_hex('#000')} NbCmdIO "
    line2 = "Print your string colorfully!"
    line3 = "-"*(Width-2)
    # 保存并使用样式
    headStyle = prt.fg_red().bold().makeStyle()
    prt[1].use(headStyle).alignCenter(line1) # 在新区域第一行使用样式居中显示文本
    prt[2].use(headStyle).alignCenter(line2)
    prt[3].use(headStyle).alignCenter(line3)
    
    text = """
 _____    _____    _______ 
|  _  \  |  _  \  |__   __|
| |__) | | |__) |    | |   
|  __ /  |  _  <     | |   
| |      | | \ \     | |   
|_|      |_|  \_\    |_|   """[1:]
    lines = text.splitlines()
    prt.set_origin(4,8,base=1)
    with prt.fg_red().bold()[0,0]:
        for i in range(len(lines)):
            prt[i](lines[i][:8])
        
    prt.set_origin(prt.origin_row,prt.origin_col+8)
    with prt.fg_green().bold()[0,0]:
        for i in range(len(lines)):
            prt[i](lines[i][8:18])
    
    prt.set_origin(prt.origin_row,prt.origin_col+9)
    with prt.fg_blue().bold()[0,0]:
        for i in range(len(lines)):
            prt[i](lines[i][18:])
    # 跳至最后一行并结束
    prt[Height].end().reset()
    # prt.set_origin_zero()
    # prt.hideCursor()
    # from random import randint
    # from time import sleep
    # try:
    #     while True:
    #         prt.getsize()
    #         w = prt.size_col
    #         h = prt.size_row
    #         prt[randint(0,h),randint(0,w-1)].bg_rgb([randint(0,255), randint(0,255),randint(0,255)])(b2)
    #         sleep(0.5)
    # except:
    #     prt[h].end().reset()

if __name__ == "__main__":
    NbCmdIO()
