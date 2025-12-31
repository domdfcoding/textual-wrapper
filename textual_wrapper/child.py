#!/usr/bin/env python3
#
#  child.py
"""
Helpers for child processes.
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

# stdlib
import os
from typing import NamedTuple

__all__ = ["ChildHelper"]


def _env_get_int(envvar: str, default: int = 0) -> int:
	try:
		return int(os.environ.get(envvar, default))
	except ValueError:
		return default


class ChildHelper(NamedTuple):
	"""
	Helpers for child processes.
	"""

	#: :py:obj:`True` if the app is running through the wrapper.
	is_wrapper: bool = False

	#: The PID of the wrapper parent process.
	parent_pid: int = -1

	#: Whether sixels are supported by the wrapper's terminal emulator.
	sixel_supported: bool = False

	@classmethod
	def new(cls) -> "ChildHelper":
		"""
		Create a new :class:`~.ChildHelper` with values set from environment variables.
		"""

		is_wrapper = False
		parent_pid = -1

		is_wrapper = bool(_env_get_int("TEXTUAL_WRAPPER", 0))
		sixel_supported = bool(_env_get_int("TEXTUAL_WRAPPER_SIXEL", 0))
		parent_pid = _env_get_int("TEXTUAL_WRAPPER_PID", -1)

		return cls(is_wrapper=is_wrapper, parent_pid=parent_pid, sixel_supported=sixel_supported)
