import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


DESCRIPTION = "skm_pyutils: Python Utilities"
LONG_DESCRIPTION = read("README.md")
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

DISTNAME = 'skm_pyutils'
MAINTAINER = 'Sean Martin'
MAINTAINER_EMAIL = 'martins7@tcd.ie'
URL = 'https://github.com/seankmartin/PythonUtils'
DOWNLOAD_URL = 'https://github.com/seankmartin/PythonUtils/archive/0.1.0.tar.gz'
VERSION = '0.1.0'

INSTALL_REQUIRES = [
    'numpy',
    'matplotlib',
    'seaborn'
]

PACKAGES = [
    'skm_pyutils'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
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
          long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          classifiers=CLASSIFIERS,
          )
