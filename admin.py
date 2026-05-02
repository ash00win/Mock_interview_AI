from flask import *

from database import *

admin=Blueprint('admin',__name__)


@admin.route("/adminhome",methods=['post','get'])
def adminhome():
   
    return render_template("admin.html")


@admin.route("/manage_roles",methods=['post','get'])
def manage_roles():
    
    z="select * from roles"
    r=select(z)
    
    if 'submit' in request.form:
        role=request.form['role']
        
        a="insert into roles values(null,'%s')"%(role)
        insert(a)
        return '''<script>alert('Added Successfully');window.location='/manage_roles'</script>'''
   
    return render_template("manage_roles.html",r=r)



@admin.route("/adm_view_user",methods=['post','get'])
def adm_view_user():
    
    z="select * from user"
    r=select(z)
    
    
    return render_template("adm_view_user.html",r=r)



@admin.route("/adm_view_complaint",methods=['post','get'])
def adm_view_complaint():
    
    z="select * from complaint"
    r=select(z)
    
    
    return render_template("adm_view_complaint.html",r=r)



@admin.route("/reply",methods=['post','get'])
def reply():
    
    id=request.args['id']
    if 'submit' in request.form:
        reply=request.form['reply']
        
        a="update complaint set reply ='%s' where complaint_id='%s'"%(reply,id)
        update(a)
        return '''<script>alert('Updated Successfully');window.location='/adm_view_complaint'</script>'''
   
    return render_template("reply.html")




@admin.route("/send_notification",methods=['post','get'])
def send_notification():
    
    z="select * from notification"
    r=select(z)
    
    if 'submit' in request.form:
        title=request.form['title']
        noti=request.form['not']
        
        
        a="insert into notification values(null,'%s','%s',now())"%(title,noti)
        insert(a)
        return '''<script>alert('Added Successfully');window.location='/send_notification'</script>'''
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    
    else:
        action=None
    
    if action=='delete':
        s="delete from notification where notification_id='%s'"%(id)
        delete(s)
        return '''<script>alert('Deleted Successfully');window.location='/send_notification'</script>'''
        
   
    return render_template("send_notification.html",r=r)


