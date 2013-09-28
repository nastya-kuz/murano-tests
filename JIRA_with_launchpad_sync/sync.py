# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import sys
import time
import httplib2
import ConfigParser
from dateutil import parser
from jira.client import JIRA
from launchpadlib.launchpad import Launchpad


httplib2.debuglevel=0


def update_status_of_jira_issue(jira, issue, new_status):
    for status in jira.transitions(issue):
        if get_str(status['name']) == new_status:
            new_status_id = status['id']

    jira.transition_issue(issue, new_status_id,
                          comment="Automatically updated by script.")
    

def get_str(parameter):
    if not parameter:
        parameter = ''
    return str(parameter.encode('ascii', 'ignore'))


def get_date(parameter):
    date = parser.parse(parameter)
    return date


def get_status(parameter):
    parameter = get_str(parameter)
    if parameter in ['In Testing', 'To Test']:
        return {'jira': parameter, 'launchpad': 'Fix Committed', 'code': 0}
    if parameter == 'Fix Committed':
        return {'jira': 'To Test', 'launchpad': 'Fix Committed', 'code': 0}
    if parameter == 'Resolved':
        return {'jira': 'Resolved', 'launchpad': 'Fix Released', 'code': 3}
    if parameter == 'Fix Released':
        return {'jira': 'Closed', 'launchpad': 'Fix Released', 'code': 3}
    if parameter in ['Reopened', 'To Do']:
        return {'jira': parameter, 'launchpad': 'New', 'code': 1}
    if parameter == 'Rejected':
        return {'jira': parameter, 'launchpad': 'Invalid' , 'code': 2}
    if parameter == 'Closed':
        return {'jira': parameter, 'launchpad': 'Fix Released', 'code': 3}
    if parameter in ['New', 'Incomplete', 'Opinion', 'Confirmed', 'Triaged']:
        return {'jira': 'ToDo', 'launchpad': parameter, 'code': 1}
    if parameter in ['Invalid', "Won't Fix"]:
        return {'jira': 'Rejected', 'launchpad': parameter, 'code': 2}
    return {'jira': parameter, 'launchpad': parameter, 'code': 4}


def get_priority(parameter):
    parameter = get_str(parameter)
    if parameter in ['Blocker', 'Critical']:
        return {'jira': parameter, 'launchpad': 'Critical', 'code': 0}
    if parameter in ['High', 'Medium']:
        return {'jira': 'Major', 'launchpad': parameter, 'code': 1}
    if parameter == 'Major':
        return {'jira': 'Major', 'launchpad': 'Medium', 'code': 1}
    if parameter in ['Nice to have', 'Some day']:
        return {'jira': parameter, 'launchpad': 'Low', 'code': 2}
    if 'Low' in parameter:
        return {'jira': 'Nice to have', 'launchpad': 'Low', 'code': 2}
 
    return {'jira': parameter, 'launchpad': parameter, 'code': 3}


def get_jira_bugs(url, user, password, project):
    ISSUES_COUNT = 900000
    ISSUE_FIELDS = 'key,summary,description,issuetype,' + \
                   'priority,status,updated,comment,fixVersions'

    jira = JIRA(basic_auth=(user, password), options={'server': url})

    SEARCH_STRING = 'project={0} and issuetype=Bug'.format(project)
    issues = jira.search_issues(SEARCH_STRING, fields=ISSUE_FIELDS,
                                maxResults=ISSUES_COUNT)
    bugs = []

    for issue in issues:
        bug = {'key': get_str(issue.key),
               'title': get_str(issue.fields.summary),
               'description': get_str(issue.fields.description),
               'priority': get_priority(issue.fields.priority.name),
               'status': get_status(issue.fields.status.name),
               'updated': get_date(issue.fields.updated),
               'comments': issue.fields.comment.comments,
               'fix_version': ''}

        if issue.fields.fixVersions:
            version = get_str(issue.fields.fixVersions[0].name)
            bug.update({'fix_version': version})

        summary = bug['title']
        if 'Launchpad Bug' in summary:
            summary = summary[24:]

        bug.update({'priority_code': bug['priority']['code'],
                    'status_code': bug['status']['code'],
                    'summary': summary})

        bugs.append(bug)

    print 'Found ' + str(len(bugs)) + ' bugs in JIRA'

    return bugs


