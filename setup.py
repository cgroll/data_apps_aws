from setuptools import setup

DESCRIPTION = 'Data analysis automated on AWS'
LONG_DESCRIPTION = 'Data analysis automated on AWS'
DISTNAME = 'data_apps_aws'
MAINTAINER = 'Christian Groll'
MAINTAINER_EMAIL = 'groll.christian.edu@gmail.com'
URL = 'https://github.com/cgroll/data_apps_aws/'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/cgroll/data_apps_aws/'
VERSION = '0.1.dev'

install_requires = print('No requirements')

setup(name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=install_requires,
        packages=['data_apps_aws', 'data_apps_aws.src_data_pipes'],
        classifiers=[
                     'Intended Audience :: Science/Research',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'License :: OSI Approved :: BSD License',
                     'Topic :: Scientific/Engineering :: Visualization',
                     'Topic :: Multimedia :: Graphics',
                     'Operating System :: POSIX',
                     'Operating System :: Unix',
                     'Operating System :: MacOS'],
          )
