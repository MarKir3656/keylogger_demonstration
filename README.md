# ⚠️ IMPORTANT: EDUCATIONAL PURPOSE ONLY ⚠️

> **This software is provided exclusively for educational and research purposes.**
> 
> By using this code, you acknowledge and agree to the following terms:

## 🚫 Prohibited Uses

This code **MUST NOT** be used for:

- Monitoring keystrokes on any system without explicit written permission from the owner
- Creating, distributing, or operating malicious software (malware)
- Violating any applicable local, state, national, or international laws
- Circumventing security measures or access controls
- Any activity that infringes upon privacy rights

## ✅ Permitted Uses

This code **MAY** be used for:

- Learning Windows API and low-level system programming
- Understanding how keyboard hooks work for defensive security research
- Developing detection methods and countermeasures (Blue Team)
- Educational demonstrations in controlled environments (your own computer)


## 🔒 Legal Compliance

- Unauthorized keystroke logging is **illegal** in most jurisdictions
- Violators may face **criminal prosecution** and **civil liability**
- The author assumes **no responsibility** for any misuse of this code
- You are **solely responsible** for complying with all applicable laws

# About keylogger-demo

This project shows how working global hooks of keyboard on Windows. It **does not save** any data
and is intended **for educational demonstration only**

## Demonstrations

| Technology | Description |
|------------|----------------|
| [ctypes](https://docs.python.org/3/library/ctypes.html) | Work with WinAPI |
| [SetWindowsHookExA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexa) | Setting of global hook WH_KEYBOARD_LL |
| [CallNextHookEx](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callnexthookex) | Passes the hook information to the next hook procedure in the current hook chain. |
| [ToUnicodeEx](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-tounicodeex) | Translates the specified virtual-key code and keyboard state to the corresponding Unicode character or characters. |
| [GetKeyboardLayout](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeyboardlayout) | Retrieves the active input locale identifier. |

## Install and run

### Requirements

- Windows 7/10/11
- Python 3.7+
- Administrator rights (for global hook)

[Downloading](https://github.com/MarKir3656/keylogger_demonstration/archive/refs/heads/main.zip) and unzip it.
Start from directory where you placed a project or from cmd:

```
python keylogger_demo.py
```

# Author 
[MarKir3656](https://github.com/MarKir3656) \
See my other projects.
