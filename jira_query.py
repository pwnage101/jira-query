from os.path import expanduser
from jira import JIRA
import yaml
import subprocess
import argparse

DEFAULT_CONF_FILE = '~/.jira-query'
DEFAULT_OUTPUT_FIELDS = ['key']


def csv_list(string):
   """
   Use this function as an argparse argument type.  It allows the following
   kind of argument to be parsed as a python list:

     $ command -l this,is,a,list

   which becomes the list ['this', 'is', 'a', 'list'] after calling
   parse_args().
   """
   return string.split(',')


def setup_client(conf_file):
    """read the configuration file and create a JIRA object"""
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
    parser.add_argument("-f", "--fields", help="issue fields to print", type=csv_list, default=DEFAULT_OUTPUT_FIELDS)
    parser.add_argument("-c", "--config", help="alternate location for the config file", type=str, default=DEFAULT_CONF_FILE)
    args = parser.parse_args()

    jira = setup_client(args.config)

    issues = jira.search_issues(args.query)

    for issue in issues:
        data = dict(issue.fields.__dict__)
        data['key'] = issue.key
        print('\t'.join([data[f] for f in args.fields]))


if __name__ == '__main__':
    main()
