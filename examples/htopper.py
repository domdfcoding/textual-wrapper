"""
Example wrapping htop.
"""

# stdlib
import shutil

# this package
from textual_wrapper.keycodes import F1
from textual_wrapper.wrapper.gtk import MenuOption, WrapperGtk

w = WrapperGtk(
		"htopper",
		[shutil.which("htop")],
		"/usr/share/icons/gnome/128x128/apps/libreoffice-base.png",
		menu_options={"_File": [MenuOption("_Help", F1)]},
		)

w.run()
