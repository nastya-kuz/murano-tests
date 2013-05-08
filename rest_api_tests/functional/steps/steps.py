import requests
import json
import logging
import ConfigParser
from keystoneclient.v2_0 import client as ksclient

CONFIG_PATH = 'config.ini'

logging.basicConfig()
LOG = logging.getLogger(__name__)


def get_request_parameters_from_file(context, template):
    request_file = 'templates/' + template
    request = {}
    response = {}

    conf.read(request_file)
    body = conf.get('request', 'body')
    headers = conf.get('request', 'headers')

    request['body'] = json.loads(body)
    request['headers'] = json.loads(headers)
    token = {'X-Auth-Token': context.headers['X-Auth-Token']}
    request['headers'].update(token)

    body = conf.get('response', 'json')
    response['body'] = json.loads(body)
    response['code'] = int(conf.get('response', 'code'))

    return request


@when('I create environment "{env_name}"')
def environment_create(context, env_name):
    body = json.dumps({"name": env_name})
    url = "%s/environments" % service_url
    result = requests.request('POST', url=url,
                              headers=context.headers, data=body)
    environment = result.json()
    # result.response_code

    # open the session for new environment
    url = '%s/environments/%s/configure' % (service_url, environment['id'])
    response = requests.request('POST', url=url,
                                headers=context.headers)
    session = response.json()
    headers['X-Configuration-Session'] = session[id]


@when('I delete environment "{env_name}"')
def environment_delete(context, env_name):
    body = json.dumps({"id": environment['id']})
    url = "%s/environments/%s" % (service_url, environment['id'])
    result = requests.request('DELETE', url=url, headers=context.headers)


@when('I update environment "{env_name}" to "{new_name}"')
def environment_action_update(context, env_name, new_name):
    body = json.dumps({'name': new_name})
    url = '%s/environments/%s' % (service_url, environment['id'])
    result = requests.request('PUT', url=url,
                              headers=context.headers, data=body)


@when('I deploy environment "{env_name}"')
def environment_action_deploy(context, env_name):
    url = str('%s/environments/%s/sessions/%s/deploy' %
              (service_url, environment['id'], session['id']))
    result = requests.request('POST', url=url, headers=context.headers)


@when('I delete opened session')
def session_delete(context, env_name):
    url = str('%s/environments/%s/sessions/%s' %
              (service_url, environment['id'], session['id']))
    response = requests.request('DELETE', url=url, headers=context.headers)
    assert response.status_code is 200


@when('I add AD service in environment "{env_name}" by template "{template}"')
def ad_action_create(context, env_name, template):
    url = str('%s/environments/%s/activeDirectories' %
              (service_url, environment['id']))
    request = get_request_parameters_from_file(context, template)
    response = requests.request('POST', url=url,
                                headers=request['headers'],
                                data=request['body'])


@when('I add IIS service in environment "{env_name}" by template "{template}"')
def iis_action_create(context, env_name, template):
    url = '%s/environments/%s/webServers' % (service_url, environment['id'])
    request = get_request_parameters_from_file(context, template)
    response = requests.request('POST', url=url,
                                headers=request['headers'],
                                data=request['body'])


@then('environment should contain AD service "{ad_name}"')
def ad_check(context, ad_name):
    ad_service = None
    url = str('%s/environments/%s/activeDirectories' %
              (service_url, environment['id']))
    response = requests.request('GET', url=url, headers=context.headers)
    services = response.json()
    for ad in services['activeDirectories']:
        if ad['name'] == ad_name:
            ad_service = ad

    assert ad_service


@then('environment should contain IIS service "{iis_name}"')
def iis_check(context, iis_name):
    iis_service = None
    url = '%s/environments/%s/webServers' % (service_url, environment['id'])
    response = requests.request('GET', url=url, headers=context.headers)
    services = response.json()
    for iis in services['webServers']:
        if iis['name'] == iis_name:
            iis_service = iis

    assert iis_service


def delete_all_environments():
    url = url=service_url + '/environments'
    response = requests.request('GET', url=url, headers=context.headers)
    result = response.json()

    for environment in result['environments']:
        environment_delete(None, environment['name'])

delete_all_environments()
