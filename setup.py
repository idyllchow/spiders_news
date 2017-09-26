from setuptools import setup, find_packages

setup(
    name         = 'moonlight',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = moonlight.settings']},
    scripts = ['bin/testargs.py']
)
