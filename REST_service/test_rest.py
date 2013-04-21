# -*- coding: utf-8 -*-


import unittest2
import requests
import json
import time
import random
import logging
from funkload.FunkLoadTestCase import FunkLoadTestCase

logging.basicConfig()
LOG = logging.getLogger(' REST service tests')

class TestSuite(FunkLoadTestCase):

    @classmethod
    def setUpClass(self):
        self.headers = {'X-Auth-Token': '7414eb76950b8d2b90b4c5a157f7f148'}

        response = requests.get(self.url, headers=self.headers)
        for env in response.json:
            self.action_delete_environment(env.id)

    def setUp(self):
        self.url = self.conf_get('main', 'url')

    def action_create_environment(self):
        headers = self.headers
        headers.update({'Content-Type': 'application/json'})
        name = "Environment" + str(random.randint(1, 10000))
        body = '{"name": "%s=%s"}' % (name, time.now())

        response = requests.post(self.url, headers=headers, data=body)
        assert response.status_code == 200
        return str(response.json.id)

    def action_delete_environment(self, env_id):
        url = self.url + '/' + str(env_id)
        response = requests.delete(self.url, headers=self.headers)
        assert response.status_code == 200

    def action_create_service_ad(self, env_id, name='test_ad'):
        headers = self.headers
        headers.update({'Content-Type': 'application/json'})

        url = self.url + '/' + str(response.json.id) + '/configure'
        response = requests.post(url, headers=headers, data=body)
        assert response.status_code == 200

        session_id = str(response.json.id)
        headers.update({'X-Configuration-Session': str(session_id)})
        body = ('{"name": "%s", "configuration": "standalone",'
                '"adminPassword": "P@ssw0rd", "domain": "test_ad",'
                '"units": [{"id": "d08887df15b94178b244904b506fe85b",'
                '"isMaster": true,"location": "west-dc"}]}') % name

        url = self.url + '/' + env_id + '/activeDirectories'

        response = requests.post(url, headers=headers, data=body)
        assert response.status_code == 200

    def action_create_service_iis(self, env_id, name='iis_service'):
        headers = self.headers
        headers.update({'Content-Type': 'application/json'})

        url = self.url + '/' + str(response.json.id) + '/configure'
        response = requests.post(url, headers=headers, data=body)
        assert response.status_code == 200

        session_id = str(response.json.id)
        headers.update({'X-Configuration-Session': str(session_id)})
        body = ('{"name": "%s","domain": {"name": "ad_test",'
                '"credentials": {"username":"admin", "password":"123"}'
                '}, "credentials": {"username":"admin", "password":"12."}'
                '"location": "temp"}') % name

        url = self.url + '/' + env_id + '/webServers'
        response = requests.post(url, headers=headers, data=body)
        assert response.status_code == 200

    def test_create_and_delete_environment(self):
        env_id = self.action_create_environment()
        self.action_delete_environment(env_id)

    def test_get_list_of_environments(self):
        headers = self.headers

        response = requests.get(self.url, headers=headers)
        assert response.status_code == 200

    def test_create_environment_with_ad(self):
        env_id = self.action_create_environment()
        self.action_create_service_ad(env_id, 'test1')
        self.action_create_service_ad(env_id, 'test2')
        self.action_create_service_ad(env_id, 'test3')

    def test_create_environment_with_iis(self):
        env_id = self.action_create_environment()
        self.action_create_service_iis(env_id, 'test1')
        self.action_create_service_iis(env_id, 'test2')
        self.action_create_service_iis(env_id, 'test3')

    def test_create_environment_with_a_few_services(self):
        env_id = self.action_create_environment()
        for i in range(150):
            self.action_create_service_ad(env_id, 'ad'+str(i))
            self.action_create_service_iis(env_id, 'iis'+str(i))

    def mix_for_load_testing(self):
        k = random.randint(1, 100)
        if k < 10:
            # 10%
            return self.test_get_list_of_environments()
        elif k < 30:
            # 20%
            return self.test_create_and_delete_environment()
        elif k < 50:
            # 20 %
            return self.test_create_environment_with_ad()
        elif k < 70:
            # 20 %
            return self.test_create_environment_with_iis()
        else:
            # 30 %
            return self.test_create_environment_with_a_few_services()

if __name__ == '__main__':
    unittest2.main()
