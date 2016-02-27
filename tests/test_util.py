# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pytest
from changelog.util import default_get, get_change_text


class TestUtil():

    def test_default_get(self):
        d = {}

        x = default_get(d, "x", dict)

        assert "x" in d
        assert d["x"] is x

        a = default_get(default_get(d, "x", dict),
                        "a", list)

        assert "x" in d
        assert d["x"] is x
        assert "a" in d["x"]
        assert d["x"]["a"] is a
        assert len(a) == 0

    def test_change_text_none(self):
        with pytest.raises(Exception):
            get_change_text(None)

    def test_change_text_nothing(self):
        assert get_change_text(
            "Blabla Blabla\nBlabla Blachangelog bla") is None
        defval = "default"
        assert get_change_text("Blabla Blabla\nBlabla Blachangelog bla",
                               defval) == defval

    def test_change_text_long(self):
        s = """
        Blabla bla bla
        blab la bla
        bla bla
        changelog: Long text with leading spaces
        bla
        bla blal

        bla
        """
        assert (get_change_text(s, "default") ==
                "Long text with leading spaces")

    def test_change_text_short(self):
        s = """
        Blabla bla bla
        blab la bla
        bla bla
        cl: Short prefix with leading spaces
        bla
        bla blal

        bla
        """
        assert (get_change_text(s, "default") ==
                "Short prefix with leading spaces")
