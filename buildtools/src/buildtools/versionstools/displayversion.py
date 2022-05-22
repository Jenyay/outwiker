# coding: utf-8

from buildtools.buildfacts import BuildFacts


def display_version():
    """Display current version"""
    print('Current OutWiker version: {}'.format(BuildFacts().version))
