# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pytest
from changelog.git import Git
from changelog.changelog import read_config, DEFAULT_CONFIG


@pytest.fixture
def config():
    return read_config(DEFAULT_CONFIG)


@pytest.fixture
def git():
    return Git()


class TestGit():

    def test_none_existing(self, git):
        commits = git.get_commits("master", "aslan10nmczzkslasvljiefs")

        assert len(commits) == 0

    def test_test(self, git):
        commits = git.get_commits("master", "#test")

        assert len(commits) > 0
        assert len(commits[0]) == 2

    def test_tes_no_boundary(self, git):
        commits = git.get_commits("master", "#tes", add_boundary=False)

        assert len(commits) > 0
        assert len(commits[0]) == 2

    def test_tes_with_boundary(self, git):
        commits = git.get_commits("master", "#tes")

        assert len(commits) == 0

    def test_changelog(self, git, config):
        config["git"]["tags"].append(dict(key="#test", name="Test commits"))
        data = git.get_changelog_data(config)

        assert len(data["master"]["Test commits"]) > 0
        assert len(data["master"]["Test commits"][0]) == 2
