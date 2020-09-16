from setuptools import find_packages, setup


with open('README.md', 'rb') as f:
    LONG_DESCRIPTION = f.read().decode('utf-8')


setup(
    name="releasely",
    version="1.1.0",
    description='A one stop shop for python library release management.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='releasemanagement continuousdelivery cd release git branch',
    url='https://github.com/huntcsg/releasely',
    license='MIT',
    author='Hunter Senft-Grupp',
    author_email='huntcsg@gmail.com',
    package_dir={
        "": "src"
    },
    packages=find_packages("src"),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        "bumpversion",
    ],
    extras_require={
        'testing': [
            'pytest',
            'pytest-cov',
        ],
        'linting': [
            'isort',
            'black',
        ]
    },
    entry_points={
        "console_scripts": [
            "releasely = releasely.__main__:main"
        ]
    },
)
