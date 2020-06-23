# i3-cheat

To run i3-cheat your i3 config will need to be inside `~/.config/i3/config` and will need to be marked like below

```
set $TerminalEmulator kitty

## Category: Applications;
# Description: Launch $TerminalEmulator;
$super_b+Return \
  $exe $TerminalEmulator;focus
$super_b+KP_Enter \
  $exe $TerminalEmulator;focus

```

## My config

[Download](https://raw.githubusercontent.com/TheCynicalTeam/DotFiles/master/.config/i3/config)

### i3-cheat config
`~/.config/i3-cheat/settings.conf`
```
[settings]
commands=False
```
