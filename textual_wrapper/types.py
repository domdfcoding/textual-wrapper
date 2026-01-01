#!/usr/bin/env python3
#
#  types.py
"""
Base classes for the wrapper.
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
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

__all__ = ["MenuOption", "Wrapper"]


class MenuOption(NamedTuple):
	"""
	An option in the menubar or the right click menu of the launcher/taskbar icon.
	"""

	#: Label for the option.
	label: str

	#: The keypress(es) to send to the terminal app.
	keypress: str


@dataclass
class Wrapper(ABC):
	"""
	A wrapper around a terminal app.
	"""

	#: The name of the application.
	name: str

	#: The executable and command line arguments.
	arguments: list[str]

	#: Optional icon filename.
	icon: str | None = None

	#: List of right click options for the launcher/taskbar icon.
	launcher_options: list[MenuOption] = field(default_factory=list)

	#: Options for the menubar.
	menu_options: dict[str, list[MenuOption]] = field(default_factory=dict)

	def add_launcher_option(self, option: MenuOption) -> None:
		"""
		Add an option to the launcher/taskbar icon.

		:param option:
		"""

		self.launcher_options.append(option)

	def add_menu_option(self, option: MenuOption, group: str = "File") -> None:
		"""
		Add an option to the menubar at the top of the window.

		:param option:
		:param group: The top level button, e.g. ``File``, ``Edit``, ``Help``.
		"""

		self.menu_options.setdefault(group, []).append(option)

	@abstractmethod
	def run(self, working_directory: str | Path | os.PathLike | None = None) -> None:
		"""
		Launch the wrapper.

		:param working_directory: Directory to execute the application in.
		"""

		raise NotImplementedError
