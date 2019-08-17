
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

