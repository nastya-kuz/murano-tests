Feature: services details

  Scenario: Check AD service parameters in details
      Given browser with new environment "d_test01" details page
       When I create AD service "ad" with 1 instances
        And I navigate to service "ad" details page
       Then service name should be equal to "ad"
        And service domain should be equal to "ad"

  Scenario: Check IIS service parameters in details
      Given browser with new environment "d_test02" details page
       When I create AD service "ad.test" with 1 instances
        And I create IIS service "iis_service" in domain ad.test
        And I navigate to service "iis_service" details page
       Then service name should be equal to "iis_service"
        And service domain should be equal to "ad.test"