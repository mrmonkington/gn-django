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
    'dal',
    'dal_select2',
"""
installed_apps_index = settings.find("INSTALLED_APPS")
installed_apps_end = settings.find(']', installed_apps_index)
settings = settings[:installed_apps_end-1] + extra_installed_apps + settings[installed_apps_end:]

extra_templates = """
    {
        "BACKEND": "gn_django.template.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
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

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../static')
]

# Static link configs

# Set the preprocessors for different clientside languages
STATICLINK_PREPROCESSORS = {
    'css': 'less',
}

# Set URL for client-side compiler
STATICLINK_CLIENT_COMPILERS = {
    'css': '//cdnjs.cloudflare.com/ajax/libs/less.js/2.7.1/less.min.js',
}

# Set debug mode for static asset compilation separately from main DEBUG setting
# STATICLINK_DEBUG = {
#     'css': False,
# }

# Set path within STATICFILES_DIRS setting where static files can be located.
# Defaults to file extension
# STATICLINK_FILE_MAP = {
#     'js': 'scripts'
# }

# Set version number to append to linked static files (for caching). Defaults to
# current timestamp.
# STATICLINK_VERSION = 123456

"""

settings = settings[:templates_start+1] + extra_templates + settings[templates_start+1:] + static_settings

with open(settings_path, "w") as f:
    f.write(settings)
