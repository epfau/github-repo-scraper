#!/usr/bin/env python

from codecs import open
from os import path
from distutils.core import setup
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="scraping-github-topics-repositories",
    version="1.0.0",
    description="A Web Scraper for Python",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/epfau/github-repo-scraper",
    author="Elisa Pfau",
    keywords="scraping - scraper",
    packages=["minishift"],
    python_requires=">=3.6",
    install_requires=["requests", "bs4", "pandas", "os", "python-daemon"]
)
