import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Guide"
    version="0.0.1",
    author="Daniel Butler",
    author_email="dabutler89@gmail.com",
    description="Graphical user interface for dot env files. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniel-butler/guide",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
