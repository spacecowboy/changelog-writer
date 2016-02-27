# -*- coding: utf-8 -*-

from __future__ import print_function, division
from collections import OrderedDict
import os
import requests
from .util import default_get, get_change_text


BASE = "https://api.github.com/repos/{}/{}/{}"


def paginated(url, **params):
    if "per_page" not in params:
        params["per_page"] = 30

    def inner_rest(func):
        def inner(config):
            print(url)

            print("Downloading 0", end="\r")
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

            count = 0

            while not done:
                json = r.json()
                count += len(json)
                print("Downloading {}".format(count), end="\r")

                for i in json:
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

            # Print once to clear
            print("Downloading {}".format(count))

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
    print("events")
    print("Downloading 0/{}".format(len(issues)),
          end='\r')
    for i, issue in enumerate(issues.values()):
        if issue.pr:
            issue.load_pr(prs[issue.number])
        else:
            print("Downloading {}/{}".format(i, len(issues)),
                  end="\r")

            event = get_event(config, issue.number)
            issue.load_event(event)

    print("Downloading {0}/{0}".format(len(issues)))

    return format_history(config, issues)


def get_event(config, issue_number):
    r = requests.get(BASE.format(config["github"]["user"],
                                 config["github"]["repo"],
                                 "issues/{}/events".format(issue_number)),
                     auth=("token", config["github"]["token"]))

    e = r.json()[0]

    return Event(e)


@paginated("pulls", state="closed")
def list_pull_requests(pr):
    return PullRequest(pr)


@paginated("issues", state="closed")
def list_issues(i):
    return Issue(i)


def format_history(config, issues):
    """
    Returns:
    OrderedDict - a history in the format specified by the config.
    """
    # Match structure in config
    history = get_structure(config["changelog"])

    for issue in issues.values():
        if not issue.fixed:
            continue
        # Make it a change
        change = Change(issue.number,
                        get_change_text(issue.body, issue.title),
                        get_changelog_labels(config, issue.labels))
        # Find its place in the history
        put_change_in_history(change, history)

    # Remove empty sections
    prune(history)

    return history


def get_changelog_labels(config, labels):
    result = []
    for l in config["github"]["labels"]:
        if l["key"] in labels:
            result.append(l["name"])
    return result


def put_change_in_history(change, history):
    for label in history:
        if label in change.labels:
            # Descend a step if nested
            if isinstance(history[label], dict):
                return put_change_in_history(change, history[label])
            else:
                history[label].append(change)
                return


def get_structure(labels):
    res = OrderedDict()
    for label in labels:
        # Nested only if inner dicts have content
        if (isinstance(labels, dict) and
            (isinstance(labels[label], dict) or
             isinstance(labels[label], list)) and
                0 < len(labels[label])):
            # Nested
            res[label] = get_structure(labels[label])
        else:
            # Each leaf label holds a list of changes
            res[label] = []

    return res


def prune(history):
    # Removes sections which do not contain any changes
    # Depth-first-search
    org = OrderedDict(history)
    for k, v in org.items():
        if isinstance(v, dict):
            prune(v)

        if len(v) == 0:
            del history[k]


class Issue(object):
    def __init__(self, json):
        self.number = json["number"]
        self.labels = [l["name"] for l in json["labels"]]
        self.title = json["title"]
        self.body = json["body"]
        self.pr = "pull_request" in json
        self.merged = None
        self.commit_id = None

    @property
    def fixed(self):
        return (self.merged is not None or
                self.commit_id is not None)

    def load_event(self, e):
        self.commit_id = e.commit_id

    def load_pr(self, pr):
        self.merged = pr.merged

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

    def __repr__(self):
        return "{}#{}: {} {}".format("pr", self.number,
                                     self.title, self.labels)


class Event(object):
    def __init__(self, json):
        self.event = json["event"]
        self.commit_id = json["commit_id"]

    def __repr__(self):
        return "Event: {}, sha={}".format(self.event,
                                          self.commit_id)


class Change(object):
    def __init__(self, id, change_text, labels):
        self.id = id
        self._change_text = change_text
        self.labels = labels

    @property
    def change_text(self):
        # Appends a link to the GitHub PR to the text
        return self._change_text + " (#{})".format(self.id)

    def __repr__(self):
        return self.change_text
