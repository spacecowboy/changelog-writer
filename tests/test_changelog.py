# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pytest
from changelog.changelog import (read_config,
                                 get_changelog,
                                 DEFAULT_CONFIG)


class TestConfig():

    def test_none(self):
        with pytest.raises(Exception):
            read_config(None)

    def test_default(self):
        config = read_config(DEFAULT_CONFIG)

        assert len(config) > 0
        assert config["git"] is not None

    def test_get_changelog(self):
        from changelog.git import Git
        config = read_config(DEFAULT_CONFIG)
        config["git"]["tags"].append(dict(key="#test", name="Test commits"))

        git = Git()

        data = git.get_changelog_data(config)

        s = get_changelog(data)

        assert s is None
        assert s is not None
