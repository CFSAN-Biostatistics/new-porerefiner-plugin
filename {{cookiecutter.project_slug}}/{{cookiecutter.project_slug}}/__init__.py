"""Top-level package for {{ cookiecutter.project_name }}."""

import pkgutil

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'

# __all__ = ["{{cookiecutter.project_slug}}"]

for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    _module = loader.find_module(module_name).load_module(module_name)
