murano-tests
============

 The functional and performance tests for OpenStack Murano project.

 Functional tests are based on behave framework, performance tests are based on FunkLoad framework.
<br><br>

How To Run Tests For Web UI
============

 The web UI tests allow to perform complex integrational testing with REST API service, REST API client, archestrator component and Murano dashboard component.
 The simplest way to execute webUI tests is to run tox.
<br><br>

How To Run Functional Tests For REST API service
============
 To run all functional tests for REAT API service need to run behave with the following command:

   # cd murano-tests/rest_api_tests/functional <br>
   # behave rest_api_service.feature <br>

 Note: need to set the correct configuration for REST API service. (please, check config.ini file for more detailed information)
<br><br>

How To Run Performance Tests For REST API service
============
 To run all performance tests for REAT API service need to run func load banch with the following command:

   # cd murano-tests/rest_api_tests/load_and_performance <br>
   # fl-run-bench test_rest.py TestSuite.mix_for_load_testing <br>
   # fl-build-report --html --output-directory=html result-bench.xml <br>
<br>
 After that we can find the html report in the same folder.
<br>
 Note: need to set the correct configuration for REST API service. (please, check config.ini file for more detailed information)
<br><br><br>



 Mirantis Inc (C) 2013.
