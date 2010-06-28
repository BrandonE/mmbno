import os
import shutil
from ConfigParser import ConfigParser

from pyglet import resource

settings_path = resource.get_settings_path('mmbnonline')
settings_file = os.path.join(settings_path, 'settings.ini')

if not os.path.exists(settings_file):
    src = os.path.join(os.path.dirname(__file__), 'settings.ini')
    shutil.copy(src, settings_file)

config = {}
cp = ConfigParser()
cp.read(settings_file)
for section in cp.sections():
    for option in cp.options(section):
        config['%s.%s' % (section, option)] = cp.get(section, option)

__all__ = ['config']