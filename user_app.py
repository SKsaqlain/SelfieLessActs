from flask import Flask,request,jsonify,json
# import pymysql
import base64
import string
import random
import datetime
import pandas as pd
from collections import Counter
app=Flask(__name__)



request_count=0

@app.route('/api/v1/_count',methods=['GET','DELETE'])
def get_count():
	global  request_count
	if(request.method=='GET'):
		
		message=[]
		print("call to request_count",request_count)
		message.append(request_count)
		resp=jsonify(message)
		resp.status_code=200
		return resp
	elif(request.method=='DELETE'):
		request_count=0
		
		print("reset request_count",request_count)
		message={}
		resp=jsonify(message)
		resp.status_code=200
		return resp
	else:
		message={}
		resp=jsonify(message)
		resp.status_code=405
		return resp

		
#201-ok 400-bad request  405-method not allowed
#1
@app.route('/api/v1/users',methods=['POST'])
def insert_users():
	global request_count
	request_count+=1
	json_data=request.json
	
	username=json_data.get('username')
	password=json_data.get('password')

	if(username==None or password==None):
		print("username or password missing")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp

	if(not all(c in string.hexdigits for c in password)):
		print("password not in hex")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp


	# db=pymysql.connect('localhost','root','123','SelfieLessActs')
	# cursor=db.cursor()
	
	print(username,password)

	user_info=pd.read_csv('user_info.csv')

	dat=user_info[user_info['username'].str.match(username)]

	if(len(dat)==0):
		temp=pd.DataFrame([[username,password]],columns=['username','password'])
		user_info=user_info.append(temp,ignore_index=True)
		user_info.to_csv('user_info.csv',index=False)
		message={}
		resp=jsonify(message)
		resp.status_code=201
		
		return resp
	else:
		print("here")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp

#200 204 400 405
@app.route('/api/v1/validate_user',methods=['POST'])
def validate_users():
	global request_count
	json_data=request.json
	
	username=json_data.get('username')
	password=json_data.get('password')
	if(username==None or password==None):
		print("username or password missing")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp

	if(not all(c in string.hexdigits for c in password)):
		print("password not in hex")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp


	# db=pymysql.connect('localhost','root','123','SelfieLessActs')
	# cursor=db.cursor()
	
	print(username,password)

	user_info=pd.read_csv('user_info.csv')
	print("getting user info from data base")
	dat=user_info[user_info['username'].str.match(username)]
	print("checking ...")
	#the user naem does not exists
	if(len(dat)==0):
		print("username does not exists")
		message={}
		resp=jsonify(message)
		resp.status_code=204
		
		return resp
	elif(str(list(dat['password'])[0])!=password):
		print(str(list(dat['password'])[0]),password)
		print("wrong password")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp
	else:
		print("username and password matched")
		message={}
		resp=jsonify(message)
		resp.status_code=200
		request_count+=1
		return resp

#201-ok 400-bad request  405-method not allowed
#1
@app.route('/api/v1/users',methods=['GET'])
def list_users():
	global request_count
	request_count+=1
	# db=pymysql.connect('localhost','root','123','SelfieLessActs')
	# cursor=db.cursor()
	
	user_info=pd.read_csv('user_info.csv')

	dat=user_info.username


	if(len(dat)==0):
		message=[]
		resp=jsonify(message)
		resp.status_code=204
		return resp
	else:
	
		message=list(dat)
		resp=jsonify(message)
		resp.status_code=200
		
		return resp

	


#2 200-ok	400-bad request/the server will not process the request 405-method not allowed.
@app.route('/api/v1/users/<username>',methods=['DELETE'])
def delete_user(username):
	global request_count
	request_count+=1
	if(username!=None):
		user_info=pd.read_csv('user_info.csv')
		#print(username.decode('utf-8'))

		username=str(username)

		dat=user_info[user_info['username'].str.match(username)]
		if(len(dat)==1):
			user_info=user_info[user_info.username != username]
			user_info.to_csv('user_info.csv',index=False)
			print("deleted user "+username)
			message={}
			resp=jsonify(message)
			resp.status_code=200
			
			return resp
		else:
			
			message={}
			resp=jsonify(message)
			resp.status_code=400
			return resp
	else:
		message={}
		resp=jsonify(message)
		resp.status_code=405
		return resp

app.run(debug=True,host="127.0.0.1",port=80)