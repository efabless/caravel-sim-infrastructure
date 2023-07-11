#!/usr/bin/env python3
from setuptools import setup, find_packages

requirements = open("requirements.txt").read().strip().split("\n")

setup(
    name="caravel_cocotb",
    packages=find_packages(),
    version="1.0.0",
    description="efabless caravel cocotb verification flow.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "caravel_cocotb": ["interfaces/*","interfaces/**/*", "scripts/*", "scripts/**/*"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    entry_points={"console_scripts": ["caravel_cocotb = caravel_cocotb.__main__:main"]},
    python_requires=">3.6",
)