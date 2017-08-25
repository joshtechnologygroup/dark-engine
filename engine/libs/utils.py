import imp


def get_default_django_settings_module():
    try:
        file_ = imp.find_module('local', ['engine/settings'])[0]
    except ImportError:
        default_django_settings_module = "engine.settings.local"
    else:
        default_django_settings_module = "engine.settings.base"
        file_.close()
    return default_django_settings_module