def get_launchpad_bugs(project):
    project = project.lower()
    launchpad = Launchpad.login_with(project, 'production')
    project = launchpad.projects[project]
    launchpad_bugs = project.searchTasks(status=["New", "Fix Committed",
                                                 "Invalid", "Won't Fix",
                                                 "Confirmed", "Triaged",
                                                 "In Progress", "Incomplete",
                                                 "Fix Released"])

    bugs = []
    for launchpad_bug in launchpad_bugs:
        bug_link = get_str(launchpad_bug.self_link)
        key = re.search(r"[0-9]+$", bug_link).group()
        parameters = launchpad_bug.bug

        bug = {'key': get_str(key),
               'title': get_str(parameters.title),
               'summary': get_str(parameters.title),
               'description': get_str(parameters.description),
               'priority': get_priority(launchpad_bug.importance),
               'status': get_status(launchpad_bug.status),
               'updated': parameters.date_last_updated,
               #'comments': parameters.messages.entries[1:],
               #'attachments': parameters.attachments.entries,
               'fix_version': ''}

        #if parameters.linked_branches.entries:
        #    version = get_str(parameters.linked_branches.entries[0])
        #    bug.update({'fix_version': version})

        bug.update({'priority_code': bug['priority']['code'],
                    'status_code': bug['status']['code']})

        bugs.append(bug)

        " It is works very slow, print the dot per bug, for fun "
        print ".",
        sys.stdout.flush()

    print ''
    print 'Found ' + str(len(bugs)) + ' bugs on launchpad'

    return bugs


def update_jira_bug(jira, issue, title, description, priority, status):
    print "Udating JIRA bug ", title

    print "Description & Title & Priority updating..."
    try:
        issue.update(summary=title, description=description,
                     priority={'name': priority})
        print "... updated: OK"
    except:
        print "... updated: FAIL (not possible)"

    print "Status updating..."
    try:
        update_status_of_jira_issue(jira, get_str(issue.key), status)
        print "... updated: OK"
    except:
        print "... updated: FAIL (not possible)"


def update_lp_bug(bug, title, description, priority, status):
    print "Udating launchpad bug ", title
    # attachments
    #print launchpad.bugs[Lbug['key']].lp_operations

    print "Description & Title updating..."
    try:
        bug.title = title
        bug.description = description
        bug.lp_save()
        print "... updated: OK"
    except:
        print "... updated: FAIL (not possible)"

    print "Status & Priority updating..."
    try:
        bug_task = bug.bug_tasks[0]
        bug_task.status = status
        bug_task.importance = priority
        bug_task.lp_save()
        print "... updated: OK"
    except:
        print "... updated: FAIL (not possible)"


def create_jira_bug(jira, project_key, title, description):
    new_issue = None
    fields = {'project': { 'key': project_key }, 'summary': title,
              'description': description, 'issuetype': { 'name': 'Bug' }}

    print "Creating new bug desciption in JIRA... ", title
    try:
        new_issue = jira.create_issue(fields=fields)
        print "New bug was successfully created in JIRA"
    except:
        print "Can not create new bug in JIRA"

    return new_issue


def create_lp_bug(launchpad, project, title, description):
    new_bug = None
    print "Creating new bug desciption on launchpad... ", title
    try:
        new_bug = launchpad.bugs.createBug(target=project.self_link,
                                           title=title,
                                           description=description)
        print "New bug was successfully created on launchpad"
    except:
        print "Can not create new bug on launchpad"

    return new_bug


