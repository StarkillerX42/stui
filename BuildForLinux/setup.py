#!/usr/bin/env python3
"""This script builds a runstui.spec file that can be sent to pyinstaller. It is
a system agnostic way to install STUI. This file takes one argument, a path to
RO, opscore, actorcore, and all the other essential libraries for STUI.
pyinstaller can use runstui.spec to build a version of STUI that doesn't require
a python interpreter. It's  possible that this will also speed up stui versus
using an interpreter, but that is untested. Check README.md for build
instructions.
"""

import sys
import os
from pathlib import Path
try:
    import RO
    import RO.OS
    import actorcore
    import actorkeys
    import opscore
    import plc
except ImportError as e:
    print('Failed to import a required STUI module:\n{}'.format(e))
    exit()

dependencies_paths = {RO: Path(RO.__file__).parent,
                      actorcore: Path(actorcore.__file__).parent,
                      actorkeys: Path(actorkeys.__file__).parent,
                      opscore: Path(opscore.__file__).parent,
                      plc: Path(plc.__file__).parent}

# Create useful paths
build_dir = Path(__file__).parent.absolute()
sys.path.append(str(build_dir))
repo = build_dir.parent
tui_dir = repo / 'TUI'
executable = repo / 'runstui.py'

data_added = []  # A list of tuples of files/directories to be added in install
# This is a place to look for non-python requirements, we need a relative path
# for them

data_added.append((str(tui_dir / 'Sounds/'), 'TUI/Sounds/'))
data_added.append((str(tui_dir / 'Scripts/'), 'TUI/Scripts/'))
data_added.append((str(tui_dir / 'Models/'), 'TUI/Models/'))

# print(sys.argv)
# Checks sys.argv for RO path
# try:
#     software_dir = Path(sys.argv[1])
# except IndexError:
#     raise Exception('Please provide a path to software (RO, opscore, actorcore'
#                     ' etc.)')

# try:
#     rel_software = software_dir.relative_to(build_dir)
# except ValueError:
#     levels_up = '..'
#     for parent in build_dir.parents:
#         print(parent)
#         try:
#             rel_software = software_dir.relative_to(parent)
#             break
#         except ValueError:
#             levels_up += '/..'
#     rel_software = levels_up / rel_software
# print(rel_software)

# Include all the necessary paths of non-python stuff (and a few pythons like
# cmds.py. Not sure why cmds.py isn't included normally, but I think it has to
# do with how it is imported using imp (in opscore/protocol/keys.py)
ro_dir = (dependencies_paths[RO]).absolute()
data_added.append((str(ro_dir), 'RO/'))
opscore_dir = (dependencies_paths[opscore]).absolute()
data_added.append((str(opscore_dir), 'opscore/'))
actorkeys_dir = (dependencies_paths[actorkeys]).absolute()
data_added.append((str(actorkeys_dir), 'actorkeys/'))
plc_dir = (dependencies_paths[plc]).absolute()
data_added.append((str(plc_dir), 'plc/'))
plc_root = dependencies_paths[plc].parent.parent.absolute()
data_added.append((str(plc_root), 'plc/'))

# Show paths to check for consistencies
print('\nPython Paths:')
for path in sys.path:
    print(path)
print('\nData Paths:')
for path in data_added:
    print(path[0])

# print(data_added)
spec_file = Path(repo/'BuildForLinux/runstui.spec').open('w')
spec_file.write('# -*- mode: python ; coding: utf-8 -*-\n\n')
spec_file.write('block_cipher = None\n\n\n')
spec_file.write("a = Analysis(['../runstui.py'],\n")
spec_file.write("             pathex={},\n".format(sys.path))
spec_file.write("             binaries=[],\n")
spec_file.write("             datas={},\n".format(data_added))
spec_file.write("             hiddenimports=[],\n")
spec_file.write("             hookspath=[],\n")
spec_file.write("             runtime_hooks=[],\n")
spec_file.write("             excludes=[],\n")
spec_file.write("             win_no_prefer_redirects=False,\n")
spec_file.write("             win_private_assemblies=False,\n")
spec_file.write("             cipher=block_cipher,\n")
spec_file.write("             noarchive=False)\n")
spec_file.write("pyz = PYZ(a.pure, a.zipped_data,\n")
spec_file.write("             cipher=block_cipher)\n")
spec_file.write("exe = EXE(pyz,\n")
spec_file.write("          a.scripts,\n")
spec_file.write("          [],\n")
spec_file.write("          exclude_binaries=True,\n")
spec_file.write("          name='runstui',\n")
spec_file.write("          debug=False,\n")
spec_file.write("          bootloader_ignore_signals=False,\n")
spec_file.write("          strip=False,\n")
spec_file.write("          upx=True,\n")
spec_file.write("          upx_exclude=[],\n")
spec_file.write("          runtime_tmpdir=None,\n")
spec_file.write("          console=True,\n")
if os.name == 'nt':  # icns files don't work on Windows
    spec_file.write("          icon='STUI.ico')\n")
else:
    spec_file.write("          icon='STUI.icns')\n")
spec_file.write("coll = COLLECT(exe,\n")
spec_file.write("               a.binaries,\n")
spec_file.write("               a.zipfiles,\n")
spec_file.write("               a.datas,\n")
spec_file.write("               strip=False,\n")
spec_file.write("               upx=True,\n")
spec_file.write("               upx_exclude=[],\n")
spec_file.write("               name='runstui')\n")
