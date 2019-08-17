# Alfmonitor


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



## Alfmonitor Supported Platforms

Version: 0.0.2

Our goal is to ensure alfmonitor works on or with the following platforms. Keep in mind you very likely will be able to get it to work anywhere Python 3.6.4 can be installed but we aren't accepting bug reports in environments where unsupported platforms are involved. If you have a particular platform in mind, please write us and let us know. We are willing to consider it.

### Operating Systems:

* Ubuntu 16.04, 14.04
* RHEL/CentOS 7, 6

### Python

* 3.6+

### Databases

#### MySQL

Supported versions - See 

* 5.7 (Ubuntu 16.04 LTS and RHEL/CentOS 7, 6)
* 5.6 (Ubuntu 14.04 LTS and RHEL/CentOS 7, 6)
* 5.5 (Ubuntu 14.04 LTS and RHEL/CentOS 7, 6)

#### Postgresql 

Supported versions - See https://www.postgresql.org/support/versioning/

* 10
* 9.6
* 9.5
* 9.4
* 9.3

### Web Browsers

UI should render as expected with the latest versions of each:

* IE 
* Chrome
* Firefox

### Alfresco

Alfmonitor should work with any of these versions of Alfresco (Enterprise or Community versions):

* 5.2.x
* 5.1.x
* 5.0.x
* 4.2.*

## Docs for installing Alfmonitor on Standalone Ubuntu 16.04 LTS Server


## Firewalls

Ensure that you have your firewall either turned off or set to allow traffic into port 80 (or whichever port you would like to use with your httpd service).


Update all packages (optional):


```
# sudo apt update
```



Install necessary packages for Alfmonitor:


```
# sudo apt install build-essential
# sudo apt install libbz2-dev libssl-dev libreadline-dev libsqlite3-dev zlib1g-dev libmysqlclient-dev
```


For Ubuntu 14.04 you will need to install git:

```
# sudo apt install git
```


Create alfmonitor user and set password:


```
# adduser --home /apps alfmonitor
# passwd alfmonitor
```


If you would like for alfmonitor to have sudo privileges to be able to start apache2 (or httpd), follow these instructions to do that.

Install sudo if it's not installed already.


```
# sudo apt install sudo
```


Add line to end of file with visudo:


```
# visudo

...
alfmonitor ALL=(ALL) NOPASSWD: ALL
```


Save file and exit.


As alfmonitor user, install pyenv and Python 3.6.4


```
# su - alfmonitor
# curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```



Add to /apps/.bashrc:


```
export PATH="/apps/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```



Source .bashrc


```
# . ~/.bashrc
```



Create the directories for Alfmonitor install:


```
# mkdir -p alfmonitor/0.0.2
```



Install Python 3.6.4


```
# pyenv install 3.6.4
```



Set up the Python virtual environment:


```
# cd alfmonitor/0.0.2
# pyenv global 3.6.4
```


To test you have the correct Python version, you can run:


```
# python
```


and you should get this output:


```
Python 3.6.4 (default, Jan  7 2018, 10:19:13) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
```


You can enter Control-D to exit the Python shell.


```
# pyenv virtualenv alfmonitor-0.0.2
# pyenv local alfmonitor-0.0.2
```


You may see a prompt that looks like though it's possible depending on your pyenv install that you may not:


```
(alfmonitor-0.0.2) [alfmonitor@localhost 0.0.2]$ 
```


You can verify that the the alfmonitor/0.0.2 directory is using the alfmonitor-0.0.2 virtual environment by checking a file called .python-version in this directory. In the file it will say alfmonitor-0.0.2.


Set up Apache as root


```
# sudo apt install apache2
```


Configure the apache2 service:

```
# cd /etc/apache2
```

Open apache2.conf and add the following line to the end of the file (set your IP address here or other hostname you prefer to use):

```
ServerName 192.168.15.35
```

In /etc/apache2/sites-available, create a vhost file called alfmonitor.conf and add the following VirtualHost configuration. Feel free to change ServerName in the VirtualHost section to whatever you need for hostname to access alfmonitor web UI::


```
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /apps/alfmonitor/0.0.2
        ServerName alfmonitor

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/alfmonitor-error.log
        CustomLog ${APACHE_LOG_DIR}/alfmonitor-access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf

        ProxyPass /static/ !
        ProxyPass / http://localhost:8000/

        <Directory "/apps/alfmonitor/0.0.2/static/">
            Order allow,deny
            Allow from all
            Options Indexes FollowSymLinks MultiViews
            Satisfy Any
            #AllowOverride None
        </Directory>
</VirtualHost>
```


