from setuptools import setup, find_packages

VERSION = "1.1.0"

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="sarban",
    version=VERSION,
    author="liwyd",
    description="marzban panel API easey-managing.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/liwyd/sarban",
    keywords=[
        "sarban",
        "marzban",
        "marzban python",
        "marzban panel"
    ],
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",
    python_requires='>=3.6'
)
