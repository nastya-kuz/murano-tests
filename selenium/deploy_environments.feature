Feature: Deploy environments


  Scenario: Deploy environment with AD service
      Given browser with new environment "env1_for_deploy" details page
       When I create AD service "ad.test" with 1 instances
        And I deploy environment "env1_for_deploy"
       Then environment "env1_for_deploy" has status "Deploy In Progress"
        And environment "env1_for_deploy" has progress bar


  Scenario: Check status of AD service
      Given browser with environment "env1_for_deploy" details page
       Then service "ad.test" has status "Deploy In Progress"
        And service "ad.test" has progress bar


  Scenario: Deploy environment with IIS service
      Given browser with new environment "env2_for_deploy" details page
       When I create IIS service "iis_service" without domain
        And I deploy environment "env2_for_deploy"
       Then environment "env2_for_deploy" has status "Deploy In Progress"
        And environment "env2_for_deploy" has progress bar


  Scenario: Check status of IIS service
      Given browser with environment "env2_for_deploy" details page
       Then service "iis_service" has status "Deploy In Progress"
        And service "iis_service" has progress bar


  Scenario: Deploy environment with AD and IIS services
      Given browser with new environment "env3_for_deploy" details page
       When I create AD service "ad.test" with 2 instances
        And I create IIS service "iis_service" in domain ad.test
        And I create IIS service "iis_service2" in domain ad.test
        And I deploy environment "env3_for_deploy"
       Then environment "env3_for_deploy" has status "Deploy In Progress"
        And environment "env3_for_deploy" has progress bar


  Scenario: Check environment status before deploy
      Given browser with new environment "env4_for_deploy" details page
       When I create AD service "ad-test" with 1 instances
        And I create IIS service "iis_service" in domain ad-test
       Then environment "env4_for_deploy" has status "Ready To Deploy"
        And environment "env4_for_deploy" has no progress bar


  Scenario: Check status of services before deploy
      Given browser with environment "env4_for_deploy" details page
       Then service "ad-test" has status "Ready To Deploy"
        And service "ad-test" has no progress bar
        And service "iis_service" has status "Ready To Deploy"
        And service "iis_service" has no progress bar