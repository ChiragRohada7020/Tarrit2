from flask import Blueprint
from distutils.log import error
from logging import exception
from pickletools import float8
from flask import render_template
import pymongo
from flask import request
from flask import abort, redirect, url_for,session
import requests
import time
import numpy as np


myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]

staff =Blueprint('staff',__name__)


def closest(lst, K):
      
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]
#---------------------------------------ADMIN LOGIN ------------------------------------------------------

@staff.route("/staff_login",methods = ['POST', 'GET'])
def staff_login():
    
    
    error=""
    if 'staff_login' in session:
        return redirect(url_for('staff.staff_index'))

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      lat=request.form['lat']
      log=request.form['log']
      print(log,lat,"hello" )
      pos=1
      if(float(log)):
        
        while(pos):

          try:
            pincode = requests.get("https://api.geoapify.com/v1/geocode/reverse?lat=" +
            str(lat) +
            "&lon=" +
            str(log) +
            "&apiKey=52562d2110f34015a23116a33cc56c65")
            postcode=pincode.json()
            postcode=postcode['features'][0]['properties']['postcode']
            print(postcode)
            pos=0

            
          except:
              time.sleep(2)
              print("i m")
              pos=1
      
      

      if(float(log)):
        try:
          mycol = mydb['Staff']
          x=mycol.find_one({"email":email,"password":password})
          if(x):
            
            session['staff_id']=x["email"]
            session['staff_name']=x["name"]
            session['staff_loc']=[lat,log,postcode]
            
            
            

            

            return redirect(url_for('staff.staff_index'))
        except:
          error="Invalid Email"
        else:
          error="Invalid Email"

      else:
        error="Allow Location!"
        



    
      
    return render_template('Staff/staff_login.html',error=error)


#------------------------------------------------------------ADMIN INDEX---------------------------------------------------

@staff.route("/staff_index")
def staff_index():
    try:

        if 'staff_id' in session:
            postcode=session['staff_loc'][2]
            mycol = mydb["accident"]
            x=mycol.find({'postcode':postcode,'critical':1})
            y=mycol.find({'postcode':postcode,'critical':0,'staff_email':session['staff_id']})
            return render_template('Staff/inbox2.html',accident=x,myloc=postcode,to_rescued=y)
        else:
            return redirect(url_for('staff.staff_login'))

    except:
         return 'error occur n'


#--------------------------------------------------------ADMIN LOGOUT-------------------------------------------------------


@staff.route("/staff_logout")
def staff_logout():
    session.pop('staff_id')
    session.pop('staff_loc')
    return redirect(url_for('staff.staff_login'))







@staff.route("/staff_rescued/<id>")
def staff_rescued(id):
    print(id)
    
    
    mycol = mydb["accident"]
    
   
    x=mycol.find({"vehicle_no":id})
    for i in x:
       
      #  mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':i['_id']}})
       mycol.update_one({'vehicle_no':id},{"$set":{'user_rescued':1}})

    
    # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
       return redirect(url_for('staff.staff_index'))




@staff.route("/staff_help/<id>")
def give_no(id):
    print(id)
    
    
    mycol = mydb["accident"]
    mycol2 = mydb["Staff"]
    y=mycol2.find({"email": session['staff_id']})
    for i in y:
      mycol.update_one({'vehicle_no':id},{"$set":{'staff_email':i['email'],"staff_name":i['name']}})
      
    x=mycol.find({"vehicle_no":id})
    for i in x:
       print(i)
      #  mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':i['_id']}})
       mycol.update_one({'vehicle_no':id},{"$set":{'critical':0}})

    
    # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
       return redirect(url_for('staff.staff_index'))

#-----------------------------------------ADMIN ACCIDENT -----------------------------------

# @admin.route("/admin_accident")
# def accident():
#   try:

#     if 'admin_id' in session:
    
#       mycol = mydb["accident"]
#       x=mycol.find({})
#       return render_template('accident.html',accident=x)
#     else:
#       return redirect(url_for('admin.admin_login'))

#   except:
#     return 'error occur n'




# @admin.route("/admin_user_data")
# def admin_user_data():
#     error=" "
#     if 'admin_id' and 'admin_loc' in session:
#       try:
#         lat=session['admin_loc'][0]
#         log=session['admin_loc'][1]
        

#         x = requests.get("https://api.geoapify.com/v1/geocode/reverse?lat=" +
#         str(lat) +
#         "&lon=" +
#         str(log) +
#         "&apiKey=52562d2110f34015a23116a33cc56c65")

#         myloc=x.json()
#         myloc=myloc['features'][0]['properties']['suburb']
#         print(myloc)
           
#         print("hello"+session['admin_loc'][0])
#         mycol = mydb['vehicle']
#         x=mycol.find({"iot_id":None})
#         y=mycol.find({"iot_id":1})
#         print(x)
#         return render_template('Admin/user_data.html',data=x,data2=y,myloc=myloc)
#       except:
#         error="allow location"
        


        
#     return render_template('Admin/admin_login.html',error=error)





# @admin.route("/user_accident")
# def user_accident():
#   try:

#     if 'admin_id' in session:
#       postcode=session['admin_loc'][2]
#       mycol = mydb["accident"]
#       x=mycol.find({'postcode':postcode})
#       return render_template('Admin/inbox.html',accident=x)
#     else:
#       return redirect(url_for('admin.admin_login'))

#   except:
#     return 'error occur n'


# @admin.route("/iot/<string:id>/<lat>/<log>")
# def iot(id,lat,log):
#     try:    
           
#             # mycol = mydb["vehicle"]
#             # mycol.find({'iot_id':id})
#             # iot_id=request.form['iot_id']
#             # location=request.form['location']
#             # location=location.split(',')
#             mycol = mydb["vehicle"]
#             data=mycol.find({"iot_id":id}) 
#             for i in data :
#               vehicle_no=i["vehicle_no"]
#               email=i['email']
#               print(email)
#               pincode = requests.get("https://api.geoapify.com/v1/geocode/reverse?lat=" +
#               str(lat) +
#               "&lon=" +
#               str(log) +
#               "&apiKey=52562d2110f34015a23116a33cc56c65")


#               postcode=pincode.json()
#               postcode=postcode['features'][0]['properties']['postcode']
#               print(postcode)
            
#             mycol = mydb["accident"]

#             mycol.insert_one({"iot_id":id,"location":[float(lat),float(log)],"vehicle_no":vehicle_no,"email":email,"critical":1,"postcode":postcode})

#             print(id)
            
#             return "data send"
#     except:
#         print("Not valid")





# @admin.route("/accident_count",methods = ['POST', 'GET'])
# def accident_count():
#   try:

#     if 'admin_id' in session:
#       y=0
#       mycol = mydb["accident"]
#       x=mycol.find({})
#       for i in x:
#         y=y+1

#       if(y>=session['accident']):
#         count=y-session['accident']
#         return {"hello":count}

#       return {"hello":0}

#   except:  
#     return "error occur"


# @admin.route("/accident_count_detected",methods = ['POST', 'GET'])
# def accident_count_detected():
#   try:
#     y=0
#     if 'admin_id' in session:
#       mycol = mydb["accident"]
#       x=mycol.find({})
#       for i in x:
#         y=y+1
#       session['accident']=y

#       return {"hello":y}

#   except:  
#     return "error occur"