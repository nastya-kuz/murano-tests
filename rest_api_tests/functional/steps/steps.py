import requests
import json
import logging


logging.basicConfig()
LOG = logging.getLogger(__name__)


result = None
conf = init_config()
service_url = conf.get('murano', 'url')
user = conf.get('keystone', 'user')
password = conf.get('keystone', 'password')
keystone_url = conf.get('keystone', 'url')
keystone_client = ksclient.Client(username=user, password=password,
                                  tenant_name=user, auth_url=keystone_url)
token = keystone_client.auth_token
headers = {'X-Auth-Token': token, 'Content-type': 'application/json'}


def environment_get_id(env_name):
    environments = get_list_of_environments()
    for environment in environments: 
        if environment['name'] == env_name:
            return environment['id']


def get_list_of_environments():
    response = requests.request('GET',
                                url=service_url + '/environments',
                                headers=headers)
    result = response.json()
    return result['environments']


@when('I create environment "{env_name}"')
def environment_create(context, env_name):
    body = json.dumps({"name": env_name})
    url = "%s/environments" % service_url
    result = requests.request('POST', url=url, headers=headers, data=body)
    # result.response_code


@when('I delete environment "{env_name}"')
def environment_delete(context, env_name):
    env_id = environment_get_id(env_name)
    body = json.dumps({"id": env_id})
    url = "%s/environments/%s" % (service_url, env_id)
    result = requests.request('DELETE', url=url, headers=headers)


@when('I update environment "{env_name}" to "{new_name}"')
def environment_action_update(context, env_name, new_name):
    env_id = environment_get_id(context, env_name)
    body = json.dumps({'name': new_name})
    url = '%s/environments/%s' % (service_url, env_id)
    result = requests.request('PUT', url=url, headers=headers, data=body)


@when('I deploy environment "{env_name}"')
def environment_action_deploy(context, env_name):
    env_id = environment_get_id(env_name)

    url = '%s/environments/%s/configure' % (service_url, env_id)
    response = requests.request('POST', url=url, headers=headers)
    session = response.json()

    url = str('%s/environments/%s/sessions/%s/deploy' %
              (service_url, env_id, session['id']))

    result = requests.request('POST', url=url, headers=headers)


@then('environments should {condition} "{param}" {feature}')
def environment_check(context, condition, param, feature):
    if feature == "environment(s)":
        env_list = environment_get_all(context)

        if condition == "contain":
            assert len(env_list) == int(param)
        if condition == "not contain":
            assert len(env_list) != int(param)


@when('I {action} session for environment "{env_name}"')
def session_action(context, action, env_name):
    if action == 'open':
        session_open(context, env_name)
    if action == 'deploy':
        session_deploy(context, env_name)
    if action == 'delete':
        session_delete(context, env_name)
    if action in ['can\'t open', 'can not open']:
        try:
            session_open(context, env_name=env_name)
        except:
            pass


def session_open(env_name):
    env_id = environment_get_id(env_name)

    url = '%s/environments/%s/configure' % (service_url, env_id)
    response = requests.request('POST', url=url, headers=headers)
    result = response.json()
    return result['id']


def session_deploy(env_name):
    env_id = environment_get_id(env_name)

    session_id = session_get_open(env_name, env_id)
    url = '%s/environments/%s/sessions/%s/deploy' % \
                    (service_url, env_id, session_id)

    result = requests.request('POST', url=url, headers=headers)


