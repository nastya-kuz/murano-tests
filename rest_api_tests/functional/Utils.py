#    Copyright (c) 2013 Mirantis, Inc.
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

from ConfigParser import ConfigParser
from os import getcwd
from os.path import join
from bs4 import BeautifulSoup


class ArtificialIntelligence:
    """
    This class allows to find input and select controls
    without manual input of identificators.
    We can find input fields by labels near those fields
    """

    def __init__(self, page_source):
        """
        Class constructor.

        Arguments:
            - page_source: web page source code.

        Return:
            - None.
        """
        self.page_source = page_source

    def _get_xpath_of_element(self, element):
        """
        This function allows to get xpath of soup elements.

        Arguments:
            - element: selector name.

        Return:
            - element xpath.
        """

        number = 1
        try:
            number += len(element.find_previous_siblings(element.name))
        except:
            pass

        xpath = element.name + '[' + str(number) + ']'

        for parent in element.findParents():
            if parent.name != '[document]':
                k = 0
                for tag in parent.find_previous_siblings():
                    if tag.name == parent.name:
                        k += 1
                if k == 0:
                    xpath = parent.name + '/' + xpath
                else:
                    xpath = parent.name + '[' + str(k + 1) + ']/' + xpath
        print xpath
        return xpath

    def extra_search(self, soup, label_element, element_type, value):
        """
        This function allows to get element by its parameters.

        Arguments:
            - soup: soup structure;
            - label_element: element with specified name;
            - element_type: element tag name;
            - value: element name.

        Return:
            - label_element.
        """
        elements_types = element_type.split('/')

        for t in elements_types:
            if not label_element:
                label_element = soup.find(t, text=str(value))
            if not label_element:
                label_element = soup.find(t, attrs={'value': value})
            if not label_element:
                label_element = soup.find(t, attrs={'title': value})
            if not label_element:
                try:
                    element = soup.find(text=str(value))
                    label_element = element.parent.\
                                      find_next(text=str(element_type))
                except:
                    pass
            if not label_element:
                try:
                    element = soup.find(text=str(value))
                    print element
                    label_element = element.parent.\
                                      find_previous(text=str(element_type)).parent
                    print label_element
                except:
                    pass
                print label_element

        return label_element

    def find_element(self, label, element_type='input', method='next'):
        """
        Looks for specified element on the page.

        Arguments:
            - label: selector name;
            - element_type: element tag name. It could be any tag or several
             tags (then they are listed as 'select/input/a');
            - method: element search method. If 'next' is set, then function
             is looking for the next input field after the specified element.
             Otherwise it returns the specified element itself.

        Return:
            - element xpath.

        Examples:
        | ${xpath} | Find element | E-mail | input | next |
        | ${xpath} | Find element | Cancel | a/div | this |
        """
        html = str(self.page_source.encode("utf-8", "replace"))

        " load html to soup structure for parsing "
        soup = BeautifulSoup(html)

        " search element after the label"
        try:
            if method == 'next':
                label_element = soup.find(text=str(label))
                label_element = self.extra_search(soup, label_element,
                                                  element_type, label)
                element = label_element.parent.find_next(element_type)
            elif method == 'previous':
                label_element = soup.find(text=str(label))
                label_element = self.extra_search(soup, label_element,
                                                  element_type, label)
                element = label_element.parent.find_previous(element_type)
            else:
                label_element = soup.find(element_type, text=str(label))
                element = self.extra_search(soup, label_element,
                                            element_type, label)
            " return xpath of element "
            return self._get_xpath_of_element(element)
        except:
            return ""


_objRepoFileName = join(getcwd(), 'resources', 'ObjRepo.ini')


class Utils(object):
    """ Boffin heart. """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    __version__ = '0.1'

    def get_element_from_repo(self, element_name):
        """
        Returns element type, identificator and frame from
        the 'resources/ObjRepo.ini' file by element name.

        Arguments:
            - elementName: selector name.

        Return:
            - <list> [elType, elIdentificator, elFrame].

        Example:
        | ${element} | Get Element From Repo | Banner Page 2 Button |
        Will return
        [xpath, //div[@class='bx-pager']/a[contains(@class, 'pager-2')]]
        """
        try:
            name = element_name.lower().replace(' ', '')

            conf = ConfigParser()
            conf.read(_objRepoFileName)

            element_type = conf.get(name, 'type')
            element_identificator = conf.get(name, 'identificator')
            element_frame = conf.get(name, 'frame')
            return [element_type, element_identificator, element_frame]
        except:
            return ['', None, '']

    def get_element_frame(self, elementName):
        """
        Returns element frame by its name in the 'resources/ObjRepo.ini' file.

        Arguments:
            - elementName: selector name.

        Return:
            - elFrame.

        Example:
        | ${elFrame} | GetElementFrame | Post Text field |
        Will return 'posteditorframe'.
        """
        result = self.get_element_from_repo(elementName)
        if len(result) > 1:
            return result[2]

    def get_element_selector(self, name, page_source=None,
                             element_type='input', method='next'):
        """
        Returns element selector by its name in the
        'resources/ObjRepo.ini' file.

        Arguments:
            - name: selector name;
            - page_source: web page source code;
            - element_type: element tag name. It could be any tag or several
             tags (then they are listed as 'select/input/a');
            - method: element search method. If 'next' is set, then function
             is looking for the next input field after the specified element.
             Otherwise it returns the specified element itself.

        Return:
            - elIdentificator.

        Examples:
        | ${selector} | Get element selector | User Name | ${source_code} \
        | input | next |
        | ${selector} | Get element selector | Submit Button | ${source_code} \
        | a | this |
        """
        _type, _id, _frame = self.get_element_from_repo(name)

        if not _id and page_source:
            _frame = ''
            boffin = ArtificialIntelligence(page_source)
            _id = boffin.find_element(name, element_type, method)
            if _id:
                _type = 'xpath'

        prefix = '' if _type == '' else str(_type) + '='

        return prefix + str(_id)
