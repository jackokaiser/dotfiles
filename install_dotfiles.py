#!/usr/bin/python3

import subprocess
import argparse
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

parser = argparse.ArgumentParser()
parser.add_argument('--all', help='install all dependencies', action='store_true')
parser.add_argument('--apt', help='install apt packages', action='store_true')
parser.add_argument('--ohmyzsh', help='install oh_my_zsh', action='store_true')
args = parser.parse_args()
yes = '-y'

additional_ppa = [
    'ppa:ubuntu-elisp/ppa'
]

apt_packages = [
    'emacs-snapshot',
    'curl',
    'fzf',
    'git',
    'zsh',
    'stow',
    'python3-pip',
    'virtualenvwrapper'
]

default_conf = {
    'root': False,
    'version': 'master',
    'target': os.path.expanduser('~')
}

normalize_dotfiles = lambda all_conf: [ {**default_conf, **conf} for conf in all_conf ]

dotfiles = normalize_dotfiles([
    {
        'name': '.emacs.d',
        'url': 'git@github.com:jackokaiser/emacs.d.git',
        'root': True
    },
    {
        'name': '.xmonad',
        'url': 'git@github.com:jackokaiser/xmonad-ubuntu-conf.git',
        'root': True
    },
    {
        'name': 'dot_profiles',
        'url': 'git@github.com:jackokaiser/dot_profiles.git',
    },
    {
        'name': 'dot_config',
        'url': 'git@github.com:jackokaiser/dot_config.git',
        'target': os.path.expanduser('~/.config')
    }
])

def install_ppas(all_ppas):
    print("installing ppas {}".format(all_ppas))
    for ppa in all_ppas:
        # first remove ppa to not install it twice
        subprocess.run(['sudo', 'add-apt-repository', '-r', ppa, yes])
        subprocess.run(['sudo', 'add-apt-repository', ppa, yes])

def install_apt_packages(all_pkg):
    print("installing apt packages {}".format(all_pkg))
    subprocess.run(['sudo', 'apt', 'install', *apt_packages, yes])

def install_oh_my_zsh():
    subprocess.run(['curl', '-Lo', '/tmp/install_oh_my_zsh.sh', 'https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh'])
    subprocess.run(['sh', '/tmp/install_oh_my_zsh.sh'])

def clone_if_needed(url, path):
    if not os.path.exists(path):
        subprocess.run(['git', 'clone', url, path])

def stow_dotfiles(all_dotfiles):
    os.chdir('stow')
    for dotfiles in all_dotfiles:
        print("stowing {} to target {}".format(dotfiles['name'], dotfiles['target']))

        if dotfiles['root']:
            os.makedirs(dotfiles['name'], exist_ok=True)
            clone_if_needed(dotfiles['url'], os.path.join(dotfiles['name'], dotfiles['name']))
        else:
            clone_if_needed(dotfiles['url'], dotfiles['name'])
        stow_res = subprocess.run(['stow', dotfiles['name'], '-t', dotfiles['target']])
    os.chdir(SCRIPT_DIR)

def main():
    if args.all or args.apt:
        install_ppas(additional_ppa)
        subprocess.run(['sudo', 'apt-get', 'update', yes])
        install_apt_packages(apt_packages)
    if args.all or args.ohmyzsh:
        install_oh_my_zsh()
    stow_dotfiles(dotfiles)

if __name__ == "__main__":
    # execute only if run as a script
    main()
