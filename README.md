# Introduction

`jira-query` is a basic command line utility for querying the JIRA API to
discover issues.  It adheres to the UNIX philosophy as best as possible; thus
its output is filterable and its scope is focused.

It does not support oauth as an authentication mechanism, but maybe it will
some day.  That feature is not useful to me because I cannot even manage oauth
clients on my JIRA instance (I am not a JIRA administrator at my organization).

# Quickstart

1. Prep a configuration file

    ```yaml
    ---
    server: https://openedx.atlassian.net/
    username: tsankey@edx.org
    pass_cmd: gpg --decrypt ~/.jira.pass
    ```

2. Try it out

    ```
    jira-query -f '{key}, {summary}' 'project=PERF and assignee = currentUser()'
    ```

3. Leverage [dmenu](http://tools.suckless.org/dmenu/) ([xmenu](https://github.com/uluyol/xmenu) for mac users) for user input

    ```
    selection=$(jira-query -f '{key}, {summary}' 'project=PERF and assignee = currentUser()' | dmenu -l 20)
    url=$(echo "$selection" | cut -d, -f1 | xargs -I{} echo http://openedx.atlassian.net/browse/{})
    surf $url
    ```

4. Make something useful
