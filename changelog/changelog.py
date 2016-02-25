# -*- coding: utf-8 -*-

from __future__ import print_function, division
import argparse
from pkg_resources import resource_filename
import pytoml as toml


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

            for commit in commits:
                lines.append("- {} ({})".format(commit[1], commit[0]))

    return "\n".join(lines)


def main():
    # First read command line options
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config",
                        help="specify config file")

    args = parser.parse_args()

    # Now read specified config file or default
    configfile = args.config or DEFAULT_CONFIG
    config = read_config(configfile)


if __name__ == '__main__':
    main()