Save the file. In /etc/apache2/sites-enabled run:


```
# ln -s /etc/apache2/sites-available/alfmonitor.conf
```


This will create a symlink to the config, letting Apache2 know to include this virtual host in its configuration.


You will also need to load the correct modules:


```
# cd /etc/apache2/mods-enabled
```


and run:


```
# ln -s /etc/apache2/mods-available/proxy.conf .
# ln -s /etc/apache2/mods-available/proxy.load .
# ln -s /etc/apache2/mods-available/proxy_balancer.conf .
# ln -s /etc/apache2/mods-available/proxy_balancer.load .
# ln -s /etc/apache2/mods-available/ssl.conf .
# ln -s /etc/apache2/mods-available/ssl.load .
# ln -s /etc/apache2/mods-available/socache_shmcb.load .
# ln -s /etc/apache2/mods-available/proxy_http.load .
# ln -s /etc/apache2/mods-available/slotmem_shm.load .
```


Start Apache:


```
# service apache2 start
```


Install and run setup for Alfmonitor:


As the alfmonitor user, copy alfmonitor-0.0.2.tar.gz to /apps/alfmonitor/.


If you want to set the database to use a real RDBMS database server (which you should for production), follow these steps (otherwise, skip to the next):


#### Postgresql Setup

Use these settings in alfmonitor/settings.py for Postgresql:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alfmonitor',
        'USER': 'alfmonitor',
        'PASSWORD': 'alfmonitor',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Note that if you want to use a different db name, you'll need to set that up in your Postgresql server. You should of course, use a different password. If your database server is on a different server, ensure that you reflect that in your settings. Your DBA should also be able to make sure that the database endpoints are accessible to alfmonitor.


#### MySQL Setup

Use these settings in alfmonitor/settings.py for Postgresql:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alfresco',
        'USER': 'alfresco',
        'PASSWORD': 'alfresco',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Note that if you want to use a different db name, you'll need to set that up in your MySQL server. You should of course, use a more secure password. If your database server is on a different server, ensure that you reflect that in your settings. Your DBA should also be able to make sure that the database endpoints are accessible to alfmonitor.


#### Default DB: SQLite3

If you want to test the demo version which uses SQLite3 as the database, you can start here:


```
# tar xvzf alfmonitor-0.0.2.tar.gz
# cd 0.0.2
# ./setup.sh --noinput (this will install with regular admin user who's password is 'admin')
```


or



```
# ./setup.sh (will allow you to create admin user and password of your choice).
```



Start up the Alfmonitor app:


```
# ./alfmonitor.sh start
```



Pull up the console in the browser:


```
http://<virtual hostname><:port>/
```



## Docs for installing Alfmonitor on Standalone CentOS 7 Server


Update all packages (optional):


```
# sudo yum update
```


Install necessary packages for Alfmonitor:


```
# yum groupinstall 'Development Tools' 
# yum install bzip2-devel openssl-devel readline-devel sqlite-devel zlib-devel
```


For RHEL 7 / CentOS 7 install mariadb-devel:

```
# yum install mariadb-devel
```


For RHEL 6 / CentOS 6 instead of mariadb-devel, install mysql-devel instead:

```
# yum install mysql-devel
```


Disable SELINUX

Open /etc/sysconfig/selinux and use this setting:


```
SELINUX=disabled
```


Then reboot the server.


Create alfmonitor user and set password:


```
# adduser --home /apps alfmonitor
# passwd alfmonitor
```


If you would like for alfmonitor to have sudo privileges to be able to start apache2 (or httpd), follow these instructions to do that.

Install sudo if it's not installed already.


```
# yum install sudo
```


Add line to end of file with visudo:


```
# visudo

...
alfmonitor ALL=(ALL) NOPASSWD: ALL
```


Save file and exit.


As alfmonitor user, install pyenv and Python 3.6.4


```
# su - alfmonitor
# curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```


Add to /apps/.bash_profile:


```
export PATH="/apps/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```


Source .bash_profile


```
# . ~/.bash_profile
```


Create the directories for Alfmonitor install:


```
# mkdir -p alfmonitor/0.0.2
```


Install Python 3.6.4


```
# pyenv install 3.6.4
```


Set up the Python virtual environment:


```
# cd alfmonitor/0.0.2
# pyenv global 3.6.4
```


To test you have the correct Python version, you can run:


