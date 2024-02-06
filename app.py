from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for,session
from flask import Blueprint

from flask_cors import CORS

from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message
import random
import pymongo




app = Flask(__name__)
CORS(app)
#---------------------------Importing other files --------------------------




from Home.index import index
from Home.User.user import user
from Home.Admin.admin import admin
from Home.Staff.staff import staff
from Home.Hospital.hospital import hospital





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

app.register_blueprint(admin)

app.register_blueprint(staff)

app.register_blueprint(hospital)





#--------------------------Mail Config-------------------------------







mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info.puppymatch@gmail.com'
app.config['MAIL_PASSWORD'] = 'icbi xxir gtmj lset'
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
                sender ='info.puppymatch@gmail.com',
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
                sender ='info.puppymatch@gmail.com',
                recipients = [email]
               )
            msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.shutterstock.com/image-vector/ambulance-car-cartoon-style-kids-600nw-2403135027.jpg" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. We will contact you soon</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;"></h2>
      <p style="font-size:0.9em;">Regards,<br />Taarit</p>
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





#-------------------------------ADMIN GIving ID-----------------------------

@app.route("/give_no/<id>")
def give_no(id):
    print(id)
    
    
    mycol = mydb["vehicle"]
    x=mycol.find({"vehicle_no":id})
    for i in x:
       print(i)
      #  mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':i['_id']}})
       mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':1}})
       msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [i['email']]
               )
       msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. Your vehicle no :-"""+i['vehicle_no'] +""" is ready to go</p>
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
    
    # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
       return redirect(url_for('admin.admin_user_data'))



#----------------------------------------------------------ADMIN ID ASSIGN-----------------------------------------------

@app.route("/assign/<id>")
def assign(id):
    print(id)
    
    
    mycol = mydb["vehicle"]
    x=mycol.find({"vehicle_no":id})
    for i in x:
       print(i)
       mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':str(i['_id'])}})
       
       msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [i['email']]
               )
       msgg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://www.iotforall.com/wp-content/uploads/2017/05/IoT-For-All-Logo.png" alt="img1" style="height: 100px ;width: 110px;"><h3>Pbl Project</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing Saftey Vehicle. Your vehicle no :-"""+i['vehicle_no'] +""" is ready to go</p>
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
    
    # mycol.update_one({'vehicle_no':id},{"$set":{'iot_id':"kjhk"}})
       return redirect(url_for('admin.admin_index'))


@app.route("/user_data/<id>")
def user_data(id):
  mycol = mydb['vehicle']
  y=mycol.find({'vehicle_no':id},{'_id':0})
  
  return y[0]








@app.route("/hospital_sign_up",methods = ['POST', 'GET'])
def hospital_sign_up():
    global n
    
    
    try:

        if request.method == 'POST':
            hospital_name=request.form['hospital_name']
            hospital_password=request.form['password']
            hospital_email=request.form['email']
            hospital_pincode=request.form['pincode']
            hospital_password = bcrypt.generate_password_hash(hospital_password)
      

        
   
            mycol = mydb['Hospital']
            x=mycol.find_one({"email":hospital_email})
            if x:
              return render_template('Hospital/sign-up.html',error="email aleardy registered")
            else:
          

          
              n = random.randint(1000,9999)
              session['hospital_otp']=n
    
      

    

      
           

      
      

      
      
           
        
      
              msg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [hospital_email]
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
   
   
            return redirect(url_for('hospital_check',email=hospital_email,password=hospital_password,name=hospital_name,pincode=hospital_pincode))
    
        return render_template("Hospital/sign-up.html",error="")
    except Exception as e:
        print("hello")
        






@app.route("/hospital_check/<email>/<password>/<name>/<pincode>",methods = ['POST', 'GET'])
def hospital_check(email,password,name,pincode):

    global n,otpp
  
  
    print("hell000o")

  
    if request.method == 'POST':
        otp=request.form['otp']
     
      
        if (str(session['hospital_otp']) == str(otp)):
            
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
            mycol.insert_one({"email":email,"name":name,"password":password,"hospital_pincode":pincode})
            n = random.randint(1000,9999)
            session['hospital_otp']=n
       
        
            return redirect(url_for('index.login'))
        else:
            n = random.randint(1000,9999)
            session['hospital_otp']=n
        
        
            text="invalid email"
            return redirect(url_for('sign_up'))







    return render_template('Hospital/check.html',email=email,name=name,password=password,pincode=pincode)

