# rhsmDeleteInactiveSystems
Script to delete Inactive systems on Red Hat Subscription Management (RHSM)

As a user of RHSM, I frequently find myself needing to clean up after systems
which I have deleted, but not properly unregistered. In lieu of performing
this manually, this script takes of that task. 

# Reporting on inactive systems

By default, **rhsmDeleteInactiveSystems.py** only reports on systems that are
inactive, defined as any system that has a lastCheckin date older than the number of
days you specify. This allows you to report on the inactive systems in the event that
they aren't managed by you or to get an idea for what is going to be deleted prior to
actually doing anything destructive. 

~~~
↪ ./rhsmDeleteInactiveSystems.py -l rh_user_account -p '*****' --days 45
================================================================================
	 Skipping host - sat-demo1.example.com as it doesn't meet the deletion criteria
================================================================================
	 Consumer Name - sat.example.info
	 Consumer UUID - f1a922e0-bf6e-45d4-ab5f-c7c7d0f5f392
	 Last Check-in - 2016-03-04T23:59:13.000+0000
	 Registered User - rh_user_account
	 sat.example.info will be deleted as it as has not checked in within 122 days, 0:00:00
================================================================================
	 Skipping host - satellite.example.com as it doesn't meet the deletion criteria
================================================================================
     Skipping host - satellite6.example.org as it doesn't have a valid lastCheckin value
================================================================================
	 Skipping host - testnode-122.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - cdn.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - satdemo.example.com as it doesn't meet the deletion criteria
================================================================================
	 Consumer Name - satellite.example.com
	 Consumer UUID - dea782c6-01c6-477a-b106-c6949b792e90
	 Last Check-in - 2016-02-13T14:39:48.000+0000
	 Registered User - rh_user_account
	 satellite.example.com will be deleted as it as has not checked in within 142 days, 0:00:00
================================================================================
	 Consumer Name - satellite.example.info
	 Consumer UUID - 22128c24-7fc9-4fd3-a56d-235cbcebf5e0
	 Last Check-in - 2016-05-12T10:22:10.000+0000
	 Registered User - rh_user_account
	 satellite.example.info will be deleted as it as has not checked in within 53 days, 0:00:00
================================================================================
	 Skipping host - rhev.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - satellite.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - sat-demo2.example.com as it doesn't meet the deletion criteria
~~~

# Deleting inactive systems

When ready, simply run the script again with the `--delete` switch to actually delete
the inactive systems. 
~~~
↪ ./rhsmDeleteInactiveSystems.py -l rh_user_account -p '*****' --days 45 --delete
================================================================================
	 Skipping host - sat-demo1.example.com as it doesn't meet the deletion criteria
================================================================================
	 Consumer Name - sat.example.info
	 Consumer UUID - f1a922e0-bf6e-45d4-ab5f-c7c7d0f5f392
	 Last Check-in - 2016-03-04T23:59:13.000+0000
	 Registered User - rh_user_account
	 sat.example.info will be deleted as it as has not checked in within 122 days, 0:00:00
	 Attemping delete of sat.example.info
	 Result - SUCCESS
================================================================================
	 Skipping host - satellite.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - satellite6.example.org as it doesn't have a valid lastCheckin value
================================================================================
	 Skipping host - testnode-122.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - cdn.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - satdemo.example.com as it doesn't meet the deletion criteria
================================================================================
	 Consumer Name - satellite.example.com
	 Consumer UUID - dea782c6-01c6-477a-b106-c6949b792e90
	 Last Check-in - 2016-02-13T14:39:48.000+0000
	 Registered User - rh_user_account
	 satellite.example.com will be deleted as it as has not checked in within 142 days, 0:00:00
	 Attemping delete of satellite.example.com
	 Result - SUCCESS
================================================================================
	 Consumer Name - satellite.example.info
	 Consumer UUID - 22128c24-7fc9-4fd3-a56d-235cbcebf5e0
	 Last Check-in - 2016-05-12T10:22:10.000+0000
	 Registered User - rh_user_account
	 satellite.example.info will be deleted as it as has not checked in within 53 days, 0:00:00
	 Attemping delete of satellite.example.info
	 Result - SUCCESS
================================================================================
	 Skipping host - rhev.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - satellite.example.com as it doesn't meet the deletion criteria
================================================================================
	 Skipping host - sat-demo2.example.com as it doesn't meet the deletion criteria
~~~
