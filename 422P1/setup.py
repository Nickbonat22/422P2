"""
This is a setup.py script generated by py2applet

Usage:
    python3 setup.py py2app
"""
from setuptools import setup
import os
'''
  https://github.com/kevinlondon/django-py2app-demo/blob/master/setup.py
'''
def add_path_tree( base_path, path, skip_dirs=[ '.svn', '.git' ]):
  path = os.path.join( base_path, path )
  partial_data_files = []
  for root, dirs, files in os.walk( os.path.join( path )):
    sample_list = []
    for skip_dir in skip_dirs:
      if skip_dir in dirs:
        dirs.remove( skip_dir )
    if files:
      for filename in files:
        sample_list.append( os.path.join( root, filename ))
    if sample_list:
      partial_data_files.append((
        root.replace(
          base_path + os.sep if base_path else '',
          '',
          1
        ),
        sample_list
      ))
  return partial_data_files

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'iconfile':'icon.icns'
}
# project files
DATA_FILES += add_path_tree( '', 'Resources' )
# DATA_FILES += add_path_tree( '', 'Controllers' )
# DATA_FILES += add_path_tree( '', 'Models' )
# DATA_FILES += add_path_tree( '', 'Services' )
# DATA_FILES += add_path_tree( '', 'Views' )

setup(
    name='Cold Caller',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
