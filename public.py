from flask import *
from database import *
import os
import uuid

from face_model import *


public=Blueprint('public',__name__)


@public.route("/",methods=['post','get'])
def home():
   
    return render_template("home.html")


@public.route("/login",methods=['post','get'])
def login():
    if 'submit' in request.form:
        uname=request.form['uname']
        psw=request.form['psw']
    
        
        a="select * from login where username='%s' and password='%s'"%(uname,psw)
        res=select(a)
        
        if res:
        
            session['log']=res[0]['login_id']
            
            if res[0]['usertype']=='admin':
                return redirect(url_for("admin.adminhome"))
            
            elif res[0]['usertype']=='user':
                d="select * from user where login_id='%s'"%(session['log'])
                re=select(d)
                session['uid']=re[0]['user_id']
                
                return redirect(url_for("user.userhome"))
            
            
            else:
                return '''<script>alert("Invalid User");window.location="/login"</script>'''
        else:
                return '''<script>alert("Invalid User");window.location="/login"</script>'''
            
            
                
        
    return render_template("login.html")



@public.route("/user_reg",methods=['post','get'])
def user_reg():
    if 'submit' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place=request.form['place']
        phone=request.form['phone']
        email=request.form['email']
        uname=request.form['uname']
        psw=request.form['psw']
        
        
        z="insert into login values(null,'%s','%s','user')"%(uname,psw)
        id=insert(z)
        
        z="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email)
        reg=insert(z)
        
        pid=str(reg)
        isFile = os.path.isdir("static/trainimages/"+pid)  
        print(isFile)
        if(isFile==False):
            os.mkdir('static\\trainimages\\'+pid)
        image1=request.files['img1']
        path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image1.filename
        image1.save(path)

        image2=request.files['img2']
        path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image2.filename
        image2.save(path)

        image3=request.files['img3']
        path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image3.filename
        image3.save(path)
        enf("static/trainimages/")
       
        flash('Added successfully...')
        return '''<script>alert("Registered Successfully");window.location="/login"</script>'''
   
    return render_template("user_reg.html")
