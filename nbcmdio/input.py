
from platform import system as getOS
import time

os = getOS()
if os=="Windows":
    import msvcrt
elif os=="Linux":
    import termios

class Input:
    WIN_KEY_MAP = {
        8: "BackSpace",
        9: "Tab",
        13: "Enter",
        27: "Esc",
        59: "F1",
        60: "F2",
        61: "F3",
        62: "F4",
        63: "F5",
        64: "F6",
        65: "F7",
        66: "F8",
        67: "F9",
        68: "F10",
        71: "Home",
        72: "ArrowUp",
        73: "PageUp",
        77: "ArrowRight",
        75: "ArrowLeft",
        80: "ArrowDown",
        81: "PageDown",
        82: "Insert",
        83: "Delete",
        133: "F11",
        134: "F12",
    }
    def __init__(self) -> None:
        self.os = getOS()
    def win_get_key(self, timeout=0.1):
        start_time = time.time()
        key = None

        # 等待按键或超时
        while (time.time() - start_time) < timeout:
            if msvcrt.kbhit():
                first_byte = msvcrt.getch()
                # 检查是否为扩展键（功能键）
                if first_byte in (b'\xe0', b'\x00'):
                    if msvcrt.kbhit():
                        second_byte = msvcrt.getch()
                        key = self.WIN_KEY_MAP.get(ord(second_byte), f'Unknown Key: {ord(second_byte)}')
                    else:
                        key = str(first_byte)
                else:
                    o = ord(first_byte)
                    key = self.WIN_KEY_MAP.get(o,None) if o<=31 else first_byte.decode()
                break
            time.sleep(0.01)  # 减少 CPU 占用

        return key

inp = Input()