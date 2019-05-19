from flask import Flask,request,jsonify,json,redirect
import pymysql
import base64
import string
import random
import datetime
from collections import Counter
import requests
import ast
import docker
import time
import threading
import os
app=Flask(__name__)



#docker client object to execute docker commands
client=docker.from_env()

#connecting to the common database for consistance
db=pymysql.connect("127.0.0.1","root","123","SelfieLessActs")
#cursor=db.cursor()



nR=1	#number of requests
i=-1	#round robin index
scaleFlag=0	#scale function to be called when first request is  encountered
#general route to capture all requests
@app.route('/<path:path>',methods=['POST','GET','DELETE'])
def catch_all(path):
		#creating cursor object
        cursor=db.cursor()
        #print(os.getpid())
        print(path)
        #sql to list all the active containers
        sql="select * from containers"
        cursor.execute(sql)
        cursor.close()
        containers=[ele[0] for ele in cursor.fetchall()]
        #print(containers)
        global i



        global scaleFlag
        #ignoring some requests 
        if(path!="api/v1/_health" or path!="alpi/v1/_crash" or path!="/"):
                global nR
                nR=nR+1
                print(nR)
                #to start the scale function
                if(scaleFlag==0):
                        #scaleFlag=1
                        t1=threading.Thread(target=scale)
                        t1.daemon=True
                        t1.start()
                scaleFlag=1

        #round Robin.
        i=(i+1)%len(containers)

        #print(containers[i])
        location="http://0.0.0.0:"+containers[i]+'/'+path
        headers={'Content-type':'application/json'}
        if(request.method=='GET'):
        		#redirecting the get request.
                r=requests.get(location,data={},headers=headers)
                #if the  request field is empty .
                try:
                        message=ast.literal_eval(r.text.strip("\n"))
                except:
                        message={}

                resp=jsonify(message)
                resp.status_code=r.status_code
                return  resp

        elif(request.method=='POST'):
        		#getting the  data
                data=request.get_data()
                #redirecting the  post request
                r=requests.post(location,data,headers=headers)
                message={}
                resp=jsonify(message)
                resp.status_code=r.status_code
                return  resp

        elif(request.method=='DELETE'):
        		#redirecting the delete request.
                r=requests.delete(location,data={},headers=headers)
                message={}
                resp=jsonify(message)
                resp.status_code=r.status_code
                return resp
        else:
                pass

        #cursor.close()

#health check function.
def watch():
        cursor=db.cursor()
        #print(os.getpid())
        #getting all the available containers
        sql="select * from containers"
        cursor.execute(sql)
        containers=[ele[0] for ele in cursor.fetchall()]
        #print(containers)

        nc=len(containers)

        for j in range(0,nc):
        		#health check
                try:
                        location="http://0.0.0.0:"+containers[j]+'/api/v1/_health'
                        headers={'Content-type':'application/json'}
                        r=requests.get(location,json={},headers=headers)


                        if(r.status_code==500):
                        		#if container is inactive stoping that container
                        		#and starting a new container with the same port number.

                                cnt=containers[j]

                                print("containers with port %s is down"%(cnt))
                                #getting the name of the containers so that it could be stoped
                                cmd="docker ps -a| grep '%s'"%(cnt)
                                name=os.popen(cmd).read().split()[-1]
                                #print(name)

                                cntrs=client.containers.get(name)
                                cntrs.stop()
                                #creating a new container with the same port number.
                                client.containers.run("acts:latest","python /app/acts_app.py",detach=True,ports={"80/tcp":str(cnt)},remove=True)

                                print("new container up and running")
                except:
                        pass
        #print("done")
        cursor.close()


#function to scale in or scale out.
def scale():
	while(1):
		cursor=db.cursor()
        global nR
        print("requests=%d scale function"%(nR))
        print(os.getpid())

        #selecting all avaiable containers.
        sql="select * from  containers"
        cursor.execute(sql)
        containers=[ele[0] for ele in cursor.fetchall()]

        #calculating minimum containers
        minC=(nR//20)+1
        nR=1;
        #scale-in.
        if(len(containers)>minC):
                for j in range(len(containers)-1,0,-1):
                        cnt=containers[j]

                        sql="delete from containers where port='%s'"%(cnt)
                        cursor.execute(sql)
                        db.commit()

                        print("containers with port %s is about to be killed"%(cnt))
                        cmd="docker ps -a| grep '%s'"%(cnt)
                        name=os.popen(cmd).read().split()[-1]
                        print(name)
                        cntrs=client.containers.get(name)
                        cntrs.stop()
        #scale-out
        elif(len(containers)<minC):
                max_port=int(max(containers))+1
                n=minC-len(containers)
                for j in range(0,n):

                        client.containers.run("acts:latest","python /app/acts_app.py",detach=True,ports={"80/tcp":str(max_port)},remove=True)
                        print("new container with port %s is up and running"%(str(max_port)))
                        sql="insert into containers values('%s')"%(max_port)
                        cursor.execute(sql)
                        db.commit()
                        max_port=max_port+1

        else:
                pass
        cursor.close()
        time.sleep(120)
                

def threadCaller():
	while(1):
                watch()
                time.sleep(1)
t1=threading.Thread(target=threadCaller)
t1.daemon=True
t1.start()



app.run(debug=False,host="0.0.0.0",port="80")
