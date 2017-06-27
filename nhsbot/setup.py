# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'nhsbot',
    version      = '0.1',
    description  = 'Dockerised python web scraper with NHS Choices website spider.',
    packages     = find_packages(),
    author       = 'Nicholas Elia',
    author_email = 'nich.elia@gmail.com',
    url          = 'https://github.com/nichelia/docker-scraper',
    entry_points = {'scrapy': ['settings = nhsbot.settings']},
)
