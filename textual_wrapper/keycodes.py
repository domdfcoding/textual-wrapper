#!/usr/bin/env python3
#
#  keycodes.py
"""
Keycodes for F1-12 and Ctrl+A-Z.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

F1 = "\u001bOP"
F2 = "\u001bOQ"
F3 = "\u001bOR"
F4 = "\u001bOS"
F5 = "\u001b[15~"
F6 = "\u001b[17~"
F7 = "\u001b[18~"
F8 = "\u001b[19~"
F9 = "\u001b[20~"
F10 = "\u001b[21~"
F11 = "\u001b[23~"
F12 = "\u001b[24~"

CTRL_AT = '\x00'
CTRL_A = '\x01'
CTRL_B = '\x02'
CTRL_C = '\x03'
CTRL_D = '\x04'
CTRL_E = '\x05'
CTRL_F = '\x06'
CTRL_G = '\x07'
CTRL_H = '\x08'
CTRL_I = '\t'
CTRL_J = '\n'
CTRL_K = '\x0b'
CTRL_L = '\x0c'
CTRL_M = '\r'
CTRL_N = '\x0e'
CTRL_O = '\x0f'
CTRL_P = '\x10'
CTRL_Q = '\x11'
CTRL_R = '\x12'
CTRL_S = '\x13'
CTRL_T = '\x14'
CTRL_U = '\x15'
CTRL_V = '\x16'
CTRL_W = '\x17'
CTRL_Z = '\x18'
CTRL_Y = '\x19'
CTRL_Z = '\x1a'
CTRL_LSQ = ESC = '\x1b'
CTRL_BS = '\x1c'
CTRL_RSQ = '\x1d'
CTRL_CARET = '\x1e'
CTRL__ = '\x1f'

# TODO: Alt (starts 0x80)
