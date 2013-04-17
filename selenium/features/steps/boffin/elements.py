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
from selenium.webdriver.support.ui import Select

logging.basicConfig()
LOG = logging.getLogger('elements')


class TableCellClass:
    table = None

    def __init__(self, obj):
        if not obj:
            LOG.error('TableCell does not found')
        self.table = obj

    def Text(self):
        if self.table:
            LOG.critical(self.table.text)
            return self.table.text
        else:
            return ''


class ButtonClass:
    button = None

    def __init__(self, obj):
        if not obj:
            LOG.error('Button does not found')
        self.button = obj

    def Click(self):
        if self.button:
            self.button.click()

    def isPresented(self):
        if self.button:
            return True
        return False


class LinkClass:
    link = None

    def __init__(self, obj):
        if not obj:
            LOG.error('Link does not found')
        self.link = obj

    def Click(self):
        if self.link:
            self.link.click()

    def isPresented(self):
        if self.link:
            return True
        return False

    def Address(self):
        if self.link:
            return self.link.get_attribute('href')
        else:
            return ''


class EditBoxClass:

    def __init__(self, obj):
        if not obj:
            LOG.error('EditBox does not found')
        self.edit = obj

    def isPresented(self):
        if self.edit:
            return True
        return False

    def Set(self, value):
        if self.edit:
            try:
                self.edit.clear()
                self.edit.send_keys(value)
            except:
                LOG.error('Can not set value for text box.')

    def Text(self):
        if self.edit:
            return self.edit.get_text()
        else:
            return ''


class DropDownListClass:
    select = None

    def __init__(self, obj):
        if not obj:
            LOG.error('DropDownList does not found')
        self.select = obj

    def isPresented(self):
        if self.select is not None:
            return True
        return False

    def Set(self, value):
        if self.select:
            try:
                Select(self.select).select_by_visible_text(value)
            except:
                message = "Can not select element %s from drop down list."
                LOG.error(message % value)

    def Text(self):
        if self.select:
            return self.select.get_text()
        else:
            return ''
