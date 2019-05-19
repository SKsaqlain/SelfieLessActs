from flask import Flask,request,jsonify,json,render_template,redirect,url_for
import requests
import base64
import random
import string
import hashlib
from werkzeug import secure_filename
import datetime
import os
import random
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='./static/images'


username=''

user_container="0.0.0.0:8080"
acts_container="0.0.0.0:8000"
flag=0
@app.route("/")
def home():
	return render_template('home.html')


@app.route("/login",methods=['POST'])
def login():
	global username
	headers={'Content-type':'application/json'}
	global flag
	if(flag==0):
		username=request.form['username']
		sha_1=hashlib.sha1()
		sha_1.update(request.form['password'])
		
		password=sha_1.hexdigest()
		print(password)
		url="http://"+user_container+"/api/v1/validate_user"
		payload={"username":username,"password":password}
		headers={'Content-type':'application/json'}
		status=0
		try:
			r=requests.post(url,data=json.dumps(payload),headers=headers)
			status=r.status_code
		except:
			return render_template('home.html')
		if(status!=200):
			return render_template('home.html')
		flag=1

	url="http://"+acts_container+"/api/v1/categories"
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200):
		return str(r.status_code)
	cat=r.json()
	print(cat,len(cat))

	url="http://"+acts_container+"/api/v1/list_act_user/"+username
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200 and r.status_code!=204):
		return str(r.status_code)
	if(r.status_code==204):
		return render_template('category.html',result=cat)

	act=r.json()
	#print(act,len(act))

	return render_template('login_category.html',result={"cat":cat,"act":act})

@app.route("/signup",methods=['POST'])
def signup():
	global username
	global flag
	username=request.form['username']
	sha_1=hashlib.sha1()
	sha_1.update(request.form['password'])
	
	password=sha_1.hexdigest()
	print(password)
	url="http://"+user_container+"/api/v1/users"
	payload={"username":username,"password":password}
	headers={'Content-type':'application/json'}
	status=0
	try:
		r=requests.post(url,data=json.dumps(payload),headers=headers)
		status=r.status_code
	except:
		return render_template('home.html')
	if(status!=201):
		return render_template('home.html')

	url="http://"+acts_container+"/api/v1/categories"
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200):
		return str(r.status_code)
	x=r.json()
	print(x,len(x))

	return render_template('category.html',result=x)



@app.route('/list_acts',methods=['GET'])
def list_acts():
	cat=request.args['cat']
	print(cat)
	headers={'Content-type':'application/json'}
	url="http://"+acts_container+"/api/v1/categories/"+cat+"/acts"
	r=requests.get(url,data={},headers=headers)
	print(r.status_code)
	if(r.status_code!=200):
		return str(r.status_code)
	x=r.json()
	# for i in range(len(x)):
	# 	decoded_image=base64.decodestring(x[i]['imgB64'])
	# 	random_filename=''.join([random.choice(string.ascii_letters+string.digits) for n in range(10)])+".jpg"
	# 	image_result=open("./static/images/"+random_filename,'wb')
	# 	image_result.write(decoded_image)
	# 	x[i]['imgB64']=random_filename
	#print(x)
	return render_template('acts.html',result=x)


@app.route('/upvote',methods=['POST'])
def upvote():
	actId=request.form['actId']
	print(actId)
	headers={'Content-type':'application/json'}
	url="http://"+acts_container+"/api/v1/acts/upvote"
	r=requests.post(url,json=[actId],headers=headers)
	print(r.status_code)
	return str(r.status_code)


@app.route('/delete',methods=['POST'])
def delete_act():
	actId=request.form['actId']
	print(actId)
	headers={'Content-type':'application/json'}
	url="http://"+acts_container+"/api/v1/acts/"+actId
	r=requests.delete(url,data={},headers=headers)
	print(r.status_code)

	return(str(r.status_code))




@app.route('/upload_act',methods=['POST'])
def upload_act():
	
	f=request.files['file']
	print(f,f.filename)
	filename=username+f.filename
	f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

	image=open('./static/images/'+filename,'rb')
	image_read=image.read()
	image_64_encode=base64.encodestring(image_read)
	
	category=request.form['category']
	caption=request.form['caption']
	time=str(datetime.datetime.now())
	
	t=str(time).split(" ")
	dmy=t[0].split("-")
	temp=dmy[2]
	dmy[2]=dmy[0]
	dmy[0]=temp
	dmy="-".join(dmy)
	hhmmss=t[1].split(":")
	temp=hhmmss[0]
	hhmmss[0]=hhmmss[2]
	hhmmss[2]=temp
	hhmmss[0]=hhmmss[0].split(".")[0]
	hhmmss="-".join(hhmmss)
	t=":".join([dmy,hhmmss])
	time=t
	print(time)
	actId=str(random.randint(500,1000))
	imgB64=image_64_encode

	imgB64=str(imgB64)
	imgB64=imgB64[:-1]
	print(imgB64[-15:])
	headers={'Content-type':'application/json'}
	url="http://"+acts_container+"/api/v1/acts"
	r=requests.post(url,json={"actId":actId,"timestamp":time,"username":username,"caption":caption,"imgB64":imgB64,"categoryName":category},headers=headers)
	print(r.status_code)
	if(r.status_code!=201):
		return str(r.status_code)
	# url="http://"+acts_container+"/api/v1/categories"
	# r=requests.get(url,data={},headers=headers)
	# print(r.status_code)
	# if(r.status_code!=200):
	# 	return str(r.status_code)
	# x=r.json()

	# return render_template('category.html',result=x)
	url="http://"+acts_container+"/api/v1/categories"
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200):
		return str(r.status_code)
	cat=r.json()
	print(cat,len(cat))

	url="http://"+acts_container+"/api/v1/list_act_user/"+username
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200 and r.status_code!=204):
		return str(r.status_code)
	if(r.status_code==204):
		return render_template('category.html',result=cat)

	act=r.json()
	#print(act,len(act))

	return render_template('login_category.html',result={"cat":cat,"act":act})

@app.route("/upload_category",methods=["POST"])
def upload_category():
	category=request.form["category"]
	print(category)
	message=[category]
	headers={'Content-type':'application/json'}
	url="http://"+acts_container+"/api/v1/categories"
	r=requests.post(url,json=message,headers=headers)
	print(r.status_code)
	if(r.status_code!=201):
		return str(r.status_code)
	url="http://"+acts_container+"/api/v1/categories"
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200):
		return str(r.status_code)
	cat=r.json()
	print(cat,len(cat))

	url="http://"+acts_container+"/api/v1/list_act_user/"+username
	r=requests.get(url,data={},headers=headers)
	if(r.status_code!=200 and r.status_code!=204):
		return str(r.status_code)
	if(r.status_code==204):
		return render_template('category.html',result=cat)

	act=r.json()
	#print(act,len(act))

	return render_template('login_category.html',result={"cat":cat,"act":act})
	# url="http://"+acts_container+"/api/v1/categories"
	# r=requests.get(url,data={},headers=headers)
	# print(r.status_code)
	# if(r.status_code!=200):
	# 	return str(r.status_code)
	# x=r.json()

	# return render_template('category.html',result=x)

app.run(debug=True,host='0.0.0.0',port=3000)