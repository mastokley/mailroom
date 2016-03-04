# coding=utf-8
from setuptools import setup

setup(
    name="mailroom",
    description="Mailroom Madness",
    version=0.1,
    author="Kent Ross, Michael Stokley",
    author_email="root.main@gmail.com",
    license="MIT",
    py_modules=["mailroom"],
    package_dir={"": "src"},
    install_requires=['tabulate'],
    extras_require={
        'test': ['pytest', 'tox']
    },
)
