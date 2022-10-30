#!/usr/bin/env python3

from setuptools import setup
from todozer.constants import VERSION


setup(
    name="todozer",
    version=VERSION,
    description="A simple CLI tool to deal with tasks",
    long_description=open("README.md", encoding="utf-8-sig").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Todozer",
    license="MIT",
    python_requires=">=3.10",
    packages=["todozer"],
    install_requires=[
        "PyYAML~=6.0",
        "keyboard~=0.13.5",
        "vkostyanetsky.cliutils~=0.2.0",
    ],
    entry_points={"console_scripts": ["todozer=todozer.app:main"]},
    author="Vlad Kostyanetsky",
    author_email="vlad@kostyanetsky.me",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    keywords="organizer task todo",
)
