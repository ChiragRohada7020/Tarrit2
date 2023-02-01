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

hospital =Blueprint('hospital',__name__)


def closest(lst, K):
      
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]
#---------------------------------------ADMIN LOGIN ------------------------------------------------------

@hospital.route("/hospital_login",methods = ['POST', 'GET'])
def hospital_login():
    
    
    error=""
    if 'hospital_id' in session:
        return redirect(url_for('hospital.hospital_index'))

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      lat=request.form['lat']
      log=request.form['log']
      print(log,lat,"hello" )
      pos=1
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
            
            session['hospital_id']=x["email"]
            session['hospital_loc']=[lat,log,postcode]
            
            
            

            

            return redirect(url_for('hospital.hospital_index'))
        except:
          error="Invalid Email"
        else:
          error="Invalid Email"

      else:
        error="Allow Location!"
        



    
      
    return render_template('Hospital/login.html',error=error)


#------------------------------------------------------------ADMIN INDEX---------------------------------------------------

# @staff.route("/staff_index")
# def staff_index():
#     try:

#         if 'staff_id' in session:
#             postcode=session['staff_loc'][2]
#             mycol = mydb["accident"]
#             x=mycol.find({'postcode':postcode,'critical':1})
#             return render_template('Staff/inbox2.html',accident=x,myloc=postcode)
#         else:
#             return redirect(url_for('staff.staff_login'))

#     except:
#          return 'error occur n'


#--------------------------------------------------------ADMIN LOGOUT-------------------------------------------------------


# @staff.route("/staff_logout")
# def staff_logout():
#     session.pop('staff_id')
#     session.pop('staff_loc')
#     return redirect(url_for('staff.staff_login'))








# @staff.route("/staff_help/<id>")
# def give_no(id):
#     print(id)
    
    
#     mycol = mydb["accident"]
#     x=mycol.find({"vehicle_no":id})
#     for i in x:
#        print(i)
#       #  mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':i['_id']}})
#        mycol.update_one({'vehicle_no':id},{"$set":{'critical':0}})

    
#     # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
#        return redirect(url_for('staff.staff_index'))



