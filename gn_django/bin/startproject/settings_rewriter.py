import sys, os

error_msg = """
    settings_rewriter.py must be called with a valid path to a django
    settings file.
"""

try:
    settings_path = sys.argv[1]
    assert os.path.exists(settings_path)
except (IndexError, AssertionError):
    raise Exception(error_msg)

settings = ""
with open(settings_path, "r") as f:
    settings = f.read()

extra_installed_apps = """
    "django_jinja",
"""
installed_apps_index = settings.find("INSTALLED_APPS")
installed_apps_end = settings.find(']', installed_apps_index)
settings = settings[:installed_apps_end-1] + extra_installed_apps + settings[installed_apps_end:]

extra_templates = """
    {
        "BACKEND": "gn_django.template.backend.Jinja2",
        "APP_DIRS": True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gn_django.template.context_processors.settings',
            ],
        }
    },"""
templates_index = settings.find("TEMPLATES")
templates_start = settings.find('[', templates_index)

static_settings = """
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, '../.collected_static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../static')
]
CLIENT_LESS_COMPILER = '//cdnjs.cloudflare.com/ajax/libs/less.js/2.7.1/less.min.js'
"""

settings = settings.replace("STATIC_URL = '/static/'", static_settings)

settings = settings[:templates_start+1] + extra_templates + settings[templates_start+1:]

with open(settings_path, "w") as f:
    f.write(settings)
