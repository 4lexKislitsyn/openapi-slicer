# coding: utf-8

from setuptools import setup, find_packages


setup(
    name="openapi-slicer",
    version=open('VERSION', 'r').read(),
    include_package_data=True,
    description=f"Open API Slicer Library",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license=open('LICENSE', 'r').read(),
    author="Alexander Kislitsyn",
    author_email="public@kislitsyn.work",
    url="https://github.com/4lexKislitsyn/openapi-slicer",
    packages=find_packages(exclude=["test", "tests"]),
    install_requires=["jsonpath-ng >= 1.5.3"],
    keywords=["Open API"],
)
