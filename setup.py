import re

from setuptools import setup, find_packages

with open("pyproject.toml", "r") as fh:
    all_file_txt = fh.read()
    chunks = all_file_txt.split("\n\n")
    tools = next(filter(lambda line: line.startswith("[tool.poetry]"), chunks))
    NAME = re.findall(r"name = \"(.+)\"", tools)[0]
    VERSION = re.findall(r"version = \"(.+)\"", tools)[0]
    requirements_ver = next(filter(lambda line: line.startswith("[tool.poetry.dependencies]"), chunks)).splitlines()[2:]
    requirements = list(map(lambda x: x.split(" = ")[0], requirements_ver))

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=requirements,
    author="M_9SCO",
    author_email="programmerbojaner@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    description="A Python simple library for merging pulls with one label",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [f"{NAME}=automerge.command_line:cli"],
    },
)
