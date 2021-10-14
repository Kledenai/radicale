#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="radicale-rights-ldap",
    version="0.1",
    description="""
    A radicale plugin to manage rights with ldap,
    with support for groups and shared calendars""",
    long_description="""
This is a radicale plugin enabling LDAP users to access shared group calendars.
The plugin  simply checks if a user owns the calendar or is member of
the group that owns the calendar and gives **read** and **write** permissions
if the check is successful.
    """,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="GNU GPLv3",
    install_requires=["radicale", "ldap3"],
    author="ZEDV FB-Physik FU-Berlin",
    author_email="zedv@physik.fu-berlin.de",
    url='https://github.com/sents/radicale-rights-ldap',
    packages=["radicale_rights_ldap"],
    entry_points={
        "console_scripts": [
            "radicale_create_groups.py = radicale_rights_ldap.create_group_calendars:main"
        ]
    },
)
