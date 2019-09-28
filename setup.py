from setuptools import setup, find_packages

setup(
    name='releasely',
    version='0.1.0',
    package_dir={
        '': 'src',
    },
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'releasely = releasely.__main__:main',
        ]
    }
)
