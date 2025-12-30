#!/usr/bin/env python3
#
#  gtk.py
"""
GTK wrapper.

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
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

# 3rd party
import gi  # nodep
from domdf_python_tools.paths import PathPlus

# this package
from textual_wrapper.wrapper import MenuOption, Wrapper

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Vte", "2.91")  # vte-0.38 (gnome-3.14)
gi.require_version("Unity", "7.0")
gi.require_version("Dbusmenu", "0.4")

# 3rd party
from gi.repository import Dbusmenu, Gdk, Gio, GLib, Gtk, Unity, Vte  # nodep  # noqa: E402

__all__ = ["MainWindow", "Terminal", "WrapperGtk", "WrapperWindow"]


class Terminal(Vte.Terminal):
	"""
	Terminal widget for displaying a Textual app.
	"""

	can_use_sixel: bool = False

	@classmethod
	def new(cls) -> "Terminal":
		"""
		Create the terminal widget.
		"""

		self = cls()
		self.set_mouse_autohide(True)
		self.set_scroll_on_output(False)
		self.set_audible_bell(False)
		self.set_pty(self.pty_new_sync(Vte.PtyFlags.DEFAULT, None))
		self.set_word_char_exceptions("-,./?%&#:_")

		if hasattr(self, "set_enable_sixel"):
			self.set_enable_sixel(True)
			self.can_use_sixel = True

		return self

	def spawn_app(
			self,
			arguments: list[str],
			callback: Callable[["Terminal", int, Any], None] | None = None,
			) -> None:
		"""
		Launch the app in the terminal.

		:param arguments: The app executable and any arguments to pass to it.
		:param callback: Function to call when the app has launched, which is passed the terminal, the child process id, and any errors.
		"""

		terminal_pty = self.get_pty()
		fd = cast(Gio.Cancellable, Vte.Pty.get_fd(terminal_pty))

		env = ["TEXTUAL_WRAPPER=1", f"TEXTUAL_WRAPPER_PPID={os.getpid()}"]
		if self.can_use_sixel:
			env.append("TEXTUAL_WRAPPER_SIXEL=1")

		# Ensures they are ignored if set by the terminal we're invoked from
		env.extend(("COLUMNS=-1", "LINES=-1"))

		self.spawn_async(
				Vte.PtyFlags.DEFAULT,
				PathPlus(__file__).parent.parent.abspath().as_posix(),  # Working directory
				arguments,
				env,
				GLib.SpawnFlags.DO_NOT_REAP_CHILD,
				None,
				-1,
				fd,
				callback=callback,
				)


class MainWindow(Gtk.ScrolledWindow):
	"""
	The main window, containing the terminal widget.
	"""

	def __init__(self) -> None:
		super().__init__()

		self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.set_border_width(0)

	def add_widget(self, widget: Gtk.Widget) -> "MainWindow":
		"""
		Add a widget to the window.

		:param widget:
		"""

		Gtk.Container.add(self, widget)
		return self


class WrapperWindow(Gtk.Window):
	"""
	Standalone terminal wrapper for the app.

	Displays the app in a libVTE terminal window, like `gnome-terminal` but without the standard terminal functionality.
	Closes when the app exits.

	:param wrapper:
	"""

	def __init__(self, wrapper: Wrapper):
		Gtk.Window.__init__(self, title=wrapper.name)

		self.launcher_options: dict[str, bytes] = {
				mo.label: mo.keypress.encode("UTF-8")
				for mo in wrapper.launcher_options
				}
		self.menu_options: dict[Gtk.MenuItem, bytes] = {}

		self.terminal = Terminal.new()
		self.terminal.set_color_background(Gdk.RGBA(0.071, 0.071, 0.071, 1.0))
		# Matches background colour of default textual theme.

		menubar = self.create_menu_options(wrapper.menu_options)

		box = Gtk.HBox()
		self.add(box)
		box.pack_start(menubar, False, True, 0)
		box.add(MainWindow().add_widget(cast(Gtk.Widget, self.terminal)))

		char_width, char_height = self.terminal.get_char_width(), self.terminal.get_char_height()
		width, height = 805, 600
		width = (width // char_width) * char_width + 2
		height = (height // char_height) * char_height + 2

		self.set_default_size(width, height)
		self.set_border_width(0)
		self.set_wmclass(wrapper.name.lower(), wrapper.name)

		if wrapper.icon:
			self.set_icon_from_file(wrapper.icon)

	def spawn_callback(self, terminal: Vte.Terminal, pid: int, error: Any | None) -> None:
		"""
		Handler for the app finishing spawning.

		Sets up a watcher for the process later exiting.

		:param terminal:
		:param pid: Process ID of the Textual app.
		:param error:
		"""

		if error:
			print(f"{terminal=}")
			print(f"{pid=}")
			print(f"{error=}")

		terminal.watch_child(pid)
		terminal.connect("child_exited", self.on_child_exited)

	def on_menuitem_clicked(self, item: Gtk.MenuItem) -> None:
		"""
		Handler for menu buttons being clicked.

		:param item: The clicked item.
		"""

		keypress = self.menu_options[item]
		self.terminal.feed_child(keypress)

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

	def create_menu_options(self, menu_options: dict[str, list[MenuOption]]) -> Gtk.MenuBar:
		"""
		Create the menubar options.

		:param menu_options:
		"""

		menubar = Gtk.MenuBar()

		for option_group, group_items in menu_options.items():
			menuitem = Gtk.MenuItem.new_with_mnemonic(label=option_group)
			submenu = Gtk.Menu()

			for menu_option in group_items:
				submenuitem = Gtk.MenuItem.new_with_mnemonic(label=menu_option.label)
				self.menu_options[submenuitem] = menu_option.keypress.encode("UTF-8")
				submenuitem.connect("activate", self.on_menuitem_clicked)
				submenu.append(submenuitem)

			menuitem.set_submenu(submenu)
			menubar.append(menuitem)

		return menubar

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

	def on_child_exited(self, terminal: Vte.Terminal, status: int) -> None:
		"""
		Handler for the process running in the terminal exiting.

		Closes the wrapper window.

		:param terminal:
		:param status:
		"""

		# print(f"{terminal=}")
		# print(f"{status=}")
		sys.exit(status)

	def run(self, arguments: list[str]) -> None:
		"""
		Show the wrapper window and launch the Textual app.

		:param arguments: The app executable and any arguments to pass to it.
		"""

		self.terminal.spawn_app(arguments=arguments, callback=self.spawn_callback)
		self.connect("destroy", Gtk.main_quit)
		self.show_all()
		self.create_launcher_options()

		try:
			Gtk.main()
		except KeyboardInterrupt:
			sys.exit()


@dataclass
class WrapperGtk(Wrapper):
	"""
	A GTK3-based wrapper around a terminal app.
	"""

	def run(self) -> None:
		"""
		Launch the wrapper.
		"""

		window = WrapperWindow(self)
		window.run(self.arguments)
