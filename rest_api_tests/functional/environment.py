import ConfigParser
from behave import *
from keystoneclient.v2_0 import client as ksclient


project = 'murano'
CONFIG_PATH = 'config.ini'


def init_config():
    """
    @summary: Read configuration file
    @requires: CONFIG_PATH
    @return:  initialized conf file
    """
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_PATH)
    return config


def before_all(context):
    # define global variables
    context.result = None
    context.session = None
    context.environment = None
    context.expected_result = None

    conf = init_config()
    context.url = str(conf.get(project, 'url'))
    user = conf.get('keystone', 'user')
    password = conf.get('keystone', 'password')
    keystone_url = str(conf.get('keystone', 'url'))

    keystone_client = ksclient.Client(username=user, password=password,
                                      tenant_name=user, auth_url=keystone_url)
    token = str(keystone_client.auth_token)

    context.headers = {'X-Auth-Token': token,
                       'Content-type': 'application/json'}
