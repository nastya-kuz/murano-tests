import logging
from login_page import LoginPage
from environments_page import EnvironmentsPage
from services_page import ServicesPage
from selenium import webdriver
from behave import *

logging.basicConfig()
LOG = logging.getLogger(' Tests: ')


@given('browser with Environments page')
def step(browser):
    browser.page.Navigate('Project>Environments')
    browser.page = EnvironmentsPage(browser.driver)


@given('browser with environment "{environment_name}" details page')
def step(browser, environment_name):
    browser.page.Navigate("Project>Environments>%s" % environment_name)
    browser.page = ServicesPage(browser.driver)


@given('browser with new environment "{environment_name}" details page')
def step(browser, environment_name):
    page = browser.page
    page.Navigate("Project>Environments")
    page = EnvironmentsPage(browser.driver)
    page.create_environment(environment_name)

    page.Link(environment_name).Click()
    browser.page = ServicesPage(browser.driver)


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
    assert browser.page.Link(link_text).isPresented()


@then('page should not contain link "{link_text}"')
def step(browser, link_text):
    assert not browser.page.Link(link_text).isPresented()

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
        assert parameter[8:-1] in status
    elif 'no progress bar' in parameter:
        assert not progress_bar in status
    elif 'progress bar' in parameter:
        assert progress_bar in status

