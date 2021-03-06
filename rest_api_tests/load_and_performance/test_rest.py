import unittest
import json
import random
import logging
import ConfigParser
from funkload.utils import Data
from funkload.FunkLoadTestCase import FunkLoadTestCase
from keystoneclient.v2_0 import client as ksclient


logging.basicConfig()
LOG = logging.getLogger(' REST service tests')


class TestSuite(FunkLoadTestCase):

    clear = False

    def setUp(self):
        self.url = self.conf_get('main', 'url')
        self.action_set_headers()

    def action_set_headers(self):
        self.clearHeaders()
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        user = config.get('keystone', 'user')
        password = config.get('keystone', 'password')
        keystone_url = config.get('keystone', 'url')

        keystone_client = ksclient.Client(username=user,
                                          password=password,
                                          tenant_name=user,
                                          auth_url=keystone_url)
        token = keystone_client.auth_token

        self.setHeader('X-Auth-Token', token)

    def action_create_environment(self):
        self.setHeader('Content-Type', 'application/json')
        name = "Environment" + str(random.randint(1, 10000))
        body = '{"name": "%s"}' % name

        response = self.post(self.url, params=Data('application/json', body),
                             description="Create Environment")
        assert response.code == 200
        
        result = json.loads(self.getBody())
        return str(result['id'])

    def action_delete_environment(self, env_id):
        self.action_set_headers()
        url = self.url + '/' + str(env_id)
        response = self.delete(url, description="Delete Environment")
        assert response.code == 200

    def action_get_session_for_environment(self, env_id):
        self.action_set_headers()
        self.setHeader('Content-Type', 'application/json')

        url = self.url + '/' + str(env_id) + '/configure'
        response = self.post(url, description="Get Session For Environment")
        assert response.code == 200

        result = json.loads(self.getBody())
        return str(result['id'])


    def action_create_service_ad(self, env_id, session_id, name='ad'):
        self.action_set_headers()
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"name": "%s", "configuration": "standalone",'
                '"adminPassword": "P@ssw0rd", "domain": "test_ad",'
                '"units": [{"id": "d08887df15b94178b244904b506fe85b",'
                '"isMaster": true,"location": "west-dc"}]}') % name

        url = self.url + '/' + env_id + '/activeDirectories'

        response = self.post(url, params=Data('application/json', body),
                             description="Create AD service")
        assert response.code == 200

    def action_create_service_iis(self, env_id, session_id, name='iis'):
        self.action_set_headers()
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"name": "%s","domain": {"name": "ad_test",'
                '"credentials": {"username":"admin", "password":"123"}'
                '}, "credentials": {"username":"admin", "password":"12."},'
                '"location": "temp","units":[{"id":"4334"}]}') % name

        url = self.url + '/' + env_id + '/webServers'
        response = self.post(url, params=Data('application/json', body),
                             description="Create IIS service")
        assert response.code == 200

    def test_create_and_delete_environment(self):
        env_id = self.action_create_environment()
        self.action_delete_environment(env_id)

    def test_get_list_of_environments(self):
        response = self.get(self.url, description="Get List Of Environments")
        assert response.code == 200

    def test_create_environment_with_ad(self):
        env_id = self.action_create_environment()
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_ad(env_id, session_id, 'test1')
        self.action_create_service_ad(env_id, session_id, 'test2')
        self.action_create_service_ad(env_id, session_id, 'test3')
        self.action_delete_environment(env_id)

    def test_create_environment_with_iis(self):
        env_id = self.action_create_environment()
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_iis(env_id, session_id, 'test1')
        self.action_create_service_iis(env_id, session_id, 'test2')
        self.action_create_service_iis(env_id, session_id, 'test3')
        self.action_delete_environment(env_id)

    def mix_for_load_testing(self):
        k = random.randint(1, 100)

        if k < 10:
            # 10%
            return self.test_get_list_of_environments()
        elif k < 40:
            # 30%
            return self.test_create_and_delete_environment()
        elif k < 70:
            # 30 %
            return self.test_create_environment_with_ad()
        else:
            # 30 %
            return self.test_create_environment_with_iis()


if __name__ == '__main__':
    unittest.main()
