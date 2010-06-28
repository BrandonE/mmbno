#!/usr/bin/env python
from distutils.core import setup
import os

script_file = 'mmbno.py'

data_files = []
for file in os.listdir('mmbno'):
    file = os.path.join('mmbno', file)
    if os.path.exists(file):
        data_files.append(file)

setup_args = dict(
    data_files=[('mmbno', data_files)]
)

try:
    import py2exe
    setup_args.update(dict(
        windows=[dict(
            script=script_file,
            icon_resources=[(1, 'res/icon.ico')],
        )],
    ))
except ImportError:
    pass

try:
    import py2app
    setup_args.update(dict(
        app = [script_file],
        options=dict(py2app=dict(
            argv_emulation=True,
            iconfile='res/icon.icns',
        )),
    ))
except ImportError:
    pass

setup(**setup_args)
