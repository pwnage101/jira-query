from os.path import expanduser
from jira import JIRA
import yaml
import subprocess
import argparse

DEFAULT_CONF_FILE = '~/.jira-query'
DEFAULT_OUTPUT_FORMAT = '{key}'


def setup_client(conf_file):
    with open(expanduser(conf_file)) as f:
        conf = yaml.load(f)
    jira_server = conf['server']
    jira_username = conf['username']
    jira_password = subprocess.check_output(conf['pass_cmd'], shell=True).decode('utf-8')
    options = { 'server': jira_server }
    jira = JIRA(options, basic_auth=(jira_username, jira_password))
    return jira


def main():
    parser = argparse.ArgumentParser(description="Search for JIRA issues")
    parser.add_argument("query", help="JQL query", type=str)
    parser.add_argument("-f", "--format", help="format string", type=str, default=DEFAULT_OUTPUT_FORMAT)
    parser.add_argument("-c", "--config", help="alternate location for the config file", type=str, default=DEFAULT_CONF_FILE)
    args = parser.parse_args()

    jira = setup_client(args.config)

    #jira.search_issues('project=PROJ and assignee != currentUser()')
    issues = jira.search_issues(args.query)

    for issue in issues:
        data = dict(issue.fields.__dict__)
        data['key'] = issue.key
        print(args.format.format(**data))


if __name__ == '__main__':
    main()