def session_delete(context, env_name, env_id=None, session_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    url = '%s/environments/%s/sessions/%s' % (service_url, env_id, session_id)
    response = requests.request('DELETE', url=url, headers=headers)
    assert response.status_code is 200


@when('I {action} sessions for environment "{env_name}"')
def session_delete_all(context, action, env_name, env_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    sessions = session_get_all(context, env_name, env_id)
    if action == 'delete all':    
        for session in sessions:
            session_delete(context, env_name, env_id, session['id'])
    if action == 'try delete all':
        try:    
            for session in sessions:
                session_delete(context, env_name, env_id, session['id'])
        except:
            assert True


def session_get_all(context, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)

    url = '%s/environments/%s/sessions' % (service_url, env_id)
    response = requests.request('GET', url=url, headers=headers)
    assert response.status_code is 200
    result = response.json()
    return result['sessions']


def session_get_id_by_state(context, state, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    sessions = session_get_all(context, env_name, env_id)
    for s in sessions:
        if s['state'] == state:
            return s['id']


def session_get_id_by_user(context, user, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    sessions = session_get_all(context, env_name, env_id)
    for s in sessions:
        if s['user'] == user:
            return s['id']


def session_get_open(context, env_name, env_id):
    session_id = session_get_id_by_state(context, 'open', env_name, env_id)
    if session_id is None or len(session_id) is 0 :
       session_id = session_open(context, env_name, env_id)
    return session_id


@then('environment "{env_name}" should {condition} status "{state}"')
@then('environment "{env_name}" should {condition} session "{state}"')
def session_check(context, env_name, condition, state):
    session_id = session_get_id_by_state(context, state, env_name)
    if condition in ['contain', 'have']:
        assert session_id
    if condition in ['not_contain', 'have_not']:
        assert not session_id


@then('environment "{env_name}" should {condition} "{count}" session(s)')
def session_check_count(context,env_name, condition, count):
    sessions = session_get_all(context, env_name)
    if condition == 'contain':
        assert sessions is not None and len(sessions) == int (count)
    if condition == 'not_contain':
        assert sessions is None or len(sessions) != int (count)


@when('I create "{param}" AD(s) for environment "{env_name}"')
def ad_action_create(context, param, env_name):
    if param is None or param == '':
        ad_create(context, env_name)
    else:
        for x in range(int(param)):
            ad_create(context, env_name)


@when('I set AD {item}: "{param}"')
def ad_set_item(context, item, param):
    if item == 'name':
        context.ad.name = param
    if item == 'configuration':
        context.ad.configuration = param
    if item == 'admin password':
        context.ad.adminPassword = param
    if item == 'master unit with location:':
        context.ad.units.append(ADUnit(is_master=True, location=param))
    if item == 'secondary unit with location:':
        context.ad.units.append(ADUnit(is_master=False, location=param))

    if item == 'credentials':
        cred = param.split('\\')
        context.ad.credentials = {'username': cred[0], 'password': cred[1]}


@when('I delete AD "{ad_name}" for environment "{env_name}"')
def ad_delete(context, ad_name, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id

    ad_id = ad_get_id(context, ad_name, env_name, env_id)

    url = ('%s/environments/%s/activeDirectories/%s'
           % (service_url, env_id, ad_id))

    response = requests.request('DELETE', url=url, headers=headers)
    assert response.status_code is 200


@when('I delete all AD for environment "{env_name}"')
def ad_delete_all(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    for ad in ad_get_all(context, env_name, env_id):
        ad_delete(context, ad['name'], env_name, env_id, session_id)


def ad_create(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id

    url = '%s/environments/%s/activeDirectories' % (service_url, env_id)
    body = context.ad.json()

    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    assert response.status_code is 200


@when('I update AD "{ad_name}" for environment "{env_name}"')
def ad_update(context, ad_name, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    headers['X-Configuration-Session'] = session_id
    ad_id = ad_get_id(context, ad_name, env_name, env_id)
    url = '%s/environments/%s/activeDirectories/%s' \
                       % (service_url, env_id, ad_id)
    body = context.ad.json()
    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    assert response.status_code is 200


def ad_get_all(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    headers['X-Configuration-Session'] = session_id
    url = '%s/environments/%s/activeDirectories' % (service_url, env_id)
    response = requests.request('GET', url=url, headers=headers)
    assert response.status_code is 200
    result = response.json()
    return result['activeDirectories']


def ad_get_id(context, ad_name, env_name, env_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    ad_list = ad_get_all(context, env_name, env_id)
    for ad in ad_list:
        if ad['name'] == ad_name:
            return ad['id']


@then('environment "{env_name}" should {condition} AD "{ad_name}"')
def ad_check(context, condition, env_name, ad_name):
    ad_id = ad_get_id(context, ad_name, env_name)
    if condition == "contain":
        assert ad_id
    if condition == "not_contain":
        assert not ad_id


@then('environment "{env_name}" should {condition} "{count}" {service}(s)')
def ad_check_count(context, condition, env_name, count, service):
    if service == 'AD':
        service_list = ad_get_all(context, env_name)
    if service == 'IIS':
        service_list = iis_get_all(context, env_name)    
    if condition == 'contain':
        assert len(service_list) == int(count)
    if condition == 'not_contain':
        assert len(service_list) != int(count)


@when ('I get list of IIS services for environment "{env_name}"') 
@then ('I get list of IIS services for environment "{env_name}"') 
def iis_get_all(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (service_url, env_id)
    response = requests.request('GET', url=url, headers=headers)
    assert response.status_code == 200
    resault = response.json()
    return resault['webServers']


@when('I set IIS {item}: "{param}"')
def iis_set_item(context, item, param):
    if item == 'name':
        context.iis.name = param
    if item == 'domain':
        context.iis.domain = param


@when('I create "{param}" IIS for environment "{env_name}"')
def iis_action_create(context, param, env_name,env_id=None, session_id=None ):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (service_url, env_id)
    body = context.iis.json()
    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    assert response.status_code is 200


@then('environment "{env_name}" should {condition} IIS "{iis_name}"')
@then('environment "{env_name}" should {condition} IIS "{iis_name}" {optional}: "{iis_domain}"')
def iis_check(context, env_name, condition, iis_name, optional=None, iis_domain=None):
    if optional == 'with domain':
        iis_id = iis_get_id(context, iis_name, env_name, iis_domain)
    else:
        iis_id = iis_get_id(context, iis_name, env_name)
    if condition == 'contain':
        assert iis_id
    elif condition == 'not_contain':
        assert not iis_id
    else:
        LOG.error("Bad request - should be 'contain' or 'not_contain'")
        assert false


def iis_get_id(context, iis_name, env_name, iis_domain=None):
    env_id = environment_get_id(context, env_name)
    iis_list = iis_get_all(context, env_name, env_id)
    for iis in iis_list:
        if (iis['name'] == iis_name) and (iis_domain in [iis['domain'], None]):
            return iis['domain']


def iis_get_all(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (service_url, env_id)
    response = requests.request('GET', url=url, headers=headers)
    assert response.status_code is 200
    return response.json()['webServers']


@then('I try to {action} session for environment "{env_name}" without authentication')
def try_session(context, action, env_name, env_id=None, session_id=None):
    env_id = environment_get_id(context, env_name)

    if action == 'open':
        url = '%s/environments/%s/configure' % (service_url, env_id)
    if action == 'deploy':
        session_id = session_get_open(context, env_name, env_id)
        url = '%s/environments/%s/sessions/%s/deploy' % \
                        (service_url, env_id, session_id)

    token = headers['X-Auth-Token']
    headers['X-Auth-Token'] = '12345678903465789346589734'
    response = requests.request('POST', url=url, headers=headers)
    headers['X-Auth-Token'] = token
    assert response.status_code == 401


@then('I try to create AD for environment "{env_name}" without param "{param}"')
def ad_try_create(context, env_name, param, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id
    url = '%s/environments/%s/activeDirectories' % (service_url, env_id)
    body = context.ad.get()

    if param == 'recoveryPassword':
        del body['units'][0]
        del body['units'][0]['recoveryPassword']
    else:
        del body[param]

    body = json.dumps(body)
    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    assert response.status_code == 403
    
    
@then('I try to create environment "{param}" without authentication')
def try_create_env(context, param, env_id=None, session_id=None):
    headers['X-Configuration-Session'] = session_id
    body = json.dumps({"name": param})
    url = "%s/environments" % service_url
    token = headers['X-Auth-Token']
    headers['X-Auth-Token'] = '1234465789346589734'
    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    headers['X-Auth-Token'] = token
    assert response.status_code == 401


@then('I try to create {param} for environment "{env_name}" without authentication')
def try_create(context, param, env_name, env_id=None, session_id=None):
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    headers['X-Configuration-Session'] = session_id

    token = headers['X-Auth-Token']
    if param == 'AD':
        headers['X-Auth-Token'] = '12345678905673784'
        url = '%s/environments/%s/activeDirectories' % (service_url, env_id)
        body = context.ad.json()
        response = requests.request('POST', url=url,
                                    headers=headers,
                                    data=body)
    if param == 'session':
        headers['X-Auth-Token'] = '123453465789346589734'
        url = "%s/environments" % service_url
        response = requests.request('POST', url=url,
                                    headers=headers)
    if param == 'IIS':
        headers['X-Auth-Token'] = '123456789346589734'
        url = '%s/environments/%s/webServers' % (service_url, env_id)
        body = context.iis.json()
        response = requests.request('POST', url=url,
                                    headers=headers,
                                    data=body)
    headers['X-Auth-Token'] = token
    assert response.status_code == 401

        
@then('I try to create IIS for environment "{env_name}" without param "{param}"')
def iis_try_create(context, env_name, param, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    headers['X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (service_url, env_id)
    body = context.iis.get()
    if param in ['username', 'password']:
        del body['credentials'][param]
    else:
        del body[param]
    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    if param == 'domain':
        assert response.status_code is 200
    else:
        assert response.status_code is 403


@then('I try to create {param} for environment "{env_name}" without session ID')
def try_create_wo_session(context, param, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if param == 'AD':
        url = '%s/environments/%s/activeDirectories' % (service_url, env_id)
        body = context.ad.json()
    if param == 'IIS':
        url = '%s/environments/%s/webServers' % (service_url, env_id)
        body = context.iis.json()

    headers['X-Configuration-Session'] = '0.12345789'
    response = requests.request('POST', url=url,
                                headers=headers,
                                data=body)
    assert response.status_code == 403


@then('I try to delete environment "{env_name}" without authentication')
def try_delete_env(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    headers['X-Configuration-Session'] = session_id
    token = headers['X-Auth-Token']
    headers['X-Auth-Token'] = '1234567890567378946593465789346589734'
    body = json.dumps({"id": env_id})
    url = "%s/environments/%s" % (service_url, env_id)
    response = requests.request('DELETE', url=url,
                                headers=headers)
    headers['X-Auth-Token'] = token
    assert response.status_code == 401


@then('I try to get list of environments without authentication')
def try_list_env(context):
    token = headers['X-Auth-Token']
    headers['X-Auth-Token'] = '1234567890567378946593465789346589734'
    url = "%s/environments" % (service_url)
    response = requests.request('GET', url=url,
                                headers=headers)
    headers['X-Auth-Token'] = token
    assert response.status_code == 401


def delete_all_environments():
    environments = get_list_of_environments()
    for environment in environments:
        response = environment_delete(None, environment['name'])

delete_all_environments()
