# -*- coding: utf-8 -*-

from __future__ import print_function, division
from collections import OrderedDict
import pytest
from changelog.github import Change, format_history
from changelog.util import AttrDict


def od(*args):
    # Make an ordered dict, in a way that keeps the ordering
    d = OrderedDict()
    i = 0

    while i + 1 < len(args):
        d[args[i]] = args[i+1]
        i += 2

    return d


class TestChange():
    def test_adds_number_to_text(self):
        # Should work both with ints and strings
        c = Change(123, "Fixed a bug", [])
        assert c.change_text == "Fixed a bug (#123)"
        c = Change("123", "Fixed a bug", [])
        assert c.change_text == "Fixed a bug (#123)"


class TestHistory():
    def test_basic(self):
        pass

    def test_nested(self):
        config = dict(
            changelog=od("Docs", ["Fixed typos", "Enhancements"],
                         "Code", ["Bug fixes", "Enhancements"]),
            github=dict(
                labels=[
                    dict(key="docs", name="Docs"),
                    dict(key="code", name="Code"),
                    dict(key="typo", name="Fixed typos"),
                    dict(key="bug", name="Bug fixes"),
                    dict(key="enhancement", name="Enhancements"),
                    dict(key="feature", name="Enhancements")]))

        prs = od("1", AttrDict(dict(number=1, merged="3000-01-01",
                                    title="Fixed number one", body="",
                                    labels=["code", "bug"])),
                 "2", AttrDict(dict(number=2, merged="3000-01-02",
                                    title="..ber two",
                                    body="cl:Corrected number two",
                                    labels=["code", "bug"])),
                 "3", AttrDict(dict(number=3, merged="3000-01-02",
                                    title="blabla",
                                    body="changelog:Feature three",
                                    labels=["code", "enhancement"])),
                 "4", AttrDict(dict(number=4, merged="3000-01-05",
                                    title="Added manual", body="Bla bla bla",
                                    labels=["docs", "feature"])),
                 "5", AttrDict(dict(number=5, merged="3000-01-06",
                                    title="Corrected spelling", body="...",
                                    labels=["docs", "typo"])),
                 "6", AttrDict(dict(number=6, merged="3000-01-08",
                                    title="Added language support", body="",
                                    labels=["code", "feature"])))

        h = format_history(config, prs)

        print(h)

        # Verify structure (should be an ordered dict)
        assert list(h.keys()) == ["Docs", "Code"]

        # Docs
        d = h["Docs"]

        assert list(d.keys()) == ["Fixed typos", "Enhancements"]

        s = d["Fixed typos"]

        assert len(s) == 1
        assert s[0].change_text == "Corrected spelling (#5)"

        s = d["Enhancements"]

        assert len(s) == 1
        assert s[0].change_text == "Added manual (#4)"

        # Code
        d = h["Code"]

        assert list(d.keys()) == ["Bug fixes", "Enhancements"]

        s = d["Bug fixes"]

        assert len(s) == 2
        assert s[0].change_text == "Fixed number one (#1)"
        assert s[1].change_text == "Corrected number two (#2)"

        s = d["Enhancements"]

        assert len(s) == 2
        assert s[0].change_text == "Feature three (#3)"
        assert s[1].change_text == "Added language support (#6)"
