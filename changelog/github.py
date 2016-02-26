# -*- coding: utf-8 -*-

from __future__ import print_function, division
import os
import requests
from .util import default_get


BASE = "https://api.github.com/repos/{}/{}/{}"


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


def list_pull_requests(config):
    params = {}
    # TODO branch
    # Want only merged PRs, and they are of course closed
    params["state"] = "closed"
    # List as many as we can
    params["per_page"] = 100

    r = requests.get(BASE.format(config["github"]["user"],
                                 config["github"]["repo"],
                                 "pulls"),
                     params=params,
                     auth=("token", config["github"]["token"]))

    if "next" in r.links:
        nextpage = r.links["next"]["url"]
    else:
        nextpage = None

    result = {}
    done = False

    while not done:
        for p in r.json():
            pr = PullRequest(p)
            result[pr.number] = pr

        if nextpage is not None:
            r = requests.get(nextpage, auth=("token", config["github"]["token"]))

            if "next" in r.links:
                nextpage = r.links["next"]["url"]
            else:
                nextpage = None
        else:
            done = True

    return result


def list_issues(config):
    params = {}
    # TODO branch
    # Want only closed issues
    params["state"] = "closed"
    # List as many as we can
    params["per_page"] = 100
    # labels 	string 	A list of comma separated label names. Example: bug,ui,@high

    r = requests.get(BASE.format(config["github"]["user"],
                                config["github"]["repo"],
                                "issues"),
                     params=params,
                     auth=("token", config["github"]["token"]))

    if "next" in r.links:
        nextpage = r.links["next"]["url"]
    else:
        nextpage = None

    result = {}
    done = False

    while not done:
        issues = r.json()
        for i in r.json():
            issue = Issue(i)
            result[issue.number] = issue

        if nextpage is not None:
            r = requests.get(nextpage, auth=("token", config["github"]["token"]))

            if "next" in r.links:
                nextpage = r.links["next"]["url"]
            else:
                nextpage = None
        else:
            done = True

    return result


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
        return "{}#{}: {} {}".format("pr", self.number, self.title, self.labels)


#    @property
#    def labels(self):
#        if self._labels is None:
#            r = requests.get(BASE.format(self.config["github"]["user"],
#                                         self.config["github"]["repo"],
#                                         "issues/{}/labels".format(self.number)),
#                             auth=("token", self.config["github"]["token"]))
#            if r.status_code != 200:
#                raise ValueError("Failed to fetch labels for PR")#

#            self._labels = [l["name"] for l in r.json()]

#        return self._labels
