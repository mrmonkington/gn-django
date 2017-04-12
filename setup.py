from setuptools import setup, find_packages

setup(
    name='gn-django',
    url='https://github.com/gamernetwork/gn-django',
    description='Collection of tools and patterns for Gamer Network django apps/projects.',
    long_description=open('README.md').read(),
    install_requires=[
        "django>=1.11",
        "django-jinja>=2.2.2",
    ],
    dependency_links = [
    ],
    include_package_data=True,
    packages = ['gn_django'],
)
