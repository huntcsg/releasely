from setuptools import find_packages, setup

setup(
    name="releasely",
    version="1.0.2",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["releasely = releasely.__main__:main"]},
)
