from flask import Flask,request,jsonify,json
import pymysql
import base64
import string
import random
import datetime
import pandas as pd
from collections import Counter
import requests



app=Flask(__name__)
user_container="DNS-loadbalancer:80"

#specify the ip of the database container
db=pymysql.connect("172.17.0.2","root","123","SelfieLessActs")
cursor=db.cursor()


request_count=0
server_health=True

@app.route('/api/v1/_health',methods=['GET'])
def health():
	resp=jsonify()
	if(server_health==True):
		resp.status_code=200
	else:
		resp.status_code=500
	#have to check for database connection status
	return resp

@app.route('/api/v1/_crash',methods=['POST'])
def crash():
	global server_health
	server_health=False
	resp=jsonify()
	resp.status_code=200
	return resp


def check_health():
	global server_health
	if(server_health==False):
		resp=jsonify()
		resp.status_code=500
		return resp
	return 0
@app.route('/api/v1/_count',methods=['GET','DELETE'])
def get_count():
	resp=check_health()
	if(resp!=0):
		return resp
	global request_count
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


@app.route('/api/v1/acts/count',methods=['GET'])
def acts_count():
	
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	#df=pd.read_csv('act_info.csv')
	sql="select * from  act_info;"
	total_acts=cursor.execute(sql)
	message=[]
	message.append(total_acts)
	resp=jsonify(message)
	resp.status_code=200
	
	return resp

#3 4
#200-ok 204-no content 405-bad method 400-server cannot process  the request.
@app.route('/api/v1/categories',methods=['GET','POST','DELETE'])
def list_categories():
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	if(request.method=='GET'):
		#category=pd.read_csv('category.csv')
		print("fetching data form category_table....")
		sql="select category_name from category;"
		cats=[]
		names=[]
		if(cursor.execute(sql)>0):
			cats=[ele[0] for ele in cursor.fetchall()]
		#cats=category['category_name']

		#act_info=pd.read_csv('act_info.csv')
		print("fetching data from  act_info table....")
		sql="select category_name from act_info;"
		if(cursor.execute(sql)>0):
			names=[ele[0] for ele in cursor.fetchall()]
		#names=act_info['category_name']

		message=dict(Counter(names)) #returns a dict

		print(message)

		
		if(len(cats)>=1):
			for ele in cats:
				if(ele not in message.keys()):
					message[ele]=0
			resp=jsonify(message)
			resp.status_code=200
			
			return resp
		else:
			message={}
			resp=jsonify(message)
			resp.status_code=204
			return resp
	elif(request.method=='POST'):

		#category=pd.read_csv('category.csv')
		#act_info=pd.read_csv('act_info.csv')
		json_data=request.json
		#print(json_data)
		message={}
		resp=jsonify(message)
		if(json_data==None):
			resp=jsonify(message)
			resp.status_code=400
			return	resp
		sql="select category_name from category;"
		cat=[]
		if(cursor.execute(sql)>0):
			cat=[ele[0] for ele in cursor.fetchall()]

		for ele in json_data:
			ele=str(ele)
			print(ele)
			
		
			if(ele in  cat):
				message={}
				resp=jsonify(message)
				resp.status_code=400
				return resp

				
			else:
				sql="insert into category values('%s')"%(ele)
				cursor.execute(sql)
				db.commit()
				resp.status_code=201
				
		#category.to_csv('category.csv',index=False)
		return resp;

	else:
		print("here")
		message={}
		resp=jsonify(message)
		resp.status_code=405
		return resp

#5	200-ok	400-server cannot porcess the request
@app.route('/api/v1/categories/<cat>',methods=['DELETE'])
def delete_category(cat):
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	if(cat!=None):
		#category=pd.read_csv('category.csv')
		#act_info=pd.read_csv('act_info.csv')

		#print(username.decode('utf-8'))

		cat=str(cat)
		# print(username,type(username))
		# df=pd.read_csv('users_data.csv')
		# print(df['username'])
		sql="delete from category where category_name='%s';"%(cat)
		if(cursor.execute(sql)>0):
			#df.drop([username],axis=0)
			#category=category[category.category_name != cat]
			#category.to_csv('category.csv',index=False)
			#db.commit()
			print("deleted category "+cat)
			#act_info=act_info[act_info.category_name != cat]
			#act_info.to_csv('act_info.csv',index=False)
			sql="delete from act_info where category_name='%s';"%(cat)
			cursor.execute(sql)
			db.commit()
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

