HA Testing Scripts
============

 The scripts for OpenStack Murano HA testing.

How To Test 
============
 To run HA tests need to perform the following steps:

1. Copy agent.py on all controller nodes (with services, which we want to control)

2. Copy controller.py and controller.conf on your personal host (to manage services on controller modes)

3. Change controller.conf - need to fix IP addresses of controller nodes and parameters file1 and file2

4. Execute agent.py on all controller-nodes (with services, like Murano Conductor service):

   sudo python agent.py

5. Execute controller.py on your personal host and start to testing. For example, you can start to deploy environment. In this case Murano Conductor service on the first node will start to deploy VMs and these testing scripts will detect node with Active Murano Controller service - and will stop it for several secconds. In case of properly HA the same service on the other nodes should start and continue to deploy environment.





 Mirantis Inc (C) 2013.
