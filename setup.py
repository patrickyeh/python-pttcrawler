__author__ = 'Vetom'

from setuptools import setup

setup(name='pttcrawler',
      version='0.2.0',
      description='A stream crawler for ptt',
      author='Patrick Yeh',
      author_email='vetom198@gmail.com',
      install_requires=['requests','BeautifulSoup','kafka-python'],
      url='https://github.com/patrickyeh/python-pttcrawler',
      packages=['pttcrawler','pttcrawler.stream'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7']
      )
