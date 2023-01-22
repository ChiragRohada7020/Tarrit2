from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for,session
from flask import Blueprint
from Home.index import index
from Home.User.user import user
from flask_cors import CORS

from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message
import random
import pymongo

app = Flask(__name__)
CORS(app)



#------------------------------------Some Important inside-----------------------------------


app.secret_key=os.urandom(24)
app.config['UPLOAD_FOLDER']='./static/img'
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["IOT"]


#-------------------------- App Clone --------------------------------

app.register_blueprint(index)

app.register_blueprint(user)



#--------------------------Mail Config-------------------------------







mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kjseit.q@gmail.com'
app.config['MAIL_PASSWORD'] = 'ghkwfpxqlicxlfch'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
global n,otpp
n = random.randint(1000,9999)

#-------------------------------------------------------------------------









@app.route("/sign_up",methods = ['POST', 'GET'])
def sign_up():
    global n
    
    
    try:

        if request.method == 'POST':
            user_name=request.form['name']
            user_password=request.form['password']
            user_email=request.form['email']
            user_password = bcrypt.generate_password_hash(user_password)
      

        
   
            mycol = mydb['Users']
            x=mycol.find_one({"email":user_email})
            if x:
              return render_template('SignUp/sign-up.html',error="email aleardy registered")
            else:
          

          
              n = random.randint(1000,9999)
    
      

    

      
           

      
      

      
      
           
        
      
              msg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [user_email]
               )
              msg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. Use the following OTP to complete your Sign Up procedures. Its a one time otp</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">"""+str(n)+"""</h2>
      <p style="font-size:0.9em;">Regards,<br />Pbl Project</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Pbl Project</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
      
            mail.send(msg)
   
   
            return redirect(url_for('check',email=user_email,password=user_password,name=user_name))
    
        return render_template("SignUp/sign-up.html",error="")
    except Exception as e:
        print("hello")
        






@app.route("/check/<email>/<password>/<name>",methods = ['POST', 'GET'])
def check(email,password,name):

    global n,otpp
  
  
    print("hell000o")

  
    if request.method == 'POST':
        otp=request.form['otp']
     
      
        if (str(n) == str(otp)):
            
            msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [email]
               )
            msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. We will contact you soon</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;"></h2>
      <p style="font-size:0.9em;">Regards,<br />Pbl Project</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Pbl Project</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
       
        
            mail.send(msgg)
   
            mycol = mydb["Users"]
            mycol.insert_one({"email":email,"name":name,"password":password})
            n = random.randint(1000,9999)
       
        
            return redirect(url_for('index.login'))
        else:
            n = random.randint(1000,9999)
        
        
            text="invalid email"
            return redirect(url_for('sign_up'))







    return render_template('check.html',email=email,name=name,password=password)

