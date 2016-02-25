# -*- coding: utf-8 -*-
"""
Implements functionality specific to git
"""
from __future__ import print_function, division
from subprocess import check_output


class Git(object):
    def __init__(self):
        "docstring"
        pass

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

            commits.append(line.split(maxsplit=1))

        return commits
