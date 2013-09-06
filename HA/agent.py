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

import shlex
import subprocess
import filecmp
import xmlrpclib
import time
from SimpleXMLRPCServer import SimpleXMLRPCServer

"""
    This is simple XML-RPC server which can:
      1. Execute any shell commands by the request
      2. Compare two files

    This server should be run on OpenStack controller nodes
    to control services on these nodes.
"""


def run_bash_command(cmd, timeout=0):
    args = shlex.split(cmd)
    p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
    for line in p.stdout:
        print line
    time.sleep(timeout)
    return p.stdout


def check_diff_files(file1, file2):
    return not filecmp.cmp(file1, file2)


server = SimpleXMLRPCServer(("0.0.0.0", 7007),allow_none=True)
print "Listening on port 7007..."
server.register_function(run_bash_command, "run_bash_command")
server.register_function(check_diff_files, "check_diff_files")

server.serve_forever()
