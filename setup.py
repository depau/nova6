import sys
from distutils.core import setup

if sys.version_info.major == 2:
    setup(
        name='novasearch',
        version='1.41',
        packages=['nova'],
        url='',
        license='GPLv2',
        author='Davide Depau',
        author_email='davide@depau.eu',
        description='',
        entry_points={
            "console_scripts": [
                "nova2 = nova.nova2:run"
            ]
        }
    )
else:
    setup(
        name='novasearch',
        version='1.40',
        packages=['nova3'],
        url='',
        license='GPLv2',
        author='Davide Depau',
        author_email='davide@depau.eu',
        description='',
        entry_points={
            "console_scripts": [
                "nova2 = nova3.nova2:run"
            ]
        }
    )
