# stdlib
import os
import subprocess
from pathlib import Path

# this package
from textual_wrapper.wrapper import Wrapper


class MyWrapper(Wrapper):
	"""
	Example of subclassing the dynamic wrapper class.
	"""

	def run(self, working_directory: str | Path | os.PathLike | None = None) -> None:
		"""
		Launch the wrapper.

		:param working_directory: Directory to execute the application in.
		"""

		subprocess.run(["gnome-terminal", "--", *self.arguments])