@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def delete_act(actId):
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	if(actId!=None):
		#db=pymysql.connect('localhost','root','123','SelfieLessActs')

		#cursor=db.cursor()
		# act_info=pd.read_csv('act_info.csv')
		# df=pd.DataFrame(act_info)
		# df2=df["actId"]
		# df2=df2.tolist()
		# print(type(df2))
		# print(df2)
		# print(type(actId))
		print(actId)
		# actId=int(actId)
		# if(actId in df2):
		# 	#db.commit
		# 	print("act id matched")
		# 	df=df[df.actId != actId]
		# 	df.to_csv('act_info.csv',index=False)
		sql="delete from act_info where actId='%s';"%(actId)	
		if(cursor.execute(sql)<=0):
			print("invalid act id")
			message={}
			resp=jsonify(message)
			#db.close()
			resp.status_code=400
			return resp
		db.commit()
		message={}
		resp=jsonify(message)
		resp.status_code=200
		#db.close()
		
		return resp
	else:
		mesage=dict()
		resp=jsonify(mesage)
		resp.status_code=405
		return resp

@app.route('/api/v1/acts',methods=['POST'])
def upload_act():
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	l=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/','=','\n']
	json_data=request.json
	body = request.get_json()
	if(json_data==None):
		print("No data")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp
	#print(json_data.text)

	print("here")
	
	#db=pymysql.connect('localhost','root','123','SelfieLessActs')
	#cursor=db.cursor()
	#act_info=pd.read_csv('act_info.csv')
	#df=pd.DataFrame(act_info)
	# user_info=pd.read_csv('user_info.csv')
	# uf=pd.DataFrame(user_info)
	

	#cat_info=pd.read_csv('category.csv')
	#cf=pd.DataFrame(cat_info)	

	if("actId" not in body or "username" not in body or "timestamp" not in body or "caption" not in body or "imgB64" not in body or "categoryName" not in body):
		print("some field missing")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp

	#actId=int(json_data.get('actId'))
	actId=json_data.get('actId')
	print(actId)
	sql="select actId from  act_info  where actId='%s';"%(actId);
	
	#df2=df["actId"]
	#df2=df2.tolist()

	if(cursor.execute(sql)>0):
		print("Act Id already present")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp
	
	


	
	if("upvotes" in body):
		print("No upvotes field is to be set!")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return	resp

	username=json_data.get('username')
	print(username)
	print("checking username")

	headers={'Content-type':'application/json'}
	url="http://"+user_container+"/api/v1/users"
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200):
		print("empty file or bad request")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return	resp

	usr=r.json()
	print(usr,len(usr))

	if(username not in usr):
		print("username does not exists")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return	resp

	print("valid user checking time")
	
	time=json_data.get('timestamp')
	if(len(time)!=19):
		print("Timestamp format not correct!")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return	resp
	# else:
	# 	t=time.split(":")
	# 	ymd=t[0].split("-")
	# 	temp=ymd[0]
	# 	ymd[0]=ymd[2]
	# 	ymd[2]=temp
	# 	ymd='-'.join(ymd)

	# 	hhmmss=t[1].split('-')
	# 	temp=hhmmss[2]
	# 	hhmmss[2]=hhmmss[0]
	# 	hhmmss[0]=temp
	# 	hhmmss=':'.join(hhmmss)
	# 	time=' '.join([ymd,hhmmss])
	print(time)
	caption=json_data.get('caption')
	print(caption)
	print("checking whether image is in base64")
	a=body['imgB64']
	for i in range(len(a)-1):
		if a[i] not in l:
			print("imgB64 error")
			message={}
			resp=jsonify(message)
			resp.status_code=400
			return resp
		else:
			continue
	print("Is in base64")
	
	
	print("checking whther upvote field is present or not")
	upvote=json_data.get("upvote")
	if(upvote!=None):
		print(upvote)
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp
	
	print("upvote field not present")
	print("checking category exists?")
	category_name=json_data.get('categoryName')
	print(category_name)
	
	sql="select * from category where category_name='%s';"%(category_name)

	if(cursor.execute(sql)<=0):
		print("category does not exists")
		message={}
		resp=jsonify(message)
		resp.status_code=400
		return resp
	print("category exists")
	print("initiaiting insert")
	
	#temp=pd.DataFrame([[actId,username,time,caption,'0',a,category_name]],columns=['actId','username','datetime','caption','upvote','image_path','category_name'])
	sql="insert into  act_info values('%s','%s','%s','%s',%d,'%s','%s')"%(actId,username,time,caption,0,a,category_name)
	cursor.execute(sql)
	db.commit()
	#act_info=act_info.append(temp,ignore_index=True)
	#act_info.to_csv('act_info.csv',index=False)
	#cursor.execute("insert into act_info values(%s,%s,%s,%s,%s,%s,%s)",(actId,username,time,caption,'0',body['imgB64'],category_name))
	
	print("entering into database done")
	#db.commit()
	

	message={}
	resp=jsonify(message)
	resp.status_code=201
	
	return resp





