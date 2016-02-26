# -*- coding: utf-8 -*-

from __future__ import print_function, division
import sys, os
import argparse
from pkg_resources import resource_filename
import pytoml as toml
from .git import Git
from .util import default_get
from . import github


DEFAULT_CONFIG = resource_filename("changelog", "../config.toml")


def read_config(configfile):
    """ Parses the config file.

    Parameters:
    config - path to config file

    Returns:
    a dictionary with config options
    """
    with open(configfile, 'rb') as fin:
        return toml.load(fin)


def get_changelog(data):
    """ Prints a formatted changelog corresponding to the given
    data.
    """
    lines = []

    for rev, revdata in data.items():
        lines.append("# Change Log {}".format(rev))

        # TODO version?

        for header, commits in revdata.items():
            lines.append("")
            lines.append("## {}".format(header))
            lines.append("")

            for sha, title in commits.items():
                lines.append("- {} ({})".format(title, sha))

    return "\n".join(lines)


def main():
    # First read command line options
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config",
                        help="specify config file")
    parser.add_argument("--github_token",
                        help="GitHub token")

    args = parser.parse_args()

    # Now read specified config file or default
    configfile = args.config or DEFAULT_CONFIG
    config = read_config(configfile)

    if "github" in config:
        history = github.get_history(args, config)



    #if "git" in config:
    #    git = Git()
    #    data = git.get_changelog_data(config)
    #    print(get_changelog(data))


if __name__ == '__main__':
    main()
