Feature: Active Directories

  Scenario: Create AD service with 1 instance
      Given browser with new environment "test01" details page
       When I create AD service "ad.local" with 1 instances
       Then page should contain link "ad.local"

  Scenario: Create AD service with 3 instances
      Given browser with new environment "test02" details page
       When I create AD service "AD.net" with 3 instances
       Then page should contain link "AD.net"

  Scenario: Create a few AD services
      Given browser with new environment "test03" details page
       When I create AD service "AD.net" with 1 instances
        And I create AD service "test_ad.service" with 2 instances
       Then page should contain link "AD.net"
        And page should contain link "test_ad.service"