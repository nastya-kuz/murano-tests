#!/usr/bin/python
# -*- coding: utf-8 -*-
# import requests
# import json

import logging, json, random
from behave import *

import ConfigParser
# import json

CONFIG_PATH = 'config.ini'
adminPassword = 'SwordFish_1'
recoveryPassword='SwordFish_2'


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
    context.CONFIG = init_config()
    context.url = context.CONFIG.get(u'keero', u'url')
    context.keero_id = context.CONFIG.get(u'keystone', u'x-auth-token')
    context.headers = {u'X-Auth-Token': context.keero_id,
                       u'Content-type': u'application/json'}

    context.ad = AD()
    context.iis = IIS()


class AD:

    name = "%s.ad-dc" % random.randint(1, 100)
    domain = name
    configuration = 'standalone'
    units = []
    adminPassword = 'SwordFish_1' # passwords._generate_salt(8)

    def __init__(self , units='', name='acme.dc'):
        self.name = name
        if units == '':
            self.units.append(ADUnit(is_master=True, location="west-dc").get())
            self.units.append(ADUnit(is_master=False, location="east-dc").get())
        else:    
            self.units = units


    def get(self):
        return          {'name'             :   self.name,
                         'domain'           :   self.domain,
                         'configuration'    :   self.configuration,
                         'adminPassword'    :   adminPassword,
                         'units'            :   self.units		}
    def json(self):
         return json.dumps(self.get())


class ADUnit:

    isMaster = True
    location = "%s street" % random.randint(1, 100)
    recoveryPassword = 'SwordFish_1'

    def __init__(self, is_master, location):
        self.isMaster = is_master
        self.location = location

    def get(self):
	return dict(location=self.location,
		      isMaster=self.isMaster,
		      recoveryPassword=recoveryPassword)


class IIS:

    name = "%s-iis" % random.randint(1, 100)
    domain = name
    units = []
    credentials = {}

    def __init__(self , units='', name='acme.dc'):
        self.name = name
        self.credentials['username'] = 'admin'
        self.credentials['password'] = 'swordfish'
        if units == '':
            self.units.append(IISUnit(location="west-dc").get())
        else:    
            self.units = units

    def get(self):
        iis = {'name': self.name, 'domain': self.domain,
               'units': self.units, 'credentials': self.credentials}
        return iis

    def json(self):
         return json.dumps(self.get())


class IISUnit:

    location = "%s.dc" % random.randint(1, 100)
    endpoint = dict(host='10.0.0.%s'%random.randint(1, 254))

    def __init__(self, location='', endpoint=''):
        if location != '':
            self.location = location
        if endpoint != '':
            self.endpoint = endpoint

    def get(self):
        return dict(location=self.location)

    def json(self):
        return json.dumps(self.get()) 
