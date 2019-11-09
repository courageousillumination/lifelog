import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lifelog",
    version="0.0.1",
    author="Tristan Rasmussen",
    author_email="tristanrasmussen@tristanrasmussen.com",
    description="A set of utilities for keeping track of your life",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/courageousillumination/lifelog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["lifelog = lifelog.main:main",],},
)
