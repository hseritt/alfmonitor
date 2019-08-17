

## Tutorial

Below is a walkthrough to show you how you can easily set up Alfmonitor to monitor a running Alfresco system on your laptop or on a server. This tutorial assumes you are running Alfmonitor on the same system where Alfresco is installed. It also assumes you have already set up Alfmonitor and have been successful in starting up.

1. Go to your Alfresco install directory. Start up Alfresco as you normally would.

2. Go to the directory where Alfmonitor is installed. Start it by issuing:

```
# ./alfmonitor.sh start
```

3. Go to the URL where Alfmonitor is running. Typically this will be:

```
http://[hostname:port]/console
```

4. This should prompt you for login. By default, the username/password for the console is admin/admin.

5. When the page opens up. You will notice that there are no active Profiles on the left. There also should be no Active Alarms or Inactive Alarms if you haven't configured this already. Go ahead and click on Setup a Profile. This will take you to a Add profile page.

6. Under Add profile, fill in the following:

Agent: Choose Http
Name: Localhost Share
URI: http://localhost:8080/share

For now, you can leave the rest of the settings as-is.

7. Scroll down and click Save.

8. Navigate back to http://[hostname:port]/console 

9. On the left side, you should now notice a profile called Localhost Share under Active Profiles. Looking in the console you should see something like this:

```
2018-03-05 18:32:55,155 [DEBUG] [monitor.run]:56 Starting agent: Http
2018-03-05 18:32:55,156 [DEBUG] [agents.lib.http_agent.run]:80 Running Http Agent.
2018-03-05 18:32:55,162 [DEBUG] [agents.lib.http_agent.test]:47 Testing profile: Localhost Share
2018-03-05 18:32:55,162 [DEBUG] [agents.lib.http_agent.connect]:20   Attempting http GET at http://localhost:8080/share
2018-03-05 18:32:59,316 [DEBUG] [agents.lib.tests.performance_test.test_performance]:14 Performance measured for Localhost Share is 4154ms.
2018-03-05 18:32:59,316 [DEBUG] [agents.lib.tests.performance_test.test_performance]:27 Performance test passed for Localhost Share is False.
2018-03-05 18:32:59,316 [DEBUG] [agents.lib.tests.availability_test.test_availability]:22 Availability test passed for Localhost Share is True.
2018-03-05 18:32:59,317 [DEBUG] [agents.lib.data.data_handlers.store_data]:21 Saving data from profile: Localhost Share
```

Yours may or may not fail. Since this was the first login since a restart of Alfresco, it's possible that the initial check will fail. If that happens, you should notice an alarm under Active Alarms.

Within the next minute, if the performance is reasonable on your test server, the alarm should go away. But, the alarm will now show as a historical and inactive alarm.

10. If you didn't get an alarm but would like to see one triggered, you can now go to your Alfresco install and turn it off. This will trigger an availability alarm. You will see this under Active Alarms until you start up Alfresco again.

After you feel you have a good undertanding of how this profile was configured, you should try profiles that check these resources:

* Alfresco Admin Console
* Alfresco WebDAV with username/password
* Check the REST API for People: http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/people
* Alfresco's Postgresql Database
* Ensure that CIFS ports are open and available using the Ping agent.

A note on supportability for the CMIS Rest API as shown here:

https://api-explorer.alfresco.com/api-explorer/#/

Be aware that some of the APIs shown here are not supported in Alfresco versions below 5.2.x.