```
# python
```


and you should get this output:


```
Python 3.6.4 (default, Feb 23 2018, 16:44:22) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```


You can enter Control-D to exit the Python shell.


```
# pyenv virtualenv alfmonitor-0.0.2
# pyenv local alfmonitor-0.0.2
```


You may see a prompt that looks like though it's possible depending on your pyenv install that you may not:


```
(alfmonitor-0.0.2) [alfmonitor@localhost 0.0.2]$ 
```


You can verify that the the alfmonitor/0.0.2 directory is using the alfmonitor-0.0.2 virtual environment by checking a file called .python-version in this directory. In the file it will say alfmonitor-0.0.2.


Set up Apache as root


```
# yum install httpd
```


Configure the httpd service:


```
# cd /etc/httpd/conf
```


Open httpd.conf and add the following line to the end of the file (set your IP address here or other hostname you prefer to use):

```
ServerName 192.168.15.35
```


At the end of the httpd.conf file, add the following VirtualHost configuration (note that unlike with Ubuntu you will need to set the document root to use /var/www/html/alfmonitor. This is due to more stringent security requirements for RHEL/CentOS). Feel free to change ServerName in the VirtualHost section to whatever you need for hostname to access alfmonitor web UI:


```
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html/alfmonitor
        ServerName alfmonitor

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog logs/alfmonitor-error.log
        CustomLog logs/alfmonitor-access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf

        ProxyPass /static/ !
        # ProxyPass /media/ !
        ProxyPass / http://localhost:8000/


        <Directory "/apps/alfmonitor/0.0.2/static/">
            Order allow,deny
            Allow from all
            Options Indexes FollowSymLinks MultiViews
            Satisfy Any
            #AllowOverride None
        </Directory>
</VirtualHost>
```


Save the file.

Now, create the document root folder:

```
# cd /var/www/html
# mkdir -p alfmonitor/static
```

Copy alfmonitor-0.0.2.tar.gz to /apps/monitor.

As the alfmonitor user:

```
# cd alfmonitor/
# tar xvzf alfmonitor-0.0.2.tar.gz
```

As the root user, copy over static directory to vhost directory you just created:

```
# cd /apps/alfmonitor/0.0.2
# cp -rf static /var/www/html/alfmonitor/.
```


Start Apache:


```
# service httpd start
```


or 


```
# systemctl enable httpd
# systemctl start httpd
```


As the alfmonitor user, copy alfmonitor-0.0.2.tar.gz to /apps/alfmonitor/.


Install and run setup for Alfmonitor:


If you want to set the database to use a real RDBMS database server (which you should for production), follow these steps (otherwise, skip to the next):


### Database Setup

Out of the box, alfmonitor is set to use SQLite3. This is more for a demo really and not how your database setup should be used for production. Currently, alfmonitor only supports use with either Postgresql or MySQL. We personally prefer Postgresql but MySQL can be used with very good results. You will notice that the requirements.txt file shows psycopg2 (version 2.7.3.2) module and mysqlclient (version 1.3.12). These will be installed on setup so that you can use either database API.


#### Postgresql Setup

Use these settings in alfmonitor/settings.py for Postgresql:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alfmonitor',
        'USER': 'alfmonitor',
        'PASSWORD': 'alfmonitor',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Note that if you want to use a different db name, you'll need to set that up in your Postgresql server. You should of course, use a different password. If your database server is on a different server, ensure that you reflect that in your settings. Your DBA should also be able to make sure that the database endpoints are accessible to alfmonitor.


#### MySQL Setup

Use these settings in alfmonitor/settings.py for Postgresql:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alfresco',
        'USER': 'alfresco',
        'PASSWORD': 'alfresco',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Note that if you want to use a different db name, you'll need to set that up in your MySQL server. You should of course, use a more secure password. If your database server is on a different server, ensure that you reflect that in your settings. Your DBA should also be able to make sure that the database endpoints are accessible to alfmonitor.

#### Default DB: SQLite3

If you want to test the demo version which uses SQLite3 as the database, you can start here:


```
# tar xvzf alfmonitor-0.0.2.tar.gz
# cd 0.0.2
# ./setup.sh --noinput (this will install with regular admin user who's password is 'admin')
```


or


```
# ./setup.sh (will allow you to create admin user and password of your choice).
```


Start the Alfmonitor app:


```
# ./alfmonitor.sh start
```


Pull up the console in the browser:


```
http://<virtual hostname><:port>/
```



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
