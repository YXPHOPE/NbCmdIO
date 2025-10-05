import sys
import re
from inspect import signature
from typing import Callable, Dict, List, Any
from .output import prt, NbCmdIO

re_int = re.compile(r'^-?\d+$')
re_float = re.compile(r'^-?\d+\.\d+$')
re_keyword = re.compile(r'^([a-zA-Z_]\w{0,12})=(.*)$') # 默认参数名不超过13个字符


# 可用函数字典
FUNCTIONS: Dict[object, list[str]] = {
    prt: [
    "setTitle",
    "cls",
    "print",
    "reset",
    "end",
    "loc",
    "col",
    "getLoc",
    "hideCursor",
    "showCursor",
    "bold",
    "dim",
    "italics",
    "underline",
    "blink",
    "invert",
    "strike",
    "fg_black",
    "bg_black",
    "fg_red",
    "bg_red",
    "fg_green",
    "bg_green",
    "fg_yellow",
    "bg_yellow",
    "fg_blue",
    "bg_blue",
    "fg_magenta",
    "bg_magenta",
    "fg_cyan",
    "bg_cyan",
    "fg_grey",
    "bg_grey",
    "fg_rgb",
    "bg_rgb",
    "fg_hex",
    "bg_hex",
    "getSize",
    "alignCenter",
    "alignRight",
    "setOrigin",
    "setOriginTerm",
    "drawNL",
    "drawHLine",
    "drawVLine",
    "drawRect",
    "printLines",
    "drawHGrad",
    "drawVGrad",
    "drawImage",
    "drawImageStr",
    "playGif",
    "clearRegion",
    "test"]
}
AllFun = []


def get_fun(func:str) -> Callable:
    for obj in FUNCTIONS:
        if func in FUNCTIONS[obj]:
            return getattr(obj, func)
    return lambda : None

def list_functions():
    prt.bold().fg_hex('cff')("Functions:\n\n")
    sty_name = prt.bold().fg_hex('6f6').makeStyle()
    sty_args = prt.reset().fg_hex('ccf').makeStyle()
    for obj in FUNCTIONS:
        funs = '\n'.join([f'    {sty_name}{i}{sty_args}{str(signature(get_fun(i)))}\n' for i in FUNCTIONS[obj]])
        prt(funs).drawNL()
    prt("For detailed information about function, type:\n\n").col(5).bold().fg_yellow("help <function>\n").end()

def help_function(func=None):
    if func==None:
        prt.bold().drawHGrad((220,110,80),(80, 150, 230), string=f"  NbCmdIO({prt.__version__}) prt cli.  ").drawNL()
        prt.bold("Usage")(": prt func1 args func2 args...\n")
        prt("Example:\n\n")
        prt.col(4)("prt loc 3 4 drawImage filepath\n")
        prt.col(4)('prt fg_hex "#ccf" bold "text"\n\n')
        prt.bold().fg_yellow("prt list")(": list all available functions\n")
        prt.bold().fg_yellow("prt help <function>")(": get help information of function\n").end()
        return
    fun = get_fun(func)
    prt("Function ").bold().fg_yellow(func)(":\n")
    prt.col(5).bold().fg_hex('6f6')(func)(str(signature(fun))).drawNL()
    prt.col(7)(fun.__doc__).drawNL().end()

def parse_value(arg):
    if re_int.match(arg):
        return int(arg)
    elif re_float.match(arg):
        return float(arg)
    elif arg in ("True", "true"):
        return True
    elif arg in ("False", "false"):
        return False
    else:
        return arg

def parse_args(args: List[str], params):
    """解析参数列表为参数字典"""
    pos_args = []
    key_args = {}
    for arg in args:
        if m := re_keyword.match(arg):
            key, value = m[1], m[2]
            if key in params:
                key_args[key] = parse_value(value)  # 去除字符串的引号
            else:
                raise NameError(f"Unknown parameter: {key}")
        else:
            pos_args.append(parse_value(arg))
    return pos_args, key_args


def call_function(func_name: str, args: List[str]) -> None:
    """调用指定函数"""
    func = get_fun(func_name)
    sig = signature(func)
    params = sig.parameters
    
    pos_args, key_args = parse_args(args, params.keys())
    
    func(*pos_args, **key_args)

def parse_cmd_argv(argv):
    l = len(argv)
    fun = argv[0]
    args = []
    funs = []
    for i in range(1, l):
        if argv[i] in AllFun:
            funs.append((fun, args))
            fun = argv[i]
            args = []
        else:
            args.append(argv[i])
    funs.append((fun, args))
    return funs

def cli():
    """主函数，处理命令行参数"""
    argv = sys.argv[1:]
    if not argv:
        NbCmdIO()
        help_function()
        return
    
    for obj in FUNCTIONS:
        AllFun.extend(FUNCTIONS[obj])
    
    if argv[0] in ("-h", "--help", "help", "/h", "/?"):
        if len(argv)>1:
            if argv[1] in AllFun:
                help_function(argv[1])
            else:
                prt("Unknown function: ").fg_red(argv[1])
        else:
            help_function()
        return
    elif argv[0] in ("-l", "--list", "list"):
        list_functions()
        return
    
    funs = parse_cmd_argv(argv)
    try:
        for fun, args in funs:
            call_function(fun, args)
    except Exception as e:
        print(f"{fun}: {str(e)}")

if __name__ == "__main__":
    cli()