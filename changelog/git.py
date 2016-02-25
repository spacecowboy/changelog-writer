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

    def get_commits(self, tag):
        args = ["git", "log", "--oneline", "-i", "-E",
                r'--grep="#' + str(tag) + r'\b"']
        result = check_output(" ".join(args), shell=True, universal_newlines=True)


        print(result)
        return result
