#!/usr/bin/env python3
#
#  unity.py
"""
GTK wrapper with Unity launcher support.

.. extras-require:: gtk
	:pyproject:
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
import sys
from dataclasses import dataclass

# 3rd party
import gi  # nodep

# this package
from textual_wrapper.wrapper import gtk

gi.require_version("Gtk", "3.0")
gi.require_version("Unity", "7.0")
gi.require_version("Dbusmenu", "0.4")

# 3rd party
from gi.repository import Gtk  # nodep  # noqa: E402
from gi.repository import Dbusmenu, Unity  # nodep  # noqa: E402

__all__ = ["WrapperUnity", "WrapperWindow"]


class WrapperWindow(gtk.WrapperWindow):
	"""
	Standalone terminal wrapper for the app.

	Displays the app in a libVTE terminal window, like `gnome-terminal` but without the standard terminal functionality.
	Closes when the app exits.

	:param wrapper:
	"""

	def on_launcher_menuitem_clicked(self, item: Dbusmenu.Menuitem, timestamp: int) -> None:
		"""
		Handler for a Unity Launcher rightclick menu item being clicked.

		:param item: The clicked item.
		:param timestamp:
		"""

		action = item.property_get(Dbusmenu.MENUITEM_PROP_LABEL)

		keypress = self.launcher_options[action]
		self.terminal.feed_child(keypress)
		# self.terminal.feed_child(b"\x10")  # Ctrl+p
		# self.terminal.feed_child(b"\x1b[21~")  # F10

	def create_launcher_options(self) -> None:
		"""
		Create the Unity launcher rightclick menu options.
		"""

		# TODO: gate on desktop file existing and us launching in way to use it (no spaces in install path)
		launcher = Unity.LauncherEntry.get_for_desktop_id("radioport.desktop")

		ql = Dbusmenu.Menuitem.new()

		for option in self.launcher_options:
			menuitem = Dbusmenu.Menuitem.new()
			menuitem.property_set(Dbusmenu.MENUITEM_PROP_LABEL, option)
			menuitem.property_set_bool(Dbusmenu.MENUITEM_PROP_VISIBLE, True)
			menuitem.connect(Dbusmenu.MENUITEM_SIGNAL_ITEM_ACTIVATED, self.on_launcher_menuitem_clicked)
			ql.child_append(menuitem)

		launcher.set_property("quicklist", ql)

	def run(
			self,
			arguments: list[str],
			working_directory: str,
			) -> None:
		"""
		Show the wrapper window and launch the Textual app.

		:param arguments: The app executable and any arguments to pass to it.
		:param working_directory: Directory to execute the application in.
		"""

		self.terminal.spawn_app(
				arguments=arguments,
				working_directory=working_directory,
				callback=self.spawn_callback,
				)
		self.connect("destroy", Gtk.main_quit)
		self.show_all()
		self.create_launcher_options()

		try:
			Gtk.main()
		except KeyboardInterrupt:
			sys.exit()


@dataclass
class WrapperUnity(gtk.WrapperGtk):
	"""
	A GTK3-based wrapper around a terminal app, with Unity launcher support.
	"""

	wrapper_window_cls = WrapperWindow
