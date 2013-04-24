@taran_wrk
Feature: Keero REST API

  Scenario: 1. Create IIS service without parameter 'domain'
# 1.1. Send request 'create IIS service' without parameter domain	
# 1.1. - REST API service should return response with status code 200 and body with IIS service instance.
       When I delete all environments
       Then environments should contain "0" environment(s)
       When I create environment "dc207"
        And I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
        And I create "1" IIS for environment "dc207"
        And I set IIS name: "IIS208"
        And I create "1" IIS for environment "dc207"
        And I set IIS name: "IIS209"
#       Then I try to create IIS for environment "dc207" without param "domain"
       Then environment "dc207" should not_contain IIS "IIS206"
        And environment "dc207" should contain IIS "IIS208"
#        And environment "dc207" should contain IIS "IIS209" ================================================= fail to list IIS without domain
        And environment "dc207" should not_contain IIS "IIS207" with domain: "iis_222"
        And environment "dc207" should contain IIS "IIS207" with domain: "IIS207_domain"

  Scenario: 2. Get list of IIS services
# 2.1. Send request 'get list of IIS services'.	
# 2.1. - REST API service returns respose with 200 code and body with all IIS instances in the current environment.
       When I delete environment "dc207"
        And I create environment "dc207"
        And I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
        And I create "1" IIS for environment "dc207"
        And I set IIS name: "IIS208"
        And I create "1" IIS for environment "dc207"
        And I set IIS name: "IIS209"
        And I create "1" IIS for environment "dc207"
       Then I get list of IIS services for environment "dc207"
        
        
  Scenario: 3. REST API: get list of environments
# 3.1. Send request 'get list of environments'	
# 3.1. - REST API service returns list of environments.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I create environment "dc208"
        And I create environment "dc209"
       Then environments should contain "3" environment(s)
       When I delete environment "dc208"
       Then environments should contain "2" environment(s)
       When I delete environment "dc207"
        And I delete environment "dc209"

  Scenario: 4. REST API: get list of AD services
# 4.1. Send request 'get list of AD services'.	
# 4.1. - REST API service returns respose with 200 code and body with all AD instances for the current environment.
       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
        And I create "1" AD(s) for environment "dc207"
        And I set AD name: "ad2.local"
        And I create "2" AD(s) for environment "dc207"
        And I set AD name: "ad3.local"
        And I create "3" AD(s) for environment "dc207"
        And I set AD name: "ad4.local"
        And I create "1" AD(s) for environment "dc207"
       Then environment "dc207" should contain "7" AD(s)
#       When I delete AD "ad3.local" for environment "dc207" =============================================================== not_work


  Scenario: 5. Deploy session
# 5.1. Send request 'create enironment'	
# 5.1. - REST service should return the response with status code 200 and body with new environment.		
# 5.2. Send request 'open session' for this environment.
# 5.2. - REST service should return the response with status code 200 and body with session id.
# 5.3.	Add a few services for this environment.
# 5.3. - All services should be successfully added to the environment.
# 5.4. Send request 'deploy session' for this environment.	
# 5.4. - REST service should return the response with status code 200	

       When I delete environment "dc205"
        And I create environment "dc205"
        And I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
        And I create "1" IIS for environment "dc205"
        And I set AD name: "ad.local"
        And I create "1" AD(s) for environment "dc205"
       Then I deploy environment "dc205"


  Scenario: 6. REST API: delete environment
# 6.1. Send requiest 'delete enironment'
# 6.1. - REST service should return the response with status code 200
       When I delete environment "dc207"
        And I create environment "dc207"
        And I create environment "dc208"
        And I create environment "dc209"
       Then environments should contain "4" environment(s)
#                                        4 - we also calculate "dc205"
       When I delete environment "dc207"
        And I delete environment "dc208"
       Then environments should contain "2" environment(s)
       When I delete environment "dc209"
        

  Scenario: 7. REST API: create session for environment
# 7.1. Send request 'create environment'
# 7.1. - REST service should return the response with status code 200 and body with new environment.
       When I delete environment "dc207"
        And I create environment "dc207"

# 7.2. Send request 'open session' for this environment.
# 7.2. - REST service should return the response with status code 200 and body with session id.
        And I open session for environment "dc207"

  Scenario: 8. REST API: create IIS service
# 8.1. Send request 'create IIS service'.
# 8.1. - REST API service returns respose with 200 code and body with IIS instance.
       When I delete environment "dc207"
        And I create environment "dc207"
        And I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
        And I create "1" IIS for environment "dc207"
        And I set IIS name: "IIS208"
        And I set IIS domain: "IIS208_domain"
        And I create "1" IIS for environment "dc207"
       Then environment "dc207" should contain "2" IIS(s)
       
  Scenario: 9. REST API: create environment
# 9.1. Send requiest 'create enironment'
# 9.1. REST service should return the response with status code 200 and body with new environment.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I create environment "dc208"
        And I create environment "dc209"
       Then environments should contain "4" environment(s)
#                                        4 - we also calculate "dc205"
       When I delete environment "dc208"
        And I delete environment "dc209"

  Scenario: 10. REST API: create AD service
# 10.1. Send request 'create AD service'.
# 10.1. - REST API service returns respose with 200 code and body with AD instance.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
        And I create "1" AD(s) for environment "dc207"
        And I set AD name: "ad2.local"
        And I create "2" AD(s) for environment "dc207"
       Then environment "dc207" should contain "3" AD(s)

  Scenario: 11. REST API: 200 requests 'create IIS sevice' for REST service
