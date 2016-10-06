# Introduction

`jira-query` is a basic command line utility for querying the JIRA API to
discover issues.  It adheres to the UNIX philosophy as best as possible; thus
its output is filterable and its scope is focused.

It does not support oauth as an authentication mechanism, but maybe it will
some day.  That feature is not useful to me because I cannot even manage oauth
clients on my JIRA instance (I am not a JIRA administrator at my organization).

# Quickstart

1. Prep a configuration file `~/.jira-query`

```yaml
---
server: https://example.atlassian.net/
username: joe@example.com
pass_cmd: gpg --decrypt ~/.jira.pass
```

2. Try it out

```
% jira-query -f '{key}, {summary}' 'project=PERF and assignee = currentUser()' 2>/dev/null
PERF-374, show that locust tests are imbalanced
PERF-372, make NR report request queueing
PERF-371, Balanced LMS loadtest
[...]
```

4. Make something useful :-)

# Tips

## menuing systems

One of the most basic ways of interacting with `jira-query` is via a generic
menuing system.  Examples include [dmenu](http://tools.suckless.org/dmenu/) for
Linux, [xmenu](https://github.com/uluyol/xmenu) for Mac,
[Alfred](https://www.alfredapp.com/) for Mac, etc.

```
#!/usr/bin/env sh
#
# my_qa_issues.sh - Prompt for QA issues assigned to yourself, and open the
#                   selected issue in a browser.
#

selection=$(jira-query -f '{key}, {summary}' 'project=QA and assignee=currentUser()' | dmenu -l 20)
url=$(echo "$selection" | cut -d, -f1 | xargs -I{} echo http://openedx.atlassian.net/browse/{})
surf $url
```

## password management

The `pass_cmd` field in the configuration file allows the use of your favorite
password manager, such as pass(1) or lastpass.
