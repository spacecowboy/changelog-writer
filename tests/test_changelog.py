# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pytest
from changelog.changelog import read_config, DEFAULT_CONFIG


class TestConfig():

    def test_none(self):
        with pytest.raises(Exception):
            read_config(None)

    def test_default(self):
        config = read_config(DEFAULT_CONFIG)

        assert len(config) > 0
