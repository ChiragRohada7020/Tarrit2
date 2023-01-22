from flask import Blueprint
from distutils.log import error
import os

from logging import exception
from pickletools import float8
from flask import Flask
from flask import render_template
import pymongo
from flask_mail import Mail, Message

from flask import request
from flask import abort, redirect, url_for,session
from flask_cors import CORS



from flask_bcrypt import Bcrypt


myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]

index =Blueprint('index',__name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key=os.urandom(24)


#--------------------------------------------  USER LOGOUT ------------------------------------------

@index.route("/home")
def Home2():
    try:
        if 'user_id' in session:
        
          

          return render_template('index.html',allowed="Logout") 
        return render_template('index.html',allowed="Login") 
    except:
      return render_template('error.html')


@index.route("/")
def Home():
    
  try:
        if 'user_id' in session:
        
          

          return render_template('index.html',allowed="Logout") 
        return render_template('index.html',allowed="Login") 
  except:
    return render_template('error.html')

  


@index.route("/login",methods = ['POST', 'GET'])
def login():
    
    
    error=""

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      


      try:
          mycol = mydb['Users']
          x= mycol.find_one({"email":email})
          
          if(bcrypt.check_password_hash(x['password'], password)):
            
            session['user_id']=x["email"]
            return redirect(url_for('user.user_index'))
          else:
            error="invalid credential"
            return render_template('SignUp/login.html',error=error)
      except:
          return render_template('error.html')
    else:
       return render_template('SignUp/login.html',error=error)




#---------------------------------------------  USER INDEX----------------------------------------------

@index.route("/logout")
def user_logout():
    session.pop('user_id')
    
    return redirect(url_for('index.Home'))





