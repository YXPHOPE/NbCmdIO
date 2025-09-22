
class Style:
    RESET = '\033[0m'
    def __init__(self, style: str) -> None:
        self.style = style
    def __str__(self) -> str:
        return self.style
    def __add__(self, other):
        return self.style+other
    def __radd__(self, other):
        return other+self.style
    def __call__(self, *args, **kwds):
        print(self.style,end="")
        print(*args,**kwds)
        print(self.RESET, end="")
    def reset(self):
        print(self.RESET,end="")


CSI = "\033["
RESET = Style(CSI + "0m")
BOLD = Style(CSI + "1m")
ITALICS = Style(CSI + "3m")
UNDERLINE = Style(CSI + "4m")
BLINK = Style(CSI + "5m")
VERSE = Style(CSI + "7m")
STRIKE = Style(CSI + "9m")
FG_BLACK = Style(CSI + "30m")
BG_BLACK = Style(CSI + "40m")
FG_RED = Style(CSI + "31m")
BG_RED = Style(CSI + "41m")
FG_GREEN = Style(CSI + "32m")
BG_GREEN = Style(CSI + "42m")
FG_YELLOW = Style(CSI + "33m")
BG_YELLOW = Style(CSI + "43m")
FG_BLUE = Style(CSI + "34m")
BG_BLUE = Style(CSI + "44m")
FG_MAGENTA = Style(CSI + "35m")
BG_MAGENTA = Style(CSI + "45m")
FG_CYAN = Style(CSI + "36m")
BG_CYAN = Style(CSI + "46m")
FG_WHITE = Style(CSI + "37m")
BG_WHITE = Style(CSI + "47m")
