#!/usr/bin/env python3

import json
import os
import re
import socket
import struct
import shutil
import Functions as fn
from pathlib import Path
import configparser

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gio, GLib, Gtk

variables = []
mapping = [ ('bindsym', ''), ('Mod1', 'Alt'), ('Mod4', 'Super')]
def do_replacements(line):
    for key, value in variables:
        line = line.replace(key, value)
    for k, v in mapping:
        line = line.replace(k, v)
    return line

def upsert_variable(key, value):
    new_var = (key, value)
    for i, (k, _) in enumerate(variables):
        if len(key) > len(k):
            # insert before shorter keys, in case there is a prefix of this key
            variables.insert(i, new_var)
            return
        if key == k:
            # replace
            variables[i] = new_var
            return
    variables.append(new_var)

regex = r"\s*set (\$\S+)\s+(.+)"
regex2 = r"^## Category: ((.*\n){4})"

home = os.path.expanduser("~")
if os.path.isfile("/etc/bspwm-cheat.conf"):
    if os.path.isfile(home + "/.config/bspwn-cheat/settings.conf"):
        config = home + "/.config/bspwm-cheat/settings.conf"
    else:
        config = ''.join([str(Path(__file__).parents[3]), "/etc/bpswm-cheat.conf"])
    configFile = f"{home}/.config/sxhkd/sxhkdrc"
else:
    if os.path.isfile(home + "/.config/i3-cheat/settings.conf"):
        config = home + "/.config/i3-cheat/settings.conf"
    else:
        config = ''.join([str(Path(__file__).parents[3]), "/etc/i3-cheat.conf"])
    configFile = f"{home}/.config/i3/config"

parser = configparser.RawConfigParser()
parser.read(config)

if parser.has_section("settings"):
    if parser.has_option("settings", "config"):
        configFile = str(parser.get("settings", "config"))

if configFile.startswith('~'):
    configFile = configFile.replace('~',home)

filelines = ''

with open(f'{configFile}', mode='r') as inputfile:
    for line in inputfile:
        split_line = line.split(' ')
        if split_line[0] == "include":
            with open(split_line[1].replace("$HOME", f"{home}").rstrip("\n")) as f1:
               filelines += f1.read()
        else:
            filelines += line

matches = re.finditer(regex, filelines.rstrip("\n"), re.MULTILINE)
matches2 = re.finditer(regex2, filelines.rstrip("\n"), re.MULTILINE)

for num, match in enumerate(matches, start=1):
    if match.group():
        upsert_variable(match.group(1), match.group(2))
        continue

data = {}
category={}
for num, match in enumerate(matches2, start=1):
    lines = match.group(1).splitlines()

    str_category = do_replacements(lines[0].replace('## Category: ', '').replace(';', '').strip())
    str_description = do_replacements(lines[1].replace('# Description: ', '').replace(';', '').strip())
    str_keybind = do_replacements(lines[2].replace('\\', '').strip())
    str_command = do_replacements(lines[3].replace('\\', '').strip())
    # create category if not exist
    if str_category not in data:
        data[str_category] = {}
    category = data[str_category]

    # create description
    category[str_description] = {}
    category[str_description]['keybind'] = str_keybind
    category[str_description]['command'] = str_command

# with open('./json/keybinds.json', 'w') as json_data:
#     json.dump(data, json_data, indent=4)

def mode_label(mode):
    'Create a GTK label for mode'''
    label = Gtk.Label()
    label.set_text(str(mode))
    return label

class WMCheatWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tab_lookup = dict()
        self.set_default_size(-1, 740)
        self.set_border_width(3)

        if not fn.os.path.isdir(fn.home + "/.config/i3-cheat"):
            fn.os.mkdir(fn.home + "/.config/i3-cheat")

        if not fn.os.path.isfile(fn.home + "/.config/i3-cheat/settings.conf"):
            shutil.copy(fn.root_config, fn.home + "/.config/i3-cheat/settings.conf")

        fn.get_config(self, fn.config)
        self.commands = self.commands

        accel_group = Gtk.AccelGroup()
        accel_group.connect(Gdk.keyval_from_name('Left'), Gdk.ModifierType.SUPER_MASK, 0, self.prev_mode)
        accel_group.connect(Gdk.keyval_from_name('Right'), Gdk.ModifierType.SUPER_MASK, 0, self.next_mode)
        accel_group.connect(Gdk.keyval_from_name('Escape'), 0, 0, self._quit)
        self.add_accel_group(accel_group)

        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        self.notebook = Gtk.Notebook(scrollable=True)
        for (category, array) in data.items():
            self.category = Gtk.Box()
            self.category.set_border_width(10)

            store = Gtk.ListStore(str, str, str, str)

            for description in array:
                keybind = array[description]['keybind']
                command = array[description]['command']
                store.append([category, str(description), str(keybind), str(command)])

            tree = Gtk.TreeView(model=store, headers_visible=True, enable_search=False, search_column=1)
            tree.get_selection().set_mode(Gtk.SelectionMode.BROWSE)
            tree.set_cursor(Gtk.TreePath(0), None, False)

            description_column = Gtk.TreeViewColumn("Description", Gtk.CellRendererText(), text=1)
            description_column.set_min_width(300)
            tree.append_column(description_column)

            keybind_column = Gtk.TreeViewColumn("Keybind", Gtk.CellRendererText(), text=2)
            keybind_column.set_min_width(300)
            tree.append_column(keybind_column)

            if self.commands:
                command_column = Gtk.TreeViewColumn("Command", Gtk.CellRendererText(), text=3)
                command_column.set_min_width(300)
                tree.append_column(command_column)

            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scrolled.add(tree)

            self._tab_lookup[category] = self.notebook.get_n_pages()
            self.notebook.append_page(scrolled, mode_label(category))

        self.add(self.notebook)
        self.current_page().grab_focus()

        style = Gtk.CssProvider()
        style.load_from_data(WMCheat.CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def current_page(self):
        return self.notebook.get_nth_page(self.notebook.get_current_page())

    def _init_mode(self, mode):
        store = Gtk.ListStore(str, str, str)

    def focus_mode(self, mode):
        'Focus on a mode by its name'
        idx = self._tab_lookup.get(mode, 0)
        self.notebook.set_current_page(idx)

    def next_mode(self, *args):
        self.notebook.next_page()

    def prev_mode(self, *args):
        self.notebook.prev_page()

    def _quit(self, *args):
        self.close()

class WMCheat(Gtk.Application):
    CSS = b"""
        * {
            font-size: 16px;
        }
        @binding-set i3-binds {
            bind "slash" { "start-interactive-search" () };
            bind "j" { "move-cursor" (display-lines, 1) };
            bind "k" { "move-cursor" (display-lines, -1) };
        }
        GtkTreeView, treeview {
            -gtk-key-bindings: i3-binds;
        }
    """

    def __init__(self):
        super().__init__(application_id="com.github.The-Repo-Club.keybinds", flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.add_main_option('mode', ord('m'), 0, GLib.OptionArg.STRING, "Mode tab to open", "MODE")
        self._window = None

    def do_command_line(self, cl):
        if not self._window:
            self._window = WMCheatWindow(application=self, title="Window Manager Cheatsheet")
            self._window.show_all()

        mode = cl.get_options_dict().lookup_value('mode')
        if mode:
            mode = mode.get_string()
            self._window.focus_mode(mode)
        self._window.present()
        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)

if __name__ == '__main__':
    import sys
    import signal
    app = WMCheat()
    # so ctrl+c still works
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, app.quit)
    app.run(sys.argv)
