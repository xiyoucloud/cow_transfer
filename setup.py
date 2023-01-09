from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Easily downlaod file from CowTransfer'

setup(
    name="cow_transfer",
    version=VERSION,
    author="txb",
    author_email="txb.sdn@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['DownloadKit', 'requests'],
    keywords=['python', 'DownloadKit', 'cow_transfer'],
    entry_points={
    'console_scripts': [
        'cow = cow_transfer.main:cli'
    ]
    },
    license="MIT",
    url="https://github.com/xiyoucloud/cow_transfer.git",
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)