# NbCmdIO: 终端色彩与交互的革命者⌨️

![Terminal Art](./assets/NbCmdIO.png)

**NbCmdIO** 是一个强大的Python库，将普通的命令行终端转变为充满活力的视觉画布和强大的交互平台！告别单调的黑白输出，迎接RGB真彩世界；告别笨重的文本界面，迎接精准的光标控制和输入捕获能力。

## 🌟 核心功能亮点

### ⚡ 支持链式调用
- 随时随地，设置光标位置、样式，方便快捷、清晰易读！ `prt[row, col].bold("text")`

### 🎨 真彩RGB终端着色
- 支持以RGB、HEX格式设定前景色、背景色
- 支持默认颜色：Black、Red、Green等
- 支持Bold、Underline、Italics等效果

### 🖱️ 像素级光标控制
- 精确到字符的光标定位
- 保存/恢复光标位置

### 📦 动态区域管理
- 创建独立更新区域
- 嵌套区域支持

### ⌨️ 输入捕获（路线图）
- 单键无缓冲读取
- 快捷键组合检测

## 🚀 快速入门

### 安装
```bash
pip install nbcmdio
```

### 基础使用
```python
from nbcmdio import prt

def NbCmdIO():
    lavender = "#ccf"
    # 清屏并设置终端标题
    prt.cls().setTitle('NbCmdIO')
    # 在第2行 以文字黄色 背景色#ccf  居中显示
    prt[2].fg_yellow().bg_hex(lavender).alignCenter(" NbCmdIO by Cipen ")
    Width = 40
    Height = 10
    centerOffset = (prt.size_col - Width) // 2
    # 以前景#CCF 在 3,centerOffset 处 绘制指定大小的方形，并默认设定新区域 为该方形
    prt.fg_hex(lavender)[3,centerOffset].rectangle(Width, Height)
    prt.fg_blue()[0,3](" NbCmdIO ").bold()[0,Width-8](prt.__version__)
    b2 = '  '
    # 进入上下文（里面不会自动重置样式），在区域的4个角添加方形色块
    with prt.bg_hex(lavender):
        prt[1,1](b2)[1,Width-1](b2)
        prt[Height,1](b2)[Height,Width-1](b2)
    # 字符串内添加样式
    line1 = f"Welcome to {prt.bold().bg_hex(lavender).fg_hex('#000')} NbCmdIO "
    line2 = "Print your string colorfully!"
    # 保存并使用样式
    headStyle = prt.fg_red().bold().makeStyle()
    prt[1].use(headStyle).alignCenter(line1) # 在新区域第一行使用样式居中显示文本
    prt[2].use(headStyle).alignCenter(line2)
    prt[3,3].hline(Width-4)
    
    text = r"""
 _____    _____    _______ 
|  _  \  |  _  \  |__   __|
| |__) | | |__) |    | |   
|  __ /  |  _  <     | |   
| |      | | \ \     | |   
|_|      |_|  \_\    |_|   """[1:]
    lines = text.splitlines()
    chr1 = [l[:8] for l in lines]
    chr2 = [l[8:18] for l in lines]
    chr3 = [l[18:] for l in lines]
    prt.fg_red().bold()[4, 8].printLinesInRegion(chr1)
    prt.fg_green().bold()[4, 16].printLinesInRegion(chr2)
    prt.fg_blue().bold()[4, 25].printLinesInRegion(chr3)

    # 光标跳至本区域下一行，结束
    prt[Height+1].end()

NbCmdIO()
```

## 🔮 未来路线图

| 版本 | 功能 | 状态 |
|------|------|------|
| v1.0 | RGB色彩支持、区域管理 | ✅ 已发布 |
| v2.0 | 输入捕获系统 |📅 规划中 |
| v3.0 | 终端UI组件库 |💡 构思中 |

## 🌍 社区贡献

我们欢迎各种形式的贡献！无论您是：
- 发现并报告问题
- 提交功能请求
- 贡献代码
- 创作文档
- 分享创意用例


## 📜 开源协议

NbCmdIO采用**MIT许可证** - 您可以自由地在商业和个人项目中使用它！


## ✨ 立即体验终端魔法！

```bash
pip install nbcmdio
```

准备好将您的命令行体验提升到全新维度了吗？NbCmdIO正在等待为您的终端注入生命！

---

[![PyPI Version](https://img.shields.io/pypi/v/nbcmdio)](https://pypi.org/project/nbcmdio/)
[![Downloads](https://img.shields.io/pypi/dm/nbcmdio)](https://pypi.org/project/nbcmdio/)
[![License](https://img.shields.io/pypi/l/nbcmdio)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/nbcmdio)](https://pypi.org/project/nbcmdio/)