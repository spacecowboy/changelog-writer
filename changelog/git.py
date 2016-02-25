# -*- coding: utf-8 -*-
"""
Implements functionality specific to git
"""
from __future__ import print_function, division
from subprocess import check_output
from collections import OrderedDict


def default_get(d, key, factory):
    if key not in d:
        d[key] = factory()
    return d[key]


class Git(object):
    def __init__(self):
        "docstring"
        pass

    def get_changelog_data(self, config):
        """ Finds all data matching the config in the repo.

        Parameters:
        config - Configuration to use.

        Returns:
        A dictionary matching the config.
        """
        data = {}

        for rev in config["git"]["revs"]:
            for tag in config["git"]["tags"]:
                commits = self.get_commits(rev, tag["key"])
                if commits:
                    coms = default_get(
                        default_get(data, rev, OrderedDict),
                        tag["name"], OrderedDict)

                    for sha, title in commits:
                        coms[sha] = title

        return data


    def get_commits(self, rev, tag, add_boundary=True):
        """ Returns a list of commits with the specified tag.

        Parameters:
        rev - Revision (like a branch or tag) to search from.
        tag - What tag to grep for. Can be an extended
              regular expression.
        add_boundary - Appends \b to the end. True by default.

        Returns:
        A nested list, where each item is a pair of SHA1
        and title string, or an empty list of no commits
        were found.
        """
        grep = '--grep="' + tag

        if add_boundary:
            grep += r'\b"'
        else:
            grep += '"'

        args = ["git", "log", rev, "--oneline", "-i", "-E", grep]

        result = check_output(" ".join(args),
                              shell=True, universal_newlines=True)

        commits = []
        for line in result.split("\n"):
            if len(line) == 0:
                continue

            # kwarg 'maxsplit' only available in python3
            commits.append(line.split(" ", 1))

        return commits
