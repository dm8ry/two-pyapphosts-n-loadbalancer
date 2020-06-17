Purpose:
--------

Create an infrastructure as code that creates a SaaS service environment using Vagrant. 
The service should provide a REST API which returns the hostname and current date and time of the host that the request is running on.
The solution is based on a Linux family OS.

Environment components:
-----------------------

- A load balancer
- 2 application hosts

Load balancer:
--------------

The load balancer listens to the incoming requests to the API and forwards them to one of the application hosts, spreading the load in round robin fashion.
The load balancer should run as a Docker container.

Application host:
-----------------

Runs a Python application based on Flask inside a Docker container, which will listen to incoming API requests. There are 2 REST APIs:

1. Returns the hostname of the current host
2. Returns the current date and time

Architecture:
-------------

The environment can be presented as:

- Nginx load balancer
- Two application hosts machines

The load balancer accepts incoming requests and forwards them to one of the two application servers which are prepared to accept them. 
It's done in round robin style. Also it can be done in a weighted style.
Nginx is an example of a proxy which is capable of load balancing. Also there are another load balancers. for example F5.
A load balancer performs the function of receiving the initial requests and making sure that it gets answered by a corresponding application server. 
The 2 application servers are based on Python Flask.

The Load Balancer runs as a Docker Container.
Each of two application hosts are based on Flask inside a Docker Container.

The structure of source directory:

```
/----
    +-- Vagrantfile
    |
    +-- docker-compose.yml
    |
    +-- documentation.txt
    |
    +------------- lb ----------------+
    |                                 |
    |                                 +------- Dockerfile
    |                                 |
    |                                 +------- nginx.conf
    |
    +------------- app ---------------+
                                      |
                                      +------- requirements.txt
                                      |
                                      +------- Dockerfile
                                      |
                                      +------- app.py
```

How to deploy the environment:
------------------------------

The environment can be deployed using docker-composer or using vagrant.

Using docker-composer:
----------------------

docker-compose build

Builds the following images:

```
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
dima_loadbalancer   latest              111111111111        3 minutes ago       127MB
dima_app1           latest              222222222222        3 minutes ago       220MB
dima_app2           latest              333333333333        3 minutes ago       220MB
```

docker-compose up -d

Starts app1, app2 and loadbalancer:

```
Starting app2 ... done
Starting app1 ... done
Starting loadbalancer ... done
```

docker-compose ps

Should provide output:

```
user@user-pc:~/dima$ docker-compose ps
    Name             Command          State         Ports       
----------------------------------------------------------------
app1           python app.py          Up      5000/tcp          
app2           python app.py          Up      5000/tcp          
loadbalancer   nginx -g daemon off;   Up      0.0.0.0:80->80/tcp
user@user-pc:~/dima$ 
```

docker-compose down

Brings environment down:

```
Stopping loadbalancer ... done
Stopping app2         ... done
Stopping app1         ... done
Removing loadbalancer ... done
Removing app2         ... done
Removing app1         ... done
Removing network dima_default
```

Using vagrant:
--------------

vagrant up

or 

vagrant reload

vagrant status 

Shows state of environment:

Current machine states:

```
app1                      running (docker)
app2                      running (docker)
loadbalancer              running (docker)
```

vagrant destroy -f

Stops the running machine Vagrant is managing and destroys all resources that were created during the machine creation process.

How to test the environment:
----------------------------

Run bash script ./check_configuration.sh

It checks LoadBalancer, App1 and App2 statuses, prints their IPs, and checks connectivity and round-robin distribution.

The output trace will look as follows:

user@user-pc:~/dima$ ./check_configuration.sh 
 
```
----------------------------------------
Check Configuration and Test Environment
----------------------------------------

ContainerID LoadBalancer = 8cd1175fe3ac
ContainerID App1         = 93ba9285487e
ContainerID App2         = c27e662d04a1
 
Load Balancer IP: 172.17.0.4
App1 IP:          172.17.0.2
App2 IP:          172.17.0.3
 
Check response calling to  http://172.17.0.4
Hello from the machine: 172.17.0.2!
 
Check response calling to  http://172.17.0.4/hostname
Hostname: c27e662d04a1
 
Check response calling to  http://172.17.0.4/datetime
DateTime: 02/04/2020 09:15:17
 
Check response calling to  http://172.17.0.2:5000/hostname
Hostname: 93ba9285487e
 
Check response calling to  http://172.17.0.3:5000/hostname
Hostname: c27e662d04a1
 
Check response calling to  http://172.17.0.2:5000/datetime
DateTime: 02/04/2020 09:15:17
 
Check response calling to  http://172.17.0.3:5000/datetime
DateTime: 02/04/2020 09:15:17
 
 
Status: Success
```

or

user@user-pc:~/dima$ ./check_configuration.sh 

```
----------------------------------------
Check Configuration and Test Environment
----------------------------------------
 
Error! LoadBalancer is not running!
Status: Failure
dmr@dmr-pc:~/refinitiv$


How to use the API:
-------------------

http://<Load_Balancer_IP>

Output (round-robin distributed): 

Hello from the machine: <App1_IP>!
or
Hello from the machine: <App2_IP>!

http://<Load_Balancer_IP>/hostname

Output (round-robin distributed):

Hostname: <App1_Hostname>
or
Hostname: <App2_Hostname>

http://<Load_Balancer_IP>/datetime

Output (from round-robin distributed hosts):

DateTime: DD/MM/YYYY HH:MI:SS


To get <Load_Balancer_IP> run script: 

./check_configuration.sh
```


---------------- The End ---------------------
