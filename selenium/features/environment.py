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


import logging
from datetime import datetime
from steps.login_page import LoginPage
from steps.boffin.dblogger import DBLogger
from selenium import webdriver

LOG = logging.getLogger(__name__)


def before_all(context):
    context.screenshots = True
    context.dblogger_host = 'localhost'
    context.driver = webdriver.Firefox()
    context.page = LoginPage(context)
    context.page.login()

    context.logger.test_suite_start("WEB UI sanity tests")
    


def after_all(context):
    context.driver.close()
    context.logger.test_suite_finish()


def before_tag(context, tag):
    if tag == 'time':
        context.start = datetime.now()        


def after_tag(context, tag):
    if tag == 'time':
        result = datetime.now() - context.start
        LOG.info("Elapsed time: " + str(result))


def before_scenario(context, scenario):
    context.logger.test_case_start(scenario)
