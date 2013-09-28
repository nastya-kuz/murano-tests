Script for JIRA and launchpad bug descriptions sync
============

 This script allows to sync bug titles, descriptions, statuses and priorities between two different systems: JIRA and launchpad.

 Please, see more detailed information about the JIRA and launchpad by the following links:

 - https://www.atlassian.com/software/jira

 - https://launchpad.net/

How To Sync
============
 To run sync script need to perform the following steps:

1. Fix sync.cfg file - fill information about JIRA credentials for the project in JIRA.

2. Execute sync.py and wait for a few seconds:

   python sync.py

3. Script will open browser with launchpad configuration page, need to confirm access and close browser. After that need to wait for the full sync of JIRA and launchpad. 





 Mirantis Inc (C) 2013.
