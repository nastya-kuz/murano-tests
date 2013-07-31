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

import xmlrpclib
import ConfigParser
import time


class ControllerNode():

    def __init__(self, status='on', host='', port='7007', file1='', file2='',
                 activate_cmd='', diactivate_cmd='', agent=None):
        self.status = status
        self.host = host
        self.port = port
        self.file1 = file1
        self.file2 = file2
        self.activate_cmd = activate_cmd
        self.diactivate_cmd = diactivate_cmd
        self.agent = agent
        self.checks_timeout = -1

    def check_files(self, access):
        self.checks_timeout -= 1
	if self.checks_timeout == 0:
            self.activate()
            return 1

        if self.agent.check_diff_files(self.file1, self.file2) and access:
            self.diactivate()
            return -1

        return 0

    def activate(self, timeout=5):
        print 'Start to activate node ' + self.host
        init_cmd = 'cp %s %s' % (self.file1, self.file2)
        self.agent.run_bash_command(self.activate_cmd)
        time.sleep(timeout)
        self.agent.run_bash_command(init_cmd)

    def diactivate(self, timeout=5):
        print 'Start to diactivate node ' + self.host
        time.sleep(timeout)
        self.agent.run_bash_command(self.diactivate_cmd)
        self.checks_timeout = 10


class Controller():

    nodes = []

    def __init__(self, config_file='controller.conf'):
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)

        self.agents_list = self.get_from_cfg('HA_Testing', 'nodes').split(' ')
        self.port = self.get_from_cfg('HA_Testing', 'port', '7007')

        self.activate_cmd = self.get_from_cfg('HA_Testing', 'activate_cmd')
        self.diactivate_cmd = self.get_from_cfg('HA_Testing', 'diactivate_cmd')

        self.mode = self.get_from_cfg('HA_Testing', 'mode', 'compare_files')
        self.file1 = self.get_from_cfg('HA_Testing', 'file1')
        self.file2 = self.get_from_cfg('HA_Testing', 'file2')

        parameter = 'minimum_count_of_active_nodes'
        self.min_active_nodes = self.get_from_cfg('HA_Testing',
                                                  parameter, 1)

        for agent in self.agents_list:
            host = self.get_from_cfg(agent, 'host')
            port = self.get_from_cfg(agent, 'port', self.port)
            file1 = self.get_from_cfg(agent, 'file1', self.file1)
            file2 = self.get_from_cfg(agent, 'file2', self.file2)
            activate_cmd = self.get_from_cfg(agent, 'activate_cmd',
                                             self.activate_cmd)
            diactivate_cmd = self.get_from_cfg(agent, 'diactivate_cmd',
                                               self.diactivate_cmd)

            new_agent = xmlrpclib.ServerProxy("http://%s:%s"
                                              % (host, port), allow_none=True)

            new_node = ControllerNode('on', host, port, file1, file2,
                                      activate_cmd, diactivate_cmd, new_agent)

            new_node.activate()
            " If all OK, add this node to the list "
            self.nodes.append(new_node)

        self.active_nodes = len(self.nodes)
        print 'Minimal count of active nodes: ' + str(self.min_active_nodes)
        print 'Active nodes: ' + str(self.active_nodes)

    def get_from_cfg(self, p1, p2, default=''):
        try:
            result = self.config.get(p1, p2)
            return result
        except:
            return default

    def execute(self):
        if 'compare_files' in self.mode:
            self.monitor_file_changes()

    def monitor_file_changes(self):
        while self.active_nodes != self.min_active_nodes:
            for node in self.nodes:
                access = int(self.active_nodes) > int(self.min_active_nodes)
                self.active_nodes += node.check_files(access)


ctrl = Controller()
ctrl.execute()
