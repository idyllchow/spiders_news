from setuptools import setup, find_packages

setup(
    name         = 'spidersnews',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = spidersnews.settings']},
    scripts = ['bin/testargs.py']
)
