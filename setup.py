import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


DESCRIPTION = "skm_pyutils: Python Utilities"
LONG_DESCRIPTION = """skm_pyutils is a set of utility code written by Sean Martin.
"""

DISTNAME = 'skm_pyutils'
MAINTAINER = 'Sean Martin and Gao Xiang Ham'
MAINTAINER_EMAIL = 'martins7@tcd.ie'
URL = 'https://github.com/seankmartin/neuro-tools'
DOWNLOAD_URL = 'https://github.com/seankmartin/neuro-tools'
VERSION = '0.1.0'

INSTALL_REQUIRES = [
    'numpy'
]

PACKAGES = [
    'skm_pyutils'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'Operating System :: Windows'
]

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=read('LICENSE'),
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          classifiers=CLASSIFIERS,
          )
