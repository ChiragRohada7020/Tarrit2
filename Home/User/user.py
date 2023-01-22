from flask import Blueprint
from distutils.log import error
import os

from logging import exception
from pickletools import float8
from flask import Flask
from flask import render_template
import pymongo
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

from flask import request
from flask import abort, redirect, url_for,session



from flask_bcrypt import Bcrypt


myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]

user =Blueprint('user',__name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER']='./static/UserUpload'





@user.route("/user_index")
def user_index():
    if 'user_id' in session:

        mycol = mydb["vehicle"]
        data=mycol.find({"email":session['user_id']})
        return render_template('User/user_index.html',allowed="Logout",type1="logout",data=data)
    else:
        return redirect(url_for('index.login'))


@user.route("/vehicle",methods = ['POST', 'GET'])
def add_vehicle():
    if 'user_id' in session:
        try:
            if request.method == 'POST':
                vehicle_no=request.form['vehicle_no']
                first_name=request.form['first_name']
                mobile_no=request.form['mobile_no']
                vehicle_name=request.form['vehicle_name']
                address=request.form['address']
                
                f = request.files['file']
                print(f)
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], vehicle_no+'.png' ))

                mycol = mydb["vehicle"]
                mycol.insert_one({"vehicle_no":vehicle_no,"email":session['user_id'],"iot_id":None,"mobile_no":mobile_no,"vehicle_name":vehicle_name,"first_name":first_name,"address":address})
            return redirect(url_for('user.user_index'))
        except:
            return render_template('vehicle.html')
    else:
        return render_template('error.html')