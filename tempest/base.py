# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest import config
from tempest.common import rest_client
import tempest.test
import json


class MuranoTest(tempest.test.BaseTestCase):

    def setUp(self):
        """
            This method allows to initialize authentication before
            each test case and define parameters of Murano API Service
            This method also create environment for all tests
        """

        super(MuranoTest, self).setUp()

        if not config.TempestConfig().murano.murano_avaible:
            raise self.skipException("Murano tests is disabled")
        _config = config.TempestConfig()
        #user = self.config.identity.username
        user = self.config.identity.admin_username
        #password = self.config.identity.password
        password = self.config.identity.admin_password
        #tenant = self.config.identity.tenant_name
        tenant = self.config.identity.admin_tenant_name
        auth_url = self.config.identity.uri
        client_args = (_config, user, password, auth_url, tenant)

        self.client = rest_client.RestClient(*client_args)
        self.client.service = 'identity'
        self.token = self.client.get_auth()
        self.client.base_url = self.config.murano.murano_url

        response, environment = self.create_environment('test455444')
        self.environments = [environment, ]

    def tearDown(self):
        """
            This method allows to clean up after each test.
            The main task for this method - delete environment after
            PASSED and FAILED tests.
        """

        super(MuranoTest, self).tearDown()

        for environment in self.environments:
            try:
                response = self.delete_environment(environment['id'])
            except:
                pass

    def create_environment(self, name):
        """
            This method allows to create environment.

            Input parameters:
              name - Name of new environment

            Returns response and new environment.
        """

        post_body = '{"name": "%s"}' % name
        resp, body = self.client.post('environments', post_body,
                                      self.client.headers)

        return resp, json.loads(body)

    def delete_environment(self, environment_id):
        """
            This method allows to delete environment

            Input parameters:
              environment_id - ID of deleting environment
        """
        resp, body = self.client.delete('environments/' + str(environment_id),
                                        self.client.headers)

    def update_environment(self, environment_id, environment_name):
        """
            This method allows to update environment instance

            Input parameters:
              environment_id - ID of updating environment
              environment_name - name of updating environment
        """
        post_body = '{"name": "%s"}' % (environment_name + "-changed")
        resp, body = self.client.put('environments/' + str(environment_id),
                                        post_body, self.client.headers)
        return resp, json.loads(body)

    def get_list_environments(self):
        """
            This method allows to get a list of existing environments

            Returns response and list of environments
        """
        resp, body = self.client.get('environments',
                                     self.client.headers)
        return resp, json.loads(body)

    def get_environment_by_id(self,environment_id):
        """
            This method allows to get environment's info by id

            Input parameters:
              environment_id - ID of needed environment
            Returns response and environment's info
        """
        resp, body = self.client.get('environments/' + str(environment_id), 
                                     self.client.headers)
        return resp, json.loads(body)

    def create_session(self, environment_id):
        """
            This method allow to create session

            Input parameters:
              environment_id - ID of environment
                   where session should be created
        """
        post_body = None
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/configure',
                                      post_body, self.client.headers)
        return resp, json.loads(body)

    def get_session_info(self, environment_id, session_id):
        """
            This method allow to get session's info

            Input parameters:
              environment_id - ID of environment
                             where needed session was created
              session_id - ID of needed session
            Return response and session's info
        """
        resp, body = self.client.get('environments/' + str(environment_id) +
                                      '/sessions/' + str(session_id),
                                      self.client.headers)
        return resp, json.loads(body)


    def delete_session(self, environment_id, session_id):
        """
            This method allow to delete session

            Input parameters:
              environment_id - ID of environment
                             where needed session was created
              session_id - ID of needed session
        """
        resp, body = self.client.delete('environments/' + str(environment_id) +
                                        '/sessions/' + str(session_id),
                                        self.client.headers)

    def create_AD(self, environment_id, session_id):
        """
            This method allow to add AD

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        post_body = {"type": "activeDirectory","name": "ad.local",
                    "adminPassword": "P@ssw0rd", "domain": "ad.local",
                    "availabilityZone": "nova", "unitNamingPattern": "",
                    "flavor": "m1.medium", "osImage":
                    {"type": "ws-2012-std", "name": "ws-2012-std", "title":
                    "Windows Server 2012 Standard"},"configuration":
                    "standalone", "units": [{"isMaster": True,
                    "recoveryPassword": "P@ssw0rd",
                    "location": "west-dc"}]}
        
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_IIS(self, environment_id, session_id, domain_name = ""):
        """
            This method allow to add IIS

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        iis_name = "someservice"
        creds = {'username': 'Administrator',
                 'password': 'P@ssw0rd'}
        post_body = {"type": "webServer", "domain": domain_name, 
                      "availabilityZone": "nova", "name": iis_name,
                      "adminPassword": "P@ssw0rd", "unitNamingPattern": "",
                       "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                       "title": "Windows Server 2012 Standard"},
                      "units": [{}], "credentials": creds,
                      "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_apsnet(self, environment_id, session_id, domain_name = ""):
        """
            This method allow to add apsnet

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        creds = {'username': 'Administrator',
                 'password': 'P@ssw0rd'}
        post_body = {"type": "aspNetApp", "domain": domain_name, 
                     "availabilityZone": "nova", "name": "someasp", "repository":
                     "git://github.com/Mirantis/murano-mvc-demo.git", 
                     "adminPassword": "P@ssw0rd", "unitNamingPattern": "",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"}, 
                     "units": [{}], "credentials": creds, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_IIS_farm(self, environment_id, session_id, domain_name = ""):
        """
            This method allow to add IIS farm

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        creds = {'username': 'Administrator',
                 'password': 'P@ssw0rd'}
        post_body = {"type": "webServerFarm", "domain": domain_name, 
                     "availabilityZone": "nova", "name": "someIISFARM",
                     "adminPassword": "P@ssw0rd", "loadBalancerPort": 80, 
                     "unitNamingPattern": "",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "units": [{}, {}], 
                     "credentials": creds, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_apsnet_farm(self, environment_id, session_id, domain_name = ""):
        """
            This method allow to add apsnet farm

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        creds = {'username': 'Administrator',
                 'password': 'P@ssw0rd'}
        post_body = {"type": "aspNetAppFarm", "domain": domain_name, 
                 "availabilityZone": "nova", "name": "SomeApsFarm", 
                 "repository": "git://github.com/Mirantis/murano-mvc-demo.git",
                 "adminPassword": "P@ssw0rd", "loadBalancerPort": 80, 
                 "unitNamingPattern": "",
                 "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                 "title": "Windows Server 2012 Standard"}, 
                 "units": [{}, {}], 
                 "credentials": creds, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_SQL(self, environment_id, session_id, domain_name = ""):
        """
            This method allow to add SQL

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        post_body = {"type": "msSqlServer", "domain": domain_name,
                     "availabilityZone": "nova", "name": "SQLSERVER",
                     "adminPassword": "P@ssw0rd", "unitNamingPattern": "",
                     "saPassword": "P@ssw0rd", "mixedModeAuth": "true",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},"units": [{}],
                     "credentials": {"username": "Administrator",
                     "password": "P@ssw0rd"}, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_SQL_cluster(self, environment_id, session_id, domain_name = ""):
        """
            This method allow to add SQL cluster

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        AG = self.config.murano.agListnerIP
        clIP = self.config.murano.clusterIP
        post_body = {"domain": domain_name, "domainAdminPassword": "P@ssw0rd",
                     "externalAD": False,
                     "sqlServiceUserName": "Administrator",
                     "sqlServicePassword": "P@ssw0rd",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "agListenerName": "SomeSQL_AGListner",
                     "flavor": "m1.medium",
                     "agGroupName": "SomeSQL_AG",
                     "domainAdminUserName": "Administrator",
                     "agListenerIP": AG,
                     "clusterIP": clIP,
                     "type": "msSqlClusterServer", "availabilityZone": "nova",
                     "adminPassword": "P@ssw0rd",
                     "clusterName": "SomeSQL", "mixedModeAuth": True,
                     "unitNamingPattern": "", "units": [{"isMaster": True,
                     "name": "node1", "isSync": True}, {"isMaster": False,
                     "name": "node2", "isSync": True}],
                     "name": "Sqlname", "saPassword": "P@ssw0rd",
                     "databases": []}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body) 

    def delete_service(self, environment_id, session_id, service_id):
        """
            This method allow to delete service

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
              service_id - ID of needed service
        """
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp = self.client.delete('environments/' + str(environment_id)
                                  + '/services/' + str(service_id),
                                  self.client.headers)

    def get_list_services(self, environment_id, session_id):
        """
            This method allow to get list of services

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.get('environments/' + str(environment_id) +
                                      '/services',
                                      self.client.headers)
        return resp, json.loads(body)

    def get_service_info(self, environment_id, session_id, service_id):
        """
            This method allow to get detailed service info

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
              service_id - ID of needed service
        """
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.get('environments/' + str(environment_id) +
                                      '/services/' + str(service_id),
                                      self.client.headers)
        return resp, json.loads(body)

    def update_service(self, environment_id, session_id, service_id, s_body):
        """
            This method allows to update service

            Input parameters:
              environment_id - env's id
              session_id - session_id where service is attach
              service_id - service id of updating service
              s_body - json obj
        """
        s_body['flavor'] = "m1.small"
        post_body = json.dumps(s_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.put('environments/' + str(environment_id)
                                  + '/services/' + str(service_id), post_body,
                                  self.client.headers)
        return resp, json.loads(body)

    def deploy_session(self, environment_id, session_id):
        """
            This method allow to send environment on deploy

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        post_body = None
        resp = self.client.post('environments/' + str(environment_id) +
                                      '/sessions/' + str(session_id) +
                                      '/deploy', post_body,
                                      self.client.headers)
        return resp

    def get_deployments_list(self, environment_id):
        """
            This method allow to get list of deployments

            Input parameters:
              environment_id - ID of current environment
        """
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/deployments', self.client.headers)
        return resp, json.loads(body)

    def get_deployment_info(self, environment_id, deployment_id):
        """
            This method allow to get detailed info about deployment

            Input parameters:
              environment_id - ID of current environment
              deployment_id - ID of needed deployment
        """
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/deployments/' + str(deployment_id),
                                     self.client.headers)
        return resp, json.loads(body)
