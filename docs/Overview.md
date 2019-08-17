

## Alfmonitor Overview

Alfmonitor is a tool that can be used to monitor Alfresco. In fact, it uses some general and specific agents to monitor the different parts of a running Alfresco environment. From a general standpoint, it can monitor resources like:

* HTTP connections
* Database connections
* Socket connections

For specific standpoints, alfmonitor can monitor Alfresco's availability and performance of delivering REST API's and CMIS. It's also very simple to write your own custom agents based on what kind of data you would like to store from Alfresco.

## Alfmonitor Objects

There are a few objects that are specific to alfmonitor (and indeed to most other monitoring tools available). They are:

* Agents
* Profiles
* Data
* Alarms

### Agents

An agent is a script that runs to check a particular resource in Alfresco. These are Python  modules written for a specific intention. Under the agents app, they are in the lib subdirectory. Currently, there are these agents out of the box:

* cmis_rest_agent.py (CMIS rest api)
* http_agent.py (http connections)
* pg_agent.py (postgresql connections)
* ping_agent.py (socket connections)

### Tests

By default, Each agent makes two types of checks:

* Availability
* Performance

With availability, the agent will want to make sure that the URI given for each profile is at least reachable and giving a proper response. In the case of HTTP agent, a proper response is usually a 200 status code.

Not only should a resource be available and render an expected response, it should also do it in a performant manner. For example, for most HTTP resources, it's reasonable to assume that we should get the proper response in 8 seconds or less. The performance test will then ensure that the expected response is returned in 8 seconds or an alarm will be issued if these are enabled. 


### Profiles

A profile is a set of configurations for an agent. An agent can have many profiles that can be monitored. Below are settings that can be configured for each profile:

* Name (this is just the name of the profile itself)
* URI (the technical URI that will be monitored)
* Port (port at which the URI will be checked -- optional except for ping_agent and pg_agent modules)
* Protocol (TCP or UDP -- optional for ping_agent)
* Username / Password (authentication when needed)
* Testing criteria

An example would be where we want to make sure that Alfresco Share is responding to http requests. To do this, we could set up a profile for the http_agent module like so:

Name: Alfresco Web Client
URI: http://localhost:8080/alfresco
Username: admin
Password: admin
Is Availability Checked?: True
Is Performance Checked?: True
Performance Threshold in MS: 8000 (for 8 seconds)
Is Alarm Created for Availability Failure?: True
Is Alarm Created for Performance Failure?: True
Is Data Stored for Availability?: True
Is Data Stored for Performance?: True

The would check the Alfresco Web Client and provide authentication credentials where needed (note that this does not work with Share URLs that reference protected documents in that authentication methods like NTLM, Kerberos or LDAP-AD could be used).

We would tell the agent for this profile to test availability and whether or not the connection meets the performance expectations. Also, we would be telling the agent that we would like an alert should the Alfresco Web Client not be available or doesn't return a response within 8 seconds or less. We also can store the results for each check in the database.

### Data

When a profile is checked and the option to store data for the check is set to True, then this data would be stored as a data point for reference later.

Each data point references a profile and true/false value for each test. In the case of performances checks, it will also store the result of the time it took to connect.

### Alarm

As mentioned in the Profiles section, if a test fails and alarms are enabled for the profile, then an alarm is created. Alarms are stored for historical purposes. They remain active until the profile does not fail another availability or peformance check. An active alarm will trigger an email to associated administrators referenced for each profile. If there are no administrators associated with the profile, then the email of the alfmonitor admin will be used.

