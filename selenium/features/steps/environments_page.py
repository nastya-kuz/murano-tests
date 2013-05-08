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

import re
from services_page import ServicesPage
import boffin.page as page


class EnvironmentsPage(page.Page):
    name = 'Environments'

    def create_environment(self, name):
        self.Button('Create Environment').Click()
        self.EditBox('id_name').Set(name)
        self.Button('Create').Click()

    def delete_environment(self, name):
        link = self.Link(name).Address()
        environment_id = re.search('tabula/(\S+)', link).group(0)[7:-1]

        self.Button('More', environment_id).Click()
        self.Button('Delete', environment_id).Click()
        # confirm:
        self.Button('Delete Environment').Click()

    def deploy_environment(self, name):
        link = self.Link(name).Address()
        environment_id = re.search('tabula/(\S+)', link).group(0)[7:-1]

        self.Button('More', environment_id).Click()
        self.Button('Deploy', environment_id).Click()

    def get_environment_status(self, name):
        link = self.Link(name).Address()
        environment_id = re.search('tabula/(\S+)', link).group(0)[7:-1]

        return self.TableCell('Status', environment_id).Text()
