# -*- coding: utf-8 -*-

from __future__ import print_function, division
import os
import requests
from .util import default_get, get_change_text


BASE = "https://api.github.com/repos/{}/{}/{}"


def paginated(url, **params):
    if "per_page" not in params:
        params["per_page"] = 100

    def inner_rest(func):
        def inner(config):
            r = requests.get(BASE.format(config["github"]["user"],
                                         config["github"]["repo"],
                                         url),
                             params=params,
                             auth=("token", config["github"]["token"]))

            if "next" in r.links:
                nextpage = r.links["next"]["url"]
            else:
                nextpage = None

            result = {}
            done = False

            while not done:
                for i in r.json():
                    item = func(i)
                    result[item.number] = item

                if nextpage is not None:
                    r = requests.get(nextpage,
                                     auth=("token",
                                           config["github"]["token"]))

                    if "next" in r.links:
                        nextpage = r.links["next"]["url"]
                    else:
                        nextpage = None
                else:
                    done = True

            return result

        return inner
    return inner_rest


def get_history(args, config):
    """ Get history from GitHub.
    """
    # Get github token, prio is arg, config, envvar
    if args.github_token:
        token = args.github_token
    elif "token" in config["github"]:
        token = config["github"]["token"]
    elif "GITHUB_TOKEN" in os.environ:
        token = os.environ["GITHUB_TOKEN"]
    else:
        raise IllegalArgumentError("No token specified")

    # Place it in the config
    config["github"]["token"] = token

    # Load all issues and pull requests
    issues = list_issues(config)
    prs = list_pull_requests(config)

    # Merge PR with information in Issue (like labels)
    for issue in issues.values():
        if issue.pr:
            prs[issue.number].load_issue(issue)

    for pr in prs.values():
        print(pr)


@paginated("pulls", state="closed")
def list_pull_requests(pr):
    return PullRequest(pr)


@paginated("issues", state="closed")
def list_issues(i):
    return Issue(i)


class Issue(object):
    def __init__(self, json):
        self.number = json["number"]
        self.labels = [l["name"] for l in json["labels"]]
        self.title = json["title"]
        self.body = json["body"]
        self.pr = "pull_request" in json

    def __repr__(self):
        return "{}#{}: {} {}".format("pr" if self.pr else "issue",
                                     self.number, self.title, self.labels)


class PullRequest(object):
    def __init__(self, json):
        self.number = json["number"]
        self.merged = json["merged_at"]
        self.title = json["title"]
        self.body = json["body"]
        self.labels = None

    def load_issue(self, issue):
        self.labels = issue.labels

    def __repr__(self):
        return "{}#{}: {} {}".format("pr", self.number,
                                     self.title, self.labels)


class Change(object):
    def __init__(self, id, change_text, labels):
        self.id = id
        self._change_text = change_text
        self.labels = labels

    @property
    def change_text(self):
        # Appends a link to the GitHub PR to the text
        return self._change_text + " (#{})".format(self.id)