#9	200-ok	400-bad request	405-method not allowed
@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	if(request.method=='POST'):
		json_data=request.json
		print(json_data)
		json_data[0]=str(json_data[0])
		# print(len(json_data))
		if(len(json_data)==1):
			
			# act_info=pd.read_csv('act_info.csv')
			#df=pd.read_csv("act_info.csv")
			sql="select actId from act_info where actId='%s'"%(json_data[0])
			if(cursor.execute(sql)<=0):
				message=[]
				print("invalid Id")
				resp=jsonify(message)
				resp.status_code=400
				return resp
			#df.loc[df['actId']==int(json_data[0]),'upvote']=df.loc[df['actId']==int(json_data[0]),'upvote']+1
			#df.to_csv('act_info.csv',index=False)
			sql="update act_info set upvote=upvote+1 where actId='%s'"%(json_data[0])
			cursor.execute(sql)
			db.commit()
			message=[]
			resp=jsonify(message)
			resp.status_code=200
			
			return resp
		else:
			message=[]
			print("arguments")
			resp=jsonify(message)
			resp.status_code=400
			return resp
	else:
		message={}
		print("invalid method")
		resp=jsonify(message)
		resp.status_code=405
		return resp


#6 200-ok	204-no content	405-mehtod not allowed	413-payload too large
#8	200	204	405	413
@app.route('/api/v1/categories/<cat>/acts')
def list_act_cat(cat):
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	if(request.method=='GET' and cat!=None):
		print(request.args)
		if("start" not in request.args):
			#category=pd.read_csv('category.csv')
			#act_info=pd.read_csv('act_info.csv')
			#print(act_info['category_name']=='cleaning')
			cat=str(cat)
			#res_cat=act_info[act_info['category_name']==cat]
			#print(res_cat)
			sql="select * from act_info where category_name='%s'"%(cat);
			freq=cursor.execute(sql)
			if(freq<=0):
				message=[]
				resp=jsonify(message)
				resp.status_code=204
				return resp
			message=[]
			resp=jsonify(message)	#extracting number of acts with in a category
			if(freq<100):
				print("here")
				#data_1=act_info[act_info['category_name']==cat]
				#print(type(data_1['datetime']))
				#data_1['datetime']=pd.to_datetime(data_1['datetime'])
				#data_1=data_1.sort_values(by='datetime',ascending=False)
				sql="select * from act_info where category_name='%s' order by datetime desc;"%(cat)
				if(cursor.execute(sql)>0):
					data_1=[ele for ele in cursor.fetchall()]
					for i in range(len(data_1)):
						#data=act_info[act_info['category_name']==cat]
						msg=dict()
						#data=list(data_1.iloc[i])
						data=data_1[i]
						msg['actId']=str(data[0])
						msg['username']=str(data[1])
						#msg['timestamp']=str(data[i][2])#converting date tiem object to str
						msg['timestamp']=str(data[2])
						msg['caption']=str(data[3])
						msg['upvote']=str(data[4])
						msg['imgB64']=str(data[5])
						msg['categoryName']=str(data[6])
						message.append(msg)
					resp=jsonify(message)
					resp.status_code=200
					
					return resp
				else:
					resp.status_code=204
					return resp
			else:
				resp.status_code=413
				return resp
		else:
			#category=pd.read_csv('category.csv')
			#act_info=pd.read_csv('act_info.csv')
			start=int(request.args['start'])
			end=int(request.args['end'])
			print(start)
			print(end)
			if(start ==0 or end==0 ):
				message=[]
				resp=jsonify(message)
				resp.status_code=204
				return resp
			if(end-start+1<100):

				cat=str(cat)
				
				#res_cat=act_info[act_info['category_name']==cat]
				sql="select * from act_info where category_name='%s'"%(cat)
				#freq=res_cat.shape[0]
				freq=cursor.execute(sql)
				if(freq<=0):
					message=[]
					resp=jsonify(message)
					resp.status_code=204
					return resp

				message=[]
				resp=jsonify(message)	#extracting number of acts with in a category
				if(freq<start or freq<end):
					message=[]
					resp=jsonify(message)
					resp.status_code=204
					return resp

				


				if(end-start+1<=100):
					
					#data_1=act_info[act_info['category_name']==cat]
					#data_1['datetime']=pd.to_datetime(data_1['datetime'])
					#data_1=data_1.sort_values(by='datetime',ascending=False)
					sql="select * from act_info where category_name='%s' order by datetime desc;"%(cat)
					if(cursor.execute(sql)>0):
						data_1=[ele for ele in cursor.fetchall()]
						for i in range(start-1,end):
							msg=dict()
							data=data_1[i]
							msg['actId']=str(data[0])
							msg['username']=str(data[1])
							msg['timestamp']=str(data[2])#converting date tiem object to str
							msg['caption']=str(data[3])
							msg['upvote']=str(data[4])
							msg['imgB64']=str(data[5])
							msg['categoryName']=str(data[6])
							message.append(msg)
						resp=jsonify(message)
						resp.status_code=200
						
						return resp
					else:
						resp.status_code=204
						return resp
				else:
					resp.status_code=413
					return resp
			else:
				#packet too big
				message={}
				resp=jsonify(message)
				resp.status_code=413
				return resp

	else:
		message={}
		resp=jsonify(message)
		resp.status_code=405
		return resp




