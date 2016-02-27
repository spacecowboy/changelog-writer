# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pytest
from changelog.github import Change


class TestChange():
    def test_adds_number_to_text(self):
        # Should work both with ints and strings
        c = Change(123, "Fixed a bug", [])
        assert c.change_text == "Fixed a bug (#123)"
        c = Change("123", "Fixed a bug", [])
        assert c.change_text == "Fixed a bug (#123)"
