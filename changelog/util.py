# -*- coding: utf-8 -*-
"""
Some utility functions
"""
from __future__ import print_function, division


def default_get(d, key, factory):
    """Returns the value from a dict, with the side-effect that if it doesn't
    contain it, the output from the factory will be placed in the dict
    before returning it.
    """
    if key not in d:
        d[key] = factory()
    return d[key]