@app.route("/api/v1/list_act_user/<username>",methods=["GET"])
def list_act_user(username):
	global request_count
	request_count+=1
	resp=check_health()
	if(resp!=0):
		return resp
	print(username,"in list act users ")
	#act_info=pd.read_csv('act_info.csv')
	if(request.method=="GET"):
		#d=act_info.loc[act_info['username']==username]
		#print(d)
		sql="select * from act_info where username='%s' order by datetime desc;"%(str(username))
		message=list()
		if(cursor.execute(sql)>0):
			print("here")
			d=[ele for ele in cursor.fetchall()]
			for i in  range(0,len(d)):
				msg=dict()
				data=d[i]
				
				msg['actId']=str(data[0])

				msg['username']=str(data[1])
				msg['timestamp']=str(data[2])#converting date tiem object to str
				msg['caption']=str(data[3])
				msg['upvote']=str(data[4])
				msg['imgB64']=str(data[5])
				msg['categoryName']=str(data[6])
				#print(msg)
				message.append(msg)
			#print(message)
			resp=jsonify(message)
			resp.status_code=200
			
			return resp
		else:
			message={}
			resp=jsonify(message)
			resp.status_code=204			
			return resp	
	else:
		message={}
		resp=jsonify(message)
		resp.status_code=405
		return resp
	
	

	
app.run(debug=False,host="0.0.0.0",port=80)
