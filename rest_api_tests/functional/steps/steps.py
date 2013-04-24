import requests
import json
import logging

LOG = logging.getLogger(__name__)

def environment_get_id(context, env_name):
    for e in environment_get_all(context): 
        if e[u'name'] == env_name:
            return e[u'id']


def environment_get_all(context):
    response = requests.request('GET',
                                url=context.url + '/environments',
                                headers=context.headers)
    assert response.status_code is 200
    result = response.json()
    return result['environments']


def environment_delete(context,env_id):
    body = json.dumps({"id": env_id})
    url = "%s/environments/%s" % (context.url, env_id)
    response = requests.request('DELETE', url=url,
                                headers=context.headers)
    assert response.status_code is 200


@when(u'I create environment "{env_name}"')
def environment_action_create(context, env_name):
    body = json.dumps({"name": env_name})
    url = "%s/environments" % context.url
    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code is 200


@when(u'I delete environment "{env_name}"')
def environment_action_delete(context, env_name):
    env_id = environment_get_id(context, env_name)
    if env_id:
        environment_delete(context, env_id)
    else:
        LOG.debug('Cannot delete environment '+env_name+' - nothing to delete')


@when(u'I delete all environments')
def environment_delete_all(context):
    for env in environment_get_all(context):
        response = environment_delete(context, env['id']) 


@when(u'I update environment "{env_name}" to "{env_new_name}"')
def environment_action_update(context, env_name, env_new_name):
    env_id = environment_get_id(context, env_name)
    body = json.dumps({u'name': env_new_name})
    url = '%s/environments/%s' % (context.url, env_id)
    response = requests.request(u'PUT', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code is 200


@when(u'I deploy environment "{env_name}"')
@then(u'I deploy environment "{env_name}"')
def environment_action_deploy(context, env_name):
    session_deploy(context, env_name)


@then(u'environments should {condition} "{param}" {feature}')
def environment_check(context, condition, param, feature):
    if feature == "environment(s)":
        env_list = environment_get_all(context)

        if condition == "contain":
            assert len(env_list) == int(param)
        if condition == "not contain":
            assert len(env_list) != int(param)


@when(u'I {action} session for environment "{env_name}"')
def session_action(context, action, env_name):
    if action == u'open':
        session_open(context, env_name)
    if action == u'deploy':
        session_deploy(context, env_name)
    if action == u'delete':
        session_delete(context, env_name)
    if action in [u'can\'t open', u'can not open']:
        try:
            session_open(context, env_name=env_name)
        except:
            pass


def session_open(context, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)

    url = '%s/environments/%s/configure' % (context.url, env_id)
    response = requests.request('POST', url=url, headers=context.headers)
    assert response.status_code is 200
    env_session_id = response.json()[u'id']

    if len(env_session_id) is not 0:
        context.CONFIG.set(u'keero',
                           u'x-configuration-session',
                           env_session_id)
        context.session_id = env_session_id
        return env_session_id
    else:
        assert False


def session_deploy(context, env_name, env_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    session_id = session_get_open(context, env_name, env_id)

    url = '%s/environments/%s/sessions/%s/deploy' % \
                    (context.url, env_id, session_id)
    context.headers[u'X-Configuration-Session'] = session_id

    response = requests.request('POST', url=url, headers=context.headers)
    assert response.status_code is 200


def session_delete(context, env_name, env_id=None, session_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    url = '%s/environments/%s/sessions/%s' % (context.url, env_id, session_id)
    response = requests.request('DELETE', url=url, headers=context.headers)
    context.LOG.debug("session delete all response:%s"% response._content)
    assert response.status_code is 200


@when(u'I {action} sessions for environment "{env_name}"')
def session_delete_all(context, action, env_name, env_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    sessions = session_get_all(context, env_name, env_id)
    if action == u'delete all':    
        for session in sessions:
            session_delete(context, env_name, env_id, session[u'id'])
    if action == u'try delete all':
        try:    
            for session in sessions:
                session_delete(context, env_name, env_id, session[u'id'])
        except:
            assert True


def session_get_all(context, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)

    url = '%s/environments/%s/sessions' % (context.url, env_id)
    response = requests.request('GET', url=url, headers=context.headers)
    assert response.status_code is 200
    result = response.json()
    return result[u'sessions']


def session_get_id_by_state(context, state, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    sessions = session_get_all(context, env_name, env_id)
    for s in sessions:
        if s[u'state'] == state:
            return s[u'id']


def session_get_id_by_user(context, user, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    sessions = session_get_all(context, env_name, env_id)
    for s in sessions:
        if s[u'user'] == user:
            return s[u'id']


def session_get_open(context, env_name, env_id):
    session_id = session_get_id_by_state(context, u'open', env_name, env_id)
    if session_id is None or len(session_id) is 0 :
       session_id = session_open(context, env_name, env_id)
    return session_id


@then(u'environment "{env_name}" should {condition} status "{state}"')
@then(u'environment "{env_name}" should {condition} session "{state}"')  # @UndefinedVariable
def session_check(context, env_name, condition, state):
    session_id = session_get_id_by_state(context, state, env_name)
    if condition in [u'contain', u'have']:
        assert session_id
    if condition in [u'not_contain', u'have_not']:
        assert not session_id


@then(u'environment "{env_name}" should {condition} "{count}" session(s)')
def session_check_count(context,env_name, condition, count):
    sessions = session_get_all(context, env_name)
    if condition == u'contain':
        assert sessions is not None and len(sessions) == int (count)
    if condition == u'not_contain':
        assert sessions is None or len(sessions) != int (count)


@when(u'I create "{param}" AD(s) for environment "{env_name}"')
def ad_action_create(context, param, env_name):
    if param is None or param == '':
        ad_create(context, env_name)
    else:
        for x in range(int(param)):
            ad_create(context, env_name)


@when(u'I set AD {item}: "{param}"')
def ad_set_item(context, item, param):
    if item == u'name':
        context.ad.name = param
    if item == u'configuration':
        context.ad.configuration = param
    if item == u'admin password':
        context.ad.adminPassword = param
    if item == u'master unit with location:':
        context.ad.units.append(ADUnit(is_master=True, location=param))
    if item == u'secondary unit with location:':
        context.ad.units.append(ADUnit(is_master=False, location=param))

    if item == u'credentials':
        cred = param.split('\\')
        context.ad.credentials = {'username': cred[0],
                                  'password': cred[1]}


@when(u'I delete AD "{ad_name}" for environment "{env_name}"')
def ad_delete(context, ad_name, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id

    ad_id = ad_get_id(context, ad_name, env_name, env_id)

    url = ('%s/environments/%s/activeDirectories/%s'
            % (context.url, env_id, ad_id))

    response = requests.request('DELETE', url=url, headers=context.headers)
    assert response.status_code is 200


@when(u'I delete all AD for environment "{env_name}"')
def ad_delete_all(context, env_name, env_id=None, session_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    for ad in ad_get_all(context, env_name, env_id):
        ad_delete(context, ad[u'name'], env_name, env_id, session_id)


def ad_create(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id

    url = '%s/environments/%s/activeDirectories' % (context.url, env_id)
    body = context.ad.json()

    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code is 200


@when(u'I update AD "{ad_name}" for environment "{env_name}"')
def ad_update(context, ad_name, env_name, env_id=None, session_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    context.headers[u'X-Configuration-Session'] = session_id
    ad_id = ad_get_id(context, ad_name, env_name, env_id)
    url = '%s/environments/%s/activeDirectories/%s' \
            % (context.url, env_id, ad_id)
    body = context.ad.json()
    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code is 200


def ad_get_all(context, env_name, env_id=None, session_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    context.headers[u'X-Configuration-Session'] = session_id
    url = '%s/environments/%s/activeDirectories' % (context.url, env_id)
    response = requests.request('GET', url=url, headers=context.headers)
    assert response.status_code is 200
    result = response.json()
    return result[u'activeDirectories']


def ad_get_id(context, ad_name, env_name, env_id=None):
    if  env_id is None:
        env_id = environment_get_id(context, env_name)
    ad_list = ad_get_all(context, env_name, env_id)
    for ad in ad_list:
        if ad[u'name'] == ad_name:
            return ad[u'id']


@then(u'environment "{env_name}" should {condition} AD "{ad_name}"')
def ad_check(context, condition, env_name, ad_name):
    ad_id = ad_get_id(context, ad_name, env_name)
    if condition == "contain":
        assert ad_id
    if condition == "not_contain":
        assert not ad_id


@then(u'environment "{env_name}" should {condition} "{count}" {service}(s)')
def ad_check_count(context, condition, env_name, count, service):
    if service == u'AD':
        service_list = ad_get_all(context, env_name)
    if service == u'IIS':
        service_list = iis_get_all(context, env_name)    
    if condition == u'contain':
        assert len(service_list) == int (count)
    if condition == u'not_contain':
        assert len(service_list) != int (count)


@when (u'I get list of IIS services for environment "{env_name}"') 
@then (u'I get list of IIS services for environment "{env_name}"') 
def iis_get_all(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (context.url, env_id)
    response = requests.request('GET', url=url, headers=context.headers)
    assert response.status_code == 200
    resault = response.json()
    return resault[u'webServers']


@when(u'I set IIS {item}: "{param}"')
def iis_set_item(context, item, param):
    if item == u'name':
        context.iis.name = param
    if item == u'domain':
        context.iis.domain = param


@when(u'I create "{param}" IIS for environment "{env_name}"')
def iis_action_create(context, param, env_name,env_id=None, session_id=None ):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (context.url, env_id)
    body = context.iis.json()
    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code is 200


@then(u'environment "{env_name}" should {condition} IIS "{iis_name}"')
@then(u'environment "{env_name}" should {condition} IIS "{iis_name}" {optional}: "{iis_domain}"')
def iis_check(context, env_name, condition, iis_name, optional=None, iis_domain=None):
    if optional == u'with domain':
        iis_id = iis_get_id(context, iis_name, env_name, iis_domain)
    else:
        iis_id = iis_get_id(context, iis_name, env_name)
    if condition == u'contain':
        assert iis_id
    elif condition == u'not_contain':
        assert not iis_id
    else:
        LOG.error("Bad request - should be 'contain' or 'not_contain'")
        assert false


def iis_get_id(context, iis_name, env_name, iis_domain=None):
    env_id = environment_get_id(context, env_name)
    iis_list = iis_get_all(context, env_name, env_id)
    for iis in iis_list:
        if (iis[u'name'] == iis_name) and (iis_domain in [iis[u'domain'], None]):
            return iis[u'domain']


def iis_get_all(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (context.url, env_id)
    response = requests.request('GET', url=url, headers=context.headers)
    assert response.status_code is 200
    return response.json()[u'webServers']


@then(u'I try to {action} session for environment "{env_name}" without authentication')
def try_session(context, action, env_name, env_id=None, session_id=None):
    env_id = environment_get_id(context, env_name)

    if action == u'open':
        url = '%s/environments/%s/configure' % (context.url, env_id)
    if action == u'deploy':
        session_id = session_get_open(context, env_name, env_id)
        url = '%s/environments/%s/sessions/%s/deploy' % (context.url, env_id, session_id)

    token = context.headers[u'X-Auth-Token']
    context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
    response = requests.request('POST', url=url, headers=context.headers)
    context.headers[u'X-Auth-Token'] = token
    assert response.status_code == 401


@then(u'I try to create AD for environment "{env_name}" without param "{param}"')
def ad_try_create(context, env_name, param, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id
    url = '%s/environments/%s/activeDirectories' % (context.url, env_id)
    body = context.ad.get()
    if param == u'configuration':
        del body['configuration']
    if param == u'adminPassword':
        del body['adminPassword']
    if param == u'domain':
        del body['domain']
    if param == u'units':
        del body['units']
    if param == u'name':
        del body['name']
    if param == u'recoveryPassword':
        del body['units'][0]
        del body['units'][0]['recoveryPassword']

    body = json.dumps(body)
    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code == 403
    
    
@then(u'I try to create environment "{param}" without authentication')
def try_create_env(context, param, env_id=None, session_id=None):
    context.headers[u'X-Configuration-Session'] = session_id
    body = json.dumps({"name": param})
    url = "%s/environments" % context.url
    token = context.headers[u'X-Auth-Token']
    context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
    response = requests.request('POST', url=url,
                            headers=context.headers,
                            data=body)
    context.headers[u'X-Auth-Token'] = token
    assert response.status_code == 401


@then(u'I try to create {param} for environment "{env_name}" without authentication')
def try_create(context, param, env_name, env_id=None, session_id=None):
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    context.headers[u'X-Configuration-Session'] = session_id

    token = context.headers[u'X-Auth-Token']
    if param == u'AD':
        if not env_id:
            env_id = environment_get_id(context, env_name)
        if not session_id:
            session_id = session_get_open(context, env_name, env_id)
        context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
        url = '%s/environments/%s/activeDirectories' % (context.url, env_id)
        body = context.ad.json()
        response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    if param == u'session':
        context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
        url = "%s/environments" % context.url
        response = requests.request('POST', url=url,
                                headers=context.headers)
    if param == u'IIS':
        if not env_id:
            env_id = environment_get_id(context, env_name)
        if not session_id:
            session_id = session_get_open(context, env_name, env_id)
        context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
        url = '%s/environments/%s/webServers' % (context.url, env_id)
        body = context.iis.json()
        response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    context.headers[u'X-Auth-Token'] = token
    assert response.status_code == 401

        
@then(u'I try to create IIS for environment "{env_name}" without param "{param}"')
def iis_try_create(context, env_name, param, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)

    context.headers[u'X-Configuration-Session'] = session_id
    url = '%s/environments/%s/webServers' % (context.url, env_id)
    body = context.iis.get()
    if param == u'credentials':
        del body['credentials']
    if param == u'username':
        del body['credentials']['username'] 
    if param == u'password':
        del body['credentials']['password'] 
    if param == u'domain':
        del body['domain']
    if param == u'units':
        del body['units']
    if param == u'name':
        del body['name']
    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    if param == u'domain':
        assert response.status_code is 200
    else:
        assert response.status_code is 403


@then(u'I try to create {param} for environment "{env_name}" without session ID')
def try_create_wo_session(context, param, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)

    if param == u'AD':
        url = '%s/environments/%s/activeDirectories' % (context.url, env_id)
        body = context.ad.json()
    if param == u'IIS':
        url = '%s/environments/%s/webServers' % (context.url, env_id)
        body = context.iis.json()

    context.headers[u'X-Configuration-Session'] = '0.12345789'
    response = requests.request('POST', url=url,
                                headers=context.headers,
                                data=body)
    assert response.status_code == 403


@then(u'I try to delete environment "{env_name}" without authentication')
def try_delete_env(context, env_name, env_id=None, session_id=None):
    if not env_id:
        env_id = environment_get_id(context, env_name)
    if not session_id:
        session_id = session_get_open(context, env_name, env_id)
    context.headers[u'X-Configuration-Session'] = session_id
    token = context.headers[u'X-Auth-Token']
    context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
    body = json.dumps({"id": env_id})
    url = "%s/environments/%s" % (context.url, env_id)
    response = requests.request('DELETE', url=url,
                                headers=context.headers)
    context.headers[u'X-Auth-Token'] = token
    assert response.status_code == 401


@then(u'I try to get list of environments without authentication')
def try_list_env(context):
    token = context.headers[u'X-Auth-Token']
    context.headers[u'X-Auth-Token'] = '1234567890567378946593465789346589734'
    url = "%s/environments" % (context.url)
    response = requests.request('GET', url=url,
                                headers=context.headers)
    context.headers[u'X-Auth-Token'] = token
    assert response.status_code == 401
