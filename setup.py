from setuptools import setup

with open("requirements.txt", "r") as f:
    req_list = f.read().split("\n")[:-1]

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name                          = "tapi",
    version                       = "0.0.7",
    description                   = "Tines REST API wrapper",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/1Doomdie1/Tapi",
    author                        = "Todoran Horia",
    license                       = "GPL-3.0",
    classifiers                   = [
        "License :: OSI Approved :: GPL-3.0 License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires              = req_list,
    extras_require                = {
        "dev": ["pytest", "twine"],
    },
    python_requires               =">=3.10"
)