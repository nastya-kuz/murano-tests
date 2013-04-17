Feature: Environments


  Scenario: Create environment
      Given browser with Environments page
       When I create environment "env1"
       Then page should contain link "env1"

  Scenario: Delete environment
      Given browser with Environments page
       When I create environment "env2"
        And I delete environment "env2"
       Then page should not contain link "env2"

  Scenario: Delete environments
      Given browser with Environments page
       When I create environment "env3"
        And I create environment "env4"
        And I create environment "env5"
        And I delete environment "env3"
        And I delete environment "env5"
       Then page should not contain link "env3"
        And page should not contain link "env5"
        And page should contain link "env4"