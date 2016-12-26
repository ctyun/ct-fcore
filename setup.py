from setuptools import setup, find_packages

setup(
    name = 'ct_fcore',
    version = '0.1.32',
    keywords = ('django', 'ctcloud', 'portal', 'ct_fcore', 'chinatelecom'),
    description = 'a portal framework for ctcloud using tornado',
    license = 'MIT License',
    install_requires = [],

    author = 'astwyg',
    author_email = 'i@ysgh.net',
    
    packages = find_packages(),
    platforms = 'any',

    url = "https://github.com/astwyg/ct-fcore",
)