f=open("act_info.csv","w")
f.write("actId,username,datetime,caption,upvote,image_path,category_name\n")
f.close()

f=open("category.csv","w")
f.write("category_name\n")
f.close()

f=open("user_info.csv","w")
f.write("username,password\n")
f.close()
