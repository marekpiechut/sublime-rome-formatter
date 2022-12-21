# Rome formatter integration for SublimeText 3 and 4
This repository contains SublimeText 3/4 plugin for 🏛️ [Rome](https://rome.tools) code formatter.

Why you would want to use it? Because Prettier integration in Sublime is slooow and this one is **Blazing fast ™️** 🏎️.

It will honor settings inside `rome.conf` file, if it finds it.

## How it works
There are 3 ways you can use it:

### Newbie way
Open `Edit` menu and select `Format with Rome`. This will format current selection, or whole file if nothing is selected.

### Pro way
Open command palette, type `Rome` and select `Rome: Format file or selection`. This will also format current selection, or whole file if nothing is selected.

### Master way
Just enable `format_on_save` option and let Rome format every file it can.

## Configuration
Check out `Settings...` -> `Package Settings` -> `Rome Formatter`:
```jsonc
{
	// Should we format supported files on save
	"format_on_save": false,
	// Format on save only if rome.conf file was detected
	"detect_config": true
}
```

**detect_config** will traverse up from current file or folder and try to find `rome.json` file. If it finds it, it will allow **format_on_save** to do it's job. If not, meh, nothing will happen.


## Keyboard shortcut
You can add a keyboard shortcut in your keymap, ex:
```jsonc
[
	{"keys": ["ctrl+alt+f"], "command": "rome_format"}
]
```

## Installation via Package Control
Open Sublime menu and navigate to :

`Tools` -> `Command Palette...` -> `Package Control: Install Package`,
type `Rome Formatter` and select it to complete the installation.

## Requirements
Plugin itself has no dependencies, but **you need to have Rome** installed:

- Install Rome globally via:

```bash
npm i -g rome
```

- or locally in your project (**recommended**):

```bash
npm i -D rome
```

plugin will auto-detect if there's a local binary and use that and fallback
to global install if nothing was found. So **you can have different Rome versions** for each project.