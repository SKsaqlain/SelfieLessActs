# Description
The project was carried out as a part of the Cloud Computing course at PES University 2019.<br/>
The objective of the project was to build a container orchestrator that can perform load balancing between micro-services and within micro-services, fault tolerance, and auto-scaling. The entire project was implemented on [Amazon AWS](https://aws.amazon.com/) EC2 instances.


# Requirements
* ubuntu 16.04 
* python3
* flask
* mysql
* docker 
* alpine 3.7

# Usage 
To replicate the project execute the below given steps in order'
* clone the repository
```
$git clone https://github.com/SKsaqlain/SelfieLessActs.git
```
* Create two ece2 instances one for the user micro-service and the other to acts micro-service name the key file for the user instance as user and the acts instance as acts (_for ease of replication only_).<br/> follow the below link to create a AWS EC2 instance. configure the security group to allow http,ssh traffic and tcp port 80.
```
https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html
```
