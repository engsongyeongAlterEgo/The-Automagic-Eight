from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': ['external_module'], 'build_exe': "build-setup"}

executables = [
    Executable('Main.py', target_name="main_setup", base=None)
]

print(sys.path)

setup(name='AutoMagic Eight',
      version = '1.0',
      description = 'A toolbox for Exacter',
      options = {'build_exe': build_options},
      executables = executables)