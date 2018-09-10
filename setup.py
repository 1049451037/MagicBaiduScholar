#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='MagicBaiduScholar',
    version='0.0.1',
    description="A Baidu Scholar search results crawler",
    install_requires=['beautifulsoup4', 'requests>=2.12.4', 'cchardet'],
    author='Qingsong Lv',
    author_email='lqs@mail.bnu.edu.cn',
    url="https://github.com/1049451037/MagicBaiduScholar",
    packages=find_packages(),
    package_data={'MagicBaiduScholar': ['data/*.txt']},
)
