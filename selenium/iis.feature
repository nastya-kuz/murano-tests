Feature: IIS service

  Scenario: Create IIS service without domain
      Given browser with new environment "iis_test01" details page
       When I create IIS service "iis" without domain
       Then page should contain link "iis"

  Scenario: Create IIS service with domain
      Given browser with new environment "iis_test02" details page
       When I create AD service "ad.service" with 1 instances
        And I create IIS service "iis.server" in domain ad.service
       Then page should contain link "iis.server"

  Scenario: Create a few IIS services
      Given browser with new environment "iis_test03" details page
       When I create AD service "AD-NET" with 1 instances
        And I create AD service "ad.service" with 2 instances
        And I create IIS service "iis.server1" in domain AD-NET
        And I create IIS service "iis.server2" in domain ad.service
       Then page should contain link "iis.server1"
        And page should contain link "iis.server2"