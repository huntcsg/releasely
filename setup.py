from setuptools import find_packages, setup

setup(
    name="releasely",
    version="0.2.3",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["releasely = releasely.__main__:main"]},
)
