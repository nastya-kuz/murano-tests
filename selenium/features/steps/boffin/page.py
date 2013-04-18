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


import logging
import elements
import objects_library
import dblogger


"""
    Disable selenium logging:
"""
logging.basicConfig()
logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel('ERROR')


error_msg = """
                Object with parameter: %s
                does not found on page.
            """


class Page:

    driver = None
    timeout = 60
    lib = None
    name = None

    def __init__(self, context):
        context.driver.set_page_load_timeout(self.timeout)
        context.driver.implicitly_wait(0.1)
        self.driver = context.driver

        db_host = getattr(context, 'dblogger_host', None)
        context.logger = dblogger.DBLogger(dbhost = db_host)
        self.context = context

    def _find_element(self, name, parameter=None):
        """
            This method allows to find element,
            based on descriptions in Object Library,
            xpath, id, name or pertial link text.
            If parameter != None will be used name % parameter
        """

        lib_name = "objects/objects.xml"
        if self.name:
            lib_name = "objects/%s.xml" % self.name
        lib = objects_library.ObjectsLibrary(lib_name)

        if lib.get_object(name):
            name = lib.get_object(name)

        if parameter:
            name = name % parameter

        obj = None
        k = 0

        while (obj is None and k < self.timeout):
            k += 1

            try:
                obj = self.driver.find_element_by_name(name)
                return obj
            except:
                pass
            try:
                obj = self.driver.find_element_by_id(name)
                return obj
            except:
                pass
            try:
                obj = self.driver.find_element_by_xpath(name)
                return obj
            except:
                pass
            try:
                obj = self.driver.find_element_by_partial_link_text(name)
                return obj
            except:
                pass

        self.context.logger.error(error_msg % name)
        return None

    def Open(self, url):
        self.driver.get(url)

    def Refresh(self):
        self.driver.refresh()

    def TableCell(self, name, parameter=None):
        obj = self._find_element(name, parameter)
        table = elements.TableCellClass(obj)
        return table

    def Button(self, name, parameter=None):
        obj = self._find_element(name, parameter)
        button = elements.ButtonClass(obj)
        return button

    def Link(self, name, parameter=None):
        obj = self._find_element(name, parameter)
        link = elements.LinkClass(obj)
        return link

    def EditBox(self, name, parameter=None):
        obj = self._find_element(name, parameter)
        edit = elements.EditBoxClass(obj)
        return edit

    def DropDownList(self, name, parameter=None):
        obj = self._find_element(name, parameter)
        select = elements.DropDownListClass(obj)
        return select

    def Navigate(self, path):
        """
            This method allows to navigate by
            webUI menu button and links to
            the specific page
        """
        steps = path.split('>')

        for step in steps:
            self.Button(step).Click()

        self.driver.refresh()
