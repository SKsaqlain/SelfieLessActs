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

# Architecture 
The overall architecutre of the  project looks something like the one given below
![Alt text](FLOW.jpg)
# Usage 
To replicate the project execute the below given steps in order'
* clone the repository
```
$git clone https://github.com/SKsaqlain/SelfieLessActs.git
```
* Create two ece2 instances one for the user micro-service and the other for the acts micro-service name the key file for the user instance as _users_ and the acts instance as _acts_ (_for ease of replication only_).<br/> follow the below link to create a AWS EC2 instance. configure the security group to allow http,ssh traffic and tcp port 80.
```
https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html
```
* Install Docker on both the instances.<br/> Follow the below link to install docker on both the instances
```
https://docs.docker.com/install/linux/docker-ce/ubuntu/
```
* 
* Push the docker file from your local host to the both the EC2 instances
```
$sudo scp -i key.pem -r Dockerfile instancename@ip:/
```
* Execute the below command on the intance to create alpine containers respectively
```
$sudo docker build -t acts:latest .
```
```
$sudo docker build -t users:latest .
```
* Execute the below command on the acts instance to create a mysql container, the database is used to maintain consistency across all the acts instances when scale up function  is called.
```
$sudo docker run -d -p 3306:3306 --name=database --env="MYSQL_ROOT_PASSWORD=123" mysql
$docker exec -it database bash
$mysql -u root -p
>>123
>>create database SelfieLessActs;
>>use SelfieLessActs;
>>create table user_info(username varchar(100),password varchar(100));
>>create table act_info
>>create table category(category_name varchar(100));
>>create table act_info(actId varchar(100),username varchar(100),datetime varchar(100),caption varchar(100),upvote int,image_path(5000),category_name varchar(100));
>>create table containers(port varchar(10));
>>exit
```
* 
