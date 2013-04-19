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

from login_page import LoginPage
from environments_page import EnvironmentsPage
from services_page import ServicesPage
from selenium import webdriver
from behave import *


def check(browser, condition):
    if condition:
        browser.logger.test_case_finish()
    else:
        screenshot = browser.driver.get_screenshot_as_base64()
        browser.dblogger.save_screenshot(screenshot)
        browser.dblogger.test_case_finish('FAILED')
    assert condition


@given('browser with Environments page')
def step(browser):
    browser.page.Navigate('Project>Environments')
    browser.page = EnvironmentsPage(browser)


@given('browser with environment "{environment_name}" details page')
def step(browser, environment_name):
    browser.page.Navigate("Project>Environments>%s" % environment_name)
    browser.page = ServicesPage(browser)


@given('browser with new environment "{environment_name}" details page')
def step(browser, environment_name):
    page = browser.page
    page.Navigate("Project>Environments")
    page = EnvironmentsPage(browser)
    page.create_environment(environment_name)

    page.Link(environment_name).Click()
    browser.page = ServicesPage(browser)


@when('I create environment "{environment_name}"')
def step(browser, environment_name):
    browser.page.create_environment(environment_name)


@when('I create AD service "{ad_name}" with {ad_count} instances')
def step(browser, ad_name, ad_count=1):
    parameters = {'1-dc_name': ad_name,
                  '1-dc_count': ad_count,
                  '1-adm_password': "P@ssw0rd",
                  '1-recovery_password': "P@ssw0rd2"}
    browser.page.create_service('Active Directory', parameters)


@when('I create IIS service "{iis_name}" without domain')
@when('I create IIS service "{iis_name}" in domain {iis_domain}')
def step(browser, iis_name, iis_domain=''):
    parameters = {'1-iis_name': iis_name,
                  '1-adm_password': "P@ssw0rd",
                  '1-iis_domain': iis_domain}
    browser.page.create_service('Internet Information Services', parameters)


@when('I delete environment "{environment_name}"')
def step(browser, environment_name):
    browser.page.delete_environment(environment_name)


@when('I navigate to service "{service_name}" details page')
def step(browser, service_name):
    page = browser.page
    page.Navigate(service_name)
    page.Link('Service').Click()


@then('page should contain link "{link_text}"')
def step(browser, link_text):
    check(browser, browser.page.Link(link_text).isPresented())


@then('page should not contain link "{link_text}"')
def step(browser, link_text):
    check(browser, not browser.page.Link(link_text).isPresented())


@then('service name should be equal to "{service_name}"')
def step(browser, service_name):
    text = browser.page.TableCell('Name').Text()
    check(browser, text == service_name)


@then('service domain should be equal to "{service_domain}"')
def step(browser, service_domain):
    text = browser.page.TableCell('Domain').Text()
    check(browser, text == service_domain)


@then('{element} "{element_name}" has {parameter}')
def step(browser, element, element_name, parameter):
    page = browser.page
    status = ""
    if element == 'environment':
        status = page.get_environment_status(element_name)
    elif element == 'service':
        status = page.get_service_status(element_name)

    progress_bar = '<img src="/static/dashboard/img/loading.gif">'

    if 'status' in parameter:
        check(browser, parameter[8:-1] in status)
    elif 'no progress bar' in parameter:
        check(browser, not progress_bar in status)
    elif 'progress bar' in parameter:
        check(browser, progress_bar in status)
