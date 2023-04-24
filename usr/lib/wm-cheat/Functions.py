# =====================================================
#                  Author The-Repo-Club
# =====================================================

import os
import sys
from pathlib import Path
import configparser

home = os.path.expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
if "--bspwn" in sys.argv:
    if os.path.isfile(home + "/.config/bspwn-cheat/settings.conf"):
        config = home + "/.config/bspwm-cheat/settings.conf"
    else:
        config = ''.join([str(Path(__file__).parents[3]), "/etc/bpswm-cheat.conf"])
    root_config = ''.join([str(Path(__file__).parents[3]), "/etc/bspwm-cheat.conf"])
elif "--i3" in sys.argv:
    if os.path.isfile(home + "/.config/i3-cheat/settings.conf"):
        config = home + "/.config/i3-cheat/settings.conf"
    else:
        config = ''.join([str(Path(__file__).parents[3]), "/etc/i3-cheat.conf"])
    root_config = ''.join([str(Path(__file__).parents[3]), "/etc/i3-cheat.conf"])
elif "--dk" in sys.argv:
    if os.path.isfile(home + "/.config/dk-cheat/settings.conf"):
        config = home + "/.config/dk-cheat/settings.conf"
    else:
        config = ''.join([str(Path(__file__).parents[3]), "/etc/dk-cheat.conf"])
    root_config = ''.join([str(Path(__file__).parents[3]), "/etc/dk-cheat.conf"])
else:
    if os.path.isfile(home + "/.config/i3-cheat/settings.conf"):
        config = home + "/.config/i3-cheat/settings.conf"
    else:
        config = ''.join([str(Path(__file__).parents[3]), "/etc/i3-cheat.conf"])
    root_config = ''.join([str(Path(__file__).parents[3]), "/etc/i3-cheat.conf"])


def _get_position(lists, value):
    data = [string for string in lists if value in string]
    position = lists.index(data[0])
    return position

def get_config(self, config):
    try:
        self.parser = configparser.RawConfigParser()
        self.parser.read(config)

        # Check if we're using HAL, and init it as required.
        if self.parser.has_section("settings"):
            if self.parser.has_option("settings", "commands"):
                self.commands = eval(self.parser.get("settings", "commands"))

    except Exception as e:
        print(e)
