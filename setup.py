from setuptools import setup, find_packages

VERSION = "2.0.0"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="sarban",
    version=VERSION,
    author="liwyd",
    description="A comprehensive Python SDK for managing Marzban panel through its REST API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/liwyd/sarban",
    keywords=[
        "sarban",
        "marzban",
        "marzban python",
        "marzban panel",
        "marzban api",
        "marzban sdk",
        "v2ray",
        "xray",
        "proxy",
        "vpn"
    ],
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/liwyd/sarban',
        'Source': 'https://github.com/liwyd/sarban',
        'Tracker': 'https://github.com/liwyd/sarban/issues',
    },
)
