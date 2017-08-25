#!/usr/bin/env python
import os
import sys

from engine.libs.utils import get_default_django_settings_module

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_default_django_settings_module())
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')

    # NOTE: instead of changing the DJANGO_CONFIGURATION class for each environment we change the DJANGO_SETTINGS_MODULE
    # and keeping the same class (i.e. Settings) for all environments.
    #
    # So instead of having classes like 'Common', 'Prod', 'Dev' in the module 'engine.settings',
    # We would have class 'Settings' in modules 'engine.settings.common', 'engine.settings.prod' etc

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
