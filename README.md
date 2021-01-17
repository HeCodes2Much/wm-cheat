# i3-cheat

To run i3-cheat your i3 config will need to be inside `~/.config/i3/config` and will need to be marked like below

**Note:** you may also change the config location using the config file settings also marked below

```
## Category:  Main Keybinds;
# Description: Kill a window;
Mod4 + Shift + c\
	kill
```

## My i3 config

[Download](https://raw.githubusercontent.com/TheCynicalTeam/DotFiles/master/.config/i3/config)

### i3-cheat config
`~/.config/i3-cheat/settings.conf`
```
[settings]
commands=False
config=~/.config/i3/config
```

# bspwm-cheat

To run bspwm-cheat your sxhkd config will need to be inside `~/.config/sxhkd/sxhkdrc` and will need to be marked like below

**Note:** you may also change the config location using the config file settings also marked below

```
## Category:  Main Keybinds;
# Description: Kill a window;
super + shift + c
	bspc node -c
```

**Sorry** but I do not have a bspwm config anymore

### bspwm-cheat config
`~/.config/bspwm-cheat/settings.conf`
```
[settings]
commands=False
config=~/.config/sxhkd/sxhkdrc
```
