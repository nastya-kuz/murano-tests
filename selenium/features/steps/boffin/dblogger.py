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
from log4mongo.handlers import MongoHandler


class DBLogger:
    """
        This class allows to save all log messages to the data base
        based on Mango DB - it is the simple data base with good interfaces.
        Please, see for more detailed information:
        https://github.com/log4mongo
    """

    logger = None
    test_suite = "Test Suite"
    test_case = "Test Case"

    def __init__(self, dbhost = 'localhost'):
        """
            Initialization of the Data Base Logger.
            if dbhost == None this class will not use Data Base.
        """
        self.logger = logging.getLogger('DBLogger')

        if dbhost:
            self.logger.addHandler(MongoHandler(host=dbhost))

    def test_suite_start(self, suite_name):
        self.test_suite = str(suite_name)
        self.logger.info("Test Suite started.",
                         extra={'suite_name': self.test_suite})

    def test_suite_finish(self):
        self.logger.info("Test Suite finished.",
                         extra={'suite_name': self.test_suite})

    def test_case_start(self, test_case_name):
        self.test_case = str(test_case_name)
        self.logger.info("Test Case started.",
                         extra={'test_case_name': self.test_case,
                                'test_suite': self.test_suite})

    def test_case_finish(self, result='PASSED'):
        self.logger.info("Test Case finished.",
                         extra={'test_case_name': self.test_case,
                                'test_suite': self.test_suite,
                                'result': str(result)})

    def save_screenshot(self, base64_screenshot):
        " This function allow to save screenshots in database "
        self.logger.info("Screenshot",
                         extra={'test_suite': self.test_suite,
                                'test_case': self.test_case,
                                'screenshot': str(base64_screenshot)})

    def info(self, message):
        " wrapper for standard logger interface "
        self.logger.info(message,
                         extra={'test_suite': self.test_suite,
                                'test_case': self.test_case})

    def debug(self, message):
        " wrapper for standard logger interface "
        self.logger.debug(message,
                          extra={'test_suite': self.test_suite,
                                 'test_case': self.test_case})

    def warning(self, message):
        " wrapper for standard logger interface "
        self.logger.warning(message,
                            extra={'test_suite': self.test_suite,
                                   'test_case': self.test_case})

    def critical(self, message):
        " wrapper for standard logger interface "
        self.logger.critical(message,
                             extra={'test_suite': self.test_suite,
                                    'test_case': self.test_case})

    def error(self, message):
        " wrapper for standard logger interface "
        self.logger.error(message,
                          extra={'test_suite': self.test_suite,
                                 'test_case': self.test_case})