def sync_jira_with_launchpad(url, user, password, project, project_key=''):
    template = 'Launchpad Bug #{0}: '
    
    jira_bugs = get_jira_bugs(url, user, password, project)
    launchpad_bugs = get_launchpad_bugs(project)

    jira = JIRA(basic_auth=(user, password), options={'server': url})
    launchpad = Launchpad.login_with(project, 'production')

    " Sync already create tasks "
    for Jbug in jira_bugs:
        for Lbug in launchpad_bugs:
            if (Lbug['title'] in Jbug['title'] or \
                Lbug['key'] in Jbug['title']):
                for parameter in ['description', 'summary', 'status_code', \
                                  'priority_code']:
                    if Jbug[parameter] != Lbug[parameter]:
                        if Jbug['updated'] < Lbug['updated']:

                            new_title = ''
                            if not Lbug['key'] in Jbug['title']:
                                new_title = template.format(Lbug['key'])
                            new_title += Lbug['title']

                            update_jira_bug(jira, jira.issue(Jbug['key']),
                                            new_title, Lbug['description'],
                                            Lbug['priority']['jira'],
                                            Lbug['status']['jira'])
                        else:
                            new_title = Jbug['title']
                            if 'Launchpad Bug' in new_title:
                                new_title = str(new_title[24:])

                            update_lp_bug(launchpad.bugs[Lbug['key']],
                                          new_title, Jbug['description'],
                                          Jbug['priority']['launchpad'],
                                          Jbug['status']['launchpad'])
                        break
                break

    " Move new bugs from launchpad to JIRA "
    jira_bugs = get_jira_bugs(url, user, password, project)
    launchpad_bugs = get_launchpad_bugs(project)

    for Lbug in launchpad_bugs:
        if Lbug['status_code'] == 3:
            break

        sync = False
        duplicated = False

        for Jbug in jira_bugs:
            if (Lbug['title'] in Jbug['title'] or \
                Lbug['key'] in Jbug['title'] or \
                'Launchpad Bug' in Jbug['title']):
                sync = True

        for Lbug2 in launchpad_bugs:
            if Lbug2['title'] == Lbug['title'] and \
               Lbug2['key'] != Lbug['key']:
                duplicated = True

        if not sync and not duplicated:

            new_title = ''
            if not Lbug['key'] in Jbug['title']:
                new_title = template.format(Lbug['key'])
            new_title += Lbug['title']

            new_issue = create_jira_bug(jira, project_key, new_title,
                                        Lbug['description'])
            if new_issue:
                update_jira_bug(new_issue.key,
                                new_title, Lbug['description'],
                                Lbug['priority']['jira'],
                                Lbug['status']['jira'])

    " Move new bugs from JIRA to launchpad "
    jira_bugs = get_jira_bugs(url, user, password, project)
    launchpad_bugs = get_launchpad_bugs(project)

    for Jbug in jira_bugs:
        if Jbug['status_code'] == 3:
            break

        sync = False
        duplicated = False

        for Lbug in launchpad_bugs:
            if (Lbug['title'] in Jbug['title'] or \
                Lbug['key'] in Jbug['title'] or \
                'Launchpad Bug' in Jbug['title']):
                sync = True

        for Jbug2 in jira_bugs:
            if Jbug2['title'] == Jbug['title'] and \
               Jbug2['key'] != Jbug['key']:
                duplicated = True

        if not sync and not duplicated:
            lp_project = launchpad.projects[project]
            new_bug = create_lp_bug(launchpad, lp_project, Jbug['title'],
                                    Jbug['description'])

            if new_bug:
                update_lp_bug(new_bug,
                              Jbug['title'], Jbug['description'],
                              Jbug['priority']['launchpad'],
                              Jbug['status']['launchpad'])


config = ConfigParser.RawConfigParser()
config.read('sync.cfg')
Jira_link = config.get('JIRA', 'URL')
user = config.get('JIRA', 'user')
password = config.get('JIRA', 'password')
project_key = config.get('JIRA', 'project_key')
project = config.get('project', 'name')

sync_jira_with_launchpad(Jira_link, user, password, project, project_key)

