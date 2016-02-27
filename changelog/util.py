# -*- coding: utf-8 -*-
"""
Some utility functions
"""
from __future__ import print_function, division


def default_get(d, key, factory):
    """ Returns the value from a dict, with the side-effect that if it doesn't
    contain it, the output from the factory will be placed in the dict
    before returning it.

    Parameters:
    d - dictionary to work on
    key - key of the value
    factory - a callable which will return the item to place as the value

    Returns:
    The value of the key in the dict, which should match the output of the
    factory.
    """
    if key not in d:
        d[key] = factory()
    return d[key]


def get_change_text(text, default_value=None):
    """ Given a piece of text, return the text which is prefixed, on its own
    line, with either 'changelog:' or 'cl:'. Leading/ending whitespace will
    be stripped.

    Parameters:
    text - text to search for keyword in
    default_value - optional value to return if nothing found

    Returns:
    string - Either the single line after the prefix, or the default value
    """
    val = default_value

    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("cl:"):
            val = line[3:].strip()
        elif line.startswith("changelog:"):
            val = line[10:].strip()

    return val
