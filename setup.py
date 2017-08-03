from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='nova6',
    version='2.0.1',
    packages=['nova6'],
    url='https://github.com/Depaulicious/Nova6',
    license='GPLv2',
    author='Davide Depau',
    author_email='davide@depau.eu',
    description='A torrent search engine based on qBittorrent\'s',
    long_description=long_description,
    entry_points={
        "console_scripts": [
            "nova6 = nova6.nova6:main",
            "nova6dl = nova6.nova6dl:main"
        ]
    },
    install_requires=[
        "requests",
        "requests[socks]",
        "PySocks!=1.5.7,>=1.5.6"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Communications :: File Sharing',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='torrent search engine requests'
)
