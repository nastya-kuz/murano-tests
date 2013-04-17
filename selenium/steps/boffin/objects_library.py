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


import xml.etree.ElementTree as ET


class ObjectsLibrary:
    file = None
    objects = []

    def __init__(self, file_name='objects/objects.xml'):
        """
            Initialization of the Objects Library.
            Read objects descriptions from XML file.
        """
        self.file = file_name
        tree = ET.parse(self.file)
        objects = tree.getroot()
        self.objects = []
        for element in objects:
            obj = {}
            for parameter in element:
                obj.update({parameter.tag: parameter.text})
            self.objects.append(obj)

    def get_object(self, name):
        """
            Search objects in Objects Library.
        """

        for object in self.objects:
            if object['name'] == name:
                return object['parameter']
        return None