# 11.1. Send 200 simultaneously requests 'create IIS service' for REST API service.	
# 11.1. - REST API service should succesfully created 200 IIS services and returns responces for 1-2 seconds (no more that 5 secconds)

  Scenario: 12. REST API: 200 requests 'create environment' for REST service
# 12.1. Send 200 simultaneously requests 'create environment'	
# 12.1. - REST API service should successfully created 200 environments in 1-2 secconds (no more that 5 seconds for this job)

  Scenario: 13. REST API: 200 requests 'create AD service' for REST service
# 13.1. Send 200 simultaneously requests 'create AD service' for REST API service.	
# 13.1. - REST API service should succesfully created 200 AD services and returns responces for 1-2 seconds (no more that 5 secconds)	

  Scenario: 14. Negative: try to open session for environment without auth token
# 14.1. Try to send request 'open session for environment' without auth token.
# 14.1. - REST API service should return error message about authentication.

       When I delete environment "dc207"
        And I create environment "dc207"
       Then I try to open session for environment "dc207" without authentication

  Scenario: 15. Negative: try to get list of environments without auth token
# 15.1. Try to send request 'deploy session for environment' without auth token.
# 15.1. - REST API service should return error message about authentication.

       When I delete environment "dc207"
        And I create environment "dc207"
       Then I try to get list of environments without authentication
        
  Scenario: 16. Negative: try to deploy session for environment without auth token
# 16.1. Try to send request 'delete environment' without auth token.
# 16.1. - REST API service should return error message about authentication.

       When I delete environment "dc207"
        And I create environment "dc207"
       Then I try to deploy session for environment "dc207" without authentication

  Scenario: 17. Negative: try to delete environment without auth token
# 17.1. Try to send request 'delete environment' without auth token.
# 17.1. - REST API service should return error message about authentication.

       When I delete environment "dc207"
        And I create environment "dc207"
       Then I try to delete environment "dc207" without authentication
        
  Scenario: 18. Negative: try to create IIS service without session ID parameter
# 18.1. Send request 'create IIS service' without parameter session ID.
# 18.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
#       Then I try to create IIS for environment "dc207" without session ID    ========================== not working, response code 500
       When I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
#       Then I try to create IIS for environment "dc207" without session ID    ========================== not working, response code 500

  Scenario: 19. Negative: try to create IIS service without parameter units
# 19.1. Try to send request 'create IIS service' without parameter units
# 19.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
#       Then I try to create IIS for environment "dc207" without param "units"    ========================== not working, response code 500
       When I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
#       Then I try to create IIS for environment "dc207" without param "units"    ========================== not working, response code 500

  Scenario: 20. Negative: try to create IIS service without parameter Name
# 20.1. Try to send request 'create IIS service' without parameter Name
# 20.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
#       Then I try to create IIS for environment "dc207" without param "name"    ========================== not working, response code 500
       When I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
#       Then I try to create IIS for environment "dc207" without param "name"    ========================== not working, response code 500

  Scenario: 21. Negative: try to create IIS service without parameter Admin Password
# 21.1. Try to send request 'create IIS service' without parameter Admin Password
# 21.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
#       Then I try to create IIS for environment "dc207" without param "password"  ================ pass with 200 code instead 403
       When I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
#       Then I try to create IIS for environment "dc207" without param "password"  ================ pass with 200 code instead 403

  Scenario: 22. Negative: try to create IIS service without auth token
# 22.1. Send request 'create IIS service' withou auth token.
# 22.1. - REST API service should return error message about authentication.

       When I delete environment "dc207"
        And I create environment "dc207"
       Then I try to create IIS for environment "dc207" without authentication
       When I set IIS name: "IIS207"
        And I set IIS domain: "IIS207_domain"
       Then I try to create IIS for environment "dc207" without authentication

       
  Scenario: 23. Negative: try to create environment without auth token
# 23.1. Try to send request 'create environment' without auth token.
# 23.1. - REST API service returns error message about authentication.

       When I delete environment "dc207"
       Then I try to create environment "207" without authentication

  Scenario: 24. Negative: try to create AD service without session ID parameter
# 24.1. Send request 'create AD service' without parameter session ID.
# 24.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
#       Then I try to create AD for environment "dc207" without session ID    ========================== not working, response code 500

  Scenario: 25. Negative: try to create AD service without Recovery Password parameter
# 25.1. Send request 'create AD service' without parameter Recovery Password
# 25.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
#       Then I try to create AD for environment "dc207" without param "recoveryPassword" ================ pass with 200 code instead 403

  Scenario: 26. Negative: try to create AD service without parameter units
# 26.1. Send request 'create AD service' without units
# 26.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
#       Then I try to create AD for environment "dc207" without param "units" ======================= fail with code 500

  Scenario: 27. Negative: try to create AD service without Name parameter
# 27.1. Send request 'create AD service' without parameter Name
# 27.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
#       Then I try to create AD for environment "dc207" without param "name" ================ pass with 200 code instead 403

  Scenario: 28. Negative: try to create AD service without auth token
# 28.1. Send request 'create AD service' withou auth token.
# 28.1. - REST API service returns error message about authentication.

       When I delete environment "dc207"
        And I create environment "dc207"
        And I set AD name: "ad.local"
       Then I try to create AD for environment "dc207" without authentication

  Scenario: 29. Negative: try to create AD service without Admin Password parameter
# 29.1. Send request 'create AD service' without parameter Admin Password
# 29.1. - REST API service should return error message about incorrect parameters.

       When I delete environment "dc207"
        And I create environment "dc207"
#       Then I try to create AD for environment "dc207" without param "adminPassword" ================ pass with 200 code instead 403
        When I delete environment "dc207"
