
from setuptools import setup

setup(
    name='jira-query',
    version='0.1',
    description='Simple command to query JIRA using JQL',
    author='Troy Sankey',
    author_email='',
    install_requires=['pyyaml', 'jira'],
    entry_points={
        'console_scripts': [
            'jira-query=jira_query:main',
        ]
    },
)
