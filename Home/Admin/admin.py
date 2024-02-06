from flask import Blueprint
from distutils.log import error
from logging import exception
from pickletools import float8
from flask import render_template
import pymongo
from flask import request
from flask import abort, redirect, url_for,session
import requests
from datetime import date
import numpy as np
import time
import timedelta


myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]

admin =Blueprint('admin',__name__)


def closest(lst, K):
      
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]
#---------------------------------------ADMIN LOGIN ------------------------------------------------------

@admin.route("/admin_login",methods = ['POST', 'GET'])
def admin_login():
    print("hello")
    
    
    error=""
    if 'admin_login' in session:
        print("ho gaya")
        return render_template('admin_index.html')

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
            # pincode = requests.get("https://api.geoapify.com/v1/geocode/reverse?lat=" +
            # str(lat) +
            # "&lon=" +
            # str(log) +
            # "&apiKey=52562d2110f34015a23116a33cc56c65")
            # postcode=pincode.json()
            # myloc=postcode['features'][0]['properties']['suburb']
            # postcode=postcode['features'][0]['properties']['postcode']
            
            # print(postcode)
            myloc=424201
            postcode=424201
            pos=0

            
          except:
              time.sleep(2)
              print("i m")
              pos=1
        

      

      
      
      
      

      if(float(log)):
        try:
          mycol = mydb['Admin']
          x=mycol.find_one({"email":email,"password":password})
          if(x):
            
            session['admin_id']=x["email"]
            session['admin_loc']=[lat,log,postcode,myloc]
            accident_count=0
            mycol = mydb["accident"]
            accident=mycol.find({"postcode":postcode})
            for i in accident:
              accident_count=accident_count+1

            session['accident']=accident_count
            

            

            return redirect(url_for('admin.admin_index'))
        except:
          error="Invalid Email"
        else:
          error="Invalid Email"

      else:
        error="Allow Location!"
        



    
      
    return render_template('Admin/admin_login.html',error=error)


#------------------------------------------------------------ADMIN INDEX---------------------------------------------------

@admin.route("/admin_index")
def admin_index():
    error=" "
    if 'admin_id' and 'admin_loc' in session:
      try:
        lat=session['admin_loc'][0]
        log=session['admin_loc'][1]
        myloc=session['admin_loc'][3]

        

      
           
        print("hello"+session['admin_loc'][0])
        mycol = mydb['accident']
        y=mycol.find({'postcode':session['admin_loc'][2],'user_rescued':1})
        total=0
        for i in y:
          total=total+1
        
        return render_template('Admin/admin_index.html',myloc=myloc,user_rescued=total)
      except:
        error="allow location"
        


        
    return render_template('Admin/admin_login.html',error=error)


#--------------------------------------------------------ADMIN LOGOUT-----------------------------------


@admin.route("/admin_logout")
def admin_logout():
    session.pop('admin_id')
    session.pop('admin_loc')
    return redirect(url_for('admin.admin_login'))




#-----------------------------------------ADMIN ACCIDENT -----------------------------------

@admin.route("/admin_accident")
def accident():
  try:

    if 'admin_id' in session:
    
      mycol = mydb["accident"]
      x=mycol.find({})
      return render_template('accident.html',accident=x)
    else:
      return redirect(url_for('admin.admin_login'))

  except:
    return 'error occur n'



@admin.route("/admin_data",methods = ['POST', 'GET'])
def admin_data():
  try:

    if 'admin_id' in session:
    


      mycol = mydb["Users"]
      data=mycol.find({}).limit(3)
      if request.method == 'POST':
        user=request.form['user']
        data=mycol.find({"$text": {"$search": user}}).limit(5)

    
    
        
        
    
        

        

    
        
          
      return render_template('Admin/admin_data.html',data=data)
    else:
      return redirect(url_for('admin.admin_login'))

  except:
    return 'error occur n'




@admin.route("/admin_user_data")
def admin_user_data():
    error=" "
    if 'admin_id' and 'admin_loc' in session:
      try:
        lat=session['admin_loc'][0]
        log=session['admin_loc'][1]
        

        

        
        myloc=session['admin_loc'][3]
        print(myloc)
           
        print("hello"+session['admin_loc'][0])
        mycol = mydb['vehicle']
        x=mycol.find({"iot_id":None})
        y=mycol.find({"iot_id":1})
        print(x)
        return render_template('Admin/user_data.html',data=x,data2=y,myloc=myloc)
      except:
        error="allow location"
        


        
    return render_template('Admin/admin_login.html',error=error)





@admin.route("/user_accident")
def user_accident():
  try:

    if 'admin_id' in session:
      postcode=session['admin_loc'][2]
      print(postcode)
      mycol = mydb["accident"]
      x=mycol.find({'postcode':postcode,'user_rescued':0})
      y=mycol.find({'postcode':postcode,'user_rescued':1})
      return render_template('Admin/inbox.html',accident=x,user_rescued=y)
    else:
      return redirect(url_for('admin.admin_login'))

  except:
    return 'error occur n'


@admin.route("/iot/<string:id>/<lat>/<log>")
def iot(id,lat,log):
    try:    
           
            # mycol = mydb["vehicle"]
            # mycol.find({'iot_id':id})
            # iot_id=request.form['iot_id']
            # location=request.form['location']
            # location=location.split(',')
            mycol = mydb["vehicle"]
            data=mycol.find({"iot_id":id}) 
            for i in data :
              vehicle_no=i["vehicle_no"]
              email=i['email']
              print(email)
              pincode = requests.get("https://api.geoapify.com/v1/geocode/reverse?lat=" +
              str(lat) +
              "&lon=" +
              str(log) +
              "&apiKey=52562d2110f34015a23116a33cc56c65")

              
              postcode=pincode.json()
              postcode=postcode['features'][0]['properties']['postcode']
              print(postcode)
            
            mycol = mydb["accident"]
            today = date.today() 
            print(today)
            today=str(today)

            

            mycol.insert_one({"iot_id":id,"location":[float(lat),float(log)],"vehicle_no":vehicle_no,"email":email,"critical":1,"postcode":postcode,"date":today,"staff_email":"","staff_name":"","user_rescued":0})

            print(id)
            
            return "data send"
    except:
        print("Not valid")





@admin.route("/accident_count",methods = ['POST', 'GET'])
def accident_count():
  try:

    if 'admin_id' in session:
      y=0
      postcode=session['admin_loc'][2]
      mycol = mydb["accident"]
      print(postcode)
      x=mycol.find({"postcode":postcode})
      for i in x:
        y=y+1

      if(y>=session['accident']):
        count=y-session['accident']
        return {"hello":count}

      return {"hello":0}

  except:  
    return "error occur"


@admin.route("/accident_count_detected",methods = ['POST', 'GET'])
def accident_count_detected():
  try:
    y=0
    if 'admin_id' in session:
      mycol = mydb["accident"]
      x=mycol.find({})
      for i in x:
        y=y+1
      session['accident']=y

      return {"hello":y}

  except:  
    return "error occur"


@admin.route("/today_accident_count",methods = ['POST', 'GET'])
def today_accident_count():
  try:
    y=0
    if 'admin_id' in session:
      mycol = mydb["accident"]
      today = date.today() 
      
      
      print(today)
      today=str(today)
      x=mycol.find({'date':today})
      for i in x:
        y=y+1
      

      return {"today_accident":y}

  except:  
    return "error occur"









@admin.route("/admin_staff_data/<id>")
def user_data(id):
  mycol = mydb['accident']
  y=mycol.find({'vehicle_no':id},{'_id':0})
  
  return y[0]


