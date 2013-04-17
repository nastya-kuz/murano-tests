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

import unittest2
import logging
from login_page import LoginPage
from environments_page import EnvironmentsPage
from services_page import ServicesPage
from selenium import webdriver


logging.basicConfig()
LOG = logging.getLogger(' Tests: ')

page = None

def generate_ad(name="test", count=1):
    """
        This function generates parameters for
        Active Directory service
    """
    ad_parameters = {'1-dc_name': name,
                     '1-dc_count': count,
                     '1-adm_password': "P@ssw0rd",
                     '1-recovery_password': "P@ssw0rd2"}
    return ['Active Directory', ad_parameters]

def generate_iis(name="test", domain="test"):
    """
        This function generates parameters for
        Internet Information Services service
    """
    iis_parameters = {'1-iis_name': name,
                      '1-adm_password': "P@ssw0rd",
                      '1-iis_domain': domain}
    return ['Internet Information Services', iis_parameters]


environment_for_deploy = 'environment_for_deploy'


class SanityTests(unittest2.TestCase):

    screenshots = 0  # Make screenshots for the end of each test

    @classmethod
    def setUpClass(self):
        """
            Open browser, navigate to the login page,
            login and navigate to the Windows Data Centers page
        """
        driver = webdriver.Firefox()
        page = LoginPage(driver)
        page.login()

    @classmethod
    def tearDownClass(self):
        """
            Close browser
        """
        page.driver.close()

    def setUp(self):
        """
            Navigate to the start page
        """
        page.Navigate('Project:Environments')
        page = EnvironmentsPage(driver)

    def tearDown(self):
        """
            Make screenshot
        """
        self.screenshots += 1
        page.driver.save_screenshot("screen_%s.png" % self.screenshots)

    def test_001_create_environment(self):
        page.create_environment('dc1')
        assert page.Link('dc1').isPresented()

    def test_002_delete_environment(self):
        page.delete_environment('dc1')
        assert not page.Link('dc1').isPresented()

    def test_003_create_environment_before_deploy(self):
        ad_name = "AD.net"
        iis_name = "iis_server"
        page.create_environment(environment_for_deploy)

    def test_004_configure_environment_before_deploy(self):
        page.Navigate(environment_for_deploy)
        page = ServicesPage(driver)

        page.create_service(generate_ad(ad_name, 2))
        assert page.Link(ad_name).isPresented()

        page.create_service(generate_iis(iis_name, ad_name))
        assert page.Link(iis_name).isPresented()

    def test_005_deploy_environment(self):
        page.deploy_environment(environment_for_deploy)
        status = page.get_environment_status(environment_for_deploy)
        assert 'Deploy in progress' in status

    def test_006_create_environments(self):
        for i in range(1, 10):
            name = "environment" + str(i)
            page.create_environment(name)
            assert page.Link(name).isPresented()

    def test_007_delete_environments(self):
        page.delete_environment('environment1')
        page.delete_environment('environment9')
        assert not page.Link('environment1').isPresented()
        assert not page.Link('environment9').isPresented()

        for i in range(2, 9):
            name = 'environment' + str(i)
            assert page.Link(name).isPresented()

    def test_008_create_service_ad(self):
        env_name = 'test05'
        name = "dc001.local"
        page.create_environment(env_name)

        page.Navigate(env_name)
        page = ServicesPage(driver)
        page.create_service(generate_ad(name, 1))
        assert page.Link(name).isPresented()

    def test_009_create_service_ad_two_instances(self):
        env_name = 'test06'
        name = "dc002.local"

        page.create_environment(env_name)
        page.Navigate(env_name)
        page = ServicesPage(driver)

        page.create_service(generate_ad(name, 2))
        assert page.Link(name).isPresented()

    def test_010_create_service_ad_with_iis(self):
        env_name = 'test07'
        ad_name = "dc003.local"

        page.create_environment(env_name)
        page.Navigate(env_name)
        page = ServicesPage(driver)

        page.create_service(generate_ad(ad_name, 3))
        assert page.Link(ad_name).isPresented()

        for i in range(5):
            iis_name = 'iis_server' + str(i)
            page.create_service(generate_iis(iis_name, ad_name))
            assert page.Link(iis_name).isPresented()

    def test_011_delete_environment_with_services(self):
        name = "test07"
        page.delete_environment(name)
        assert not page.Link(name).isPresented()

    def test_012_service_deploy_in_progress_status(self):
        ad_name = "AD.net"
        iis_name = "iis_server"

        page.Navigate(environment_for_deploy)
        page = ServicesPage(driver)

        ad_status = page.get_service_status(ad_name)
        iis_status = page.get_service_status(iis_name)

        assert 'Deploy in progress' in ad_status
        assert 'Deploy in progress' in iis_status

    def test_013_show_service_details_for_deploy(self):
        ad_name = "AD.net"
        iis_name = "iis_server"

        page.Navigate(environment_for_deploy)
        page = ServicesPage(driver)

        page.Navigate(iis_name)
        page.Link('Service').Click()

        name = page.TableCell('Name').Text()
        domain = page.TableCell('Domain').Text()

        assert name == iis_name
        assert domain == ad_name


if __name__ == '__main__':
    unittest2.main()
