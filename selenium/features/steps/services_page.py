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

import boffin.page as page
import re


class ServicesPage(page.Page):
    
    name = 'Services'

    def create_service(self, service_type, parameters):
        self.Button('CreateService').Click()
        self.DropDownList('0-service').Set(service_type)
        self.Button('wizard_goto_step').Click()

        for key in parameters:
            try:
                self.EditBox(key).Set(parameters[key])
            except:
                self.DropDownList(key).Set(parameters[key])
        self.Button('Create').Click()

    def delete_service(self, name):
        link = self.Link(name).Address()

        service_id = re.search('tabula/(\S+)', link).group(0)[7:-1]

        self.Button('More', service_id).Click()
        self.Button('Delete', service_id).Click()
        # confirm:
        self.Button('Delete Service').Click()

    def get_service_status(self, name):
        link = self.Link(name).Address()
        service_id = re.search('tabula/(\S+)', link).group(0)[7:-8]

        return self.TableCell('Status', service_id).Text()
