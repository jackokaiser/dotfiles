# Master repo to manage my dotfiles

I use this repo to automatically setup a new linux machine with my config files.

## Installation

Use the `--all` option to install all dependencies alongside the dotfiles:
```bash
./install_dotfiles.py --all
```

This script will clone some of my dotfile repos and symlink them with `stow`.
