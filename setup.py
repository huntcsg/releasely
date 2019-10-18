from setuptools import find_packages, setup

setup(
    name="releasely",
    version="1.0.2",
    package_dir={"": "src"},
    packages=find_packages("src"),
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
