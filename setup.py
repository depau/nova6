from setuptools import setup

setup(
    name='nova6',
    version='2.0',
    packages=['nova6'],
    url='',
    license='GPLv2',
    author='Davide Depau',
    author_email='davide@depau.eu',
    description='',
    entry_points={
        "console_scripts": [
            "nova6 = nova6.nova6:main",
            "nova6dl = nova6.nova6dl:main"
        ]
    },
    install_requires=[
        "requests",
        "requests[socks]"
    ]
)
