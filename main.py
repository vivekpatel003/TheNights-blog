#importing files for necessary work
from flask import Flask, render_template,request,session,redirect
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_mail import Mail
from flask_sendgrid import SendGrid
from datetime import datetime
import math


#initialize app
app = Flask(__name__)


#secret key for session
app.secret_key = 'super secret key'


# open json file and get the key-value
with open('config.json','r') as c:
     params = json.load(c)["params"]



#mail configuration
app.config['SENDGRID_API_KEY'] = '12940783'
app.config['SENDGRID_DEFAULT_FROM'] = 'admin@yourdomain.com'
mail = SendGrid(app)


# connection to database
local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
     app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri'] 
db = SQLAlchemy(app)



# set parameters / create table contacts
class Contacts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50),nullable=False)
    Email = db.Column(db.String(25),nullable=False)
    Phone = db.Column(db.String(13), unique=True,nullable=False)
    mes = db.Column(db.String(100),nullable=False)

class Posts(db.Model):
    serialNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    slug = db.Column(db.String(25),nullable=False)
    content = db.Column(db.String(13), unique=False,nullable=False)
    img_url = db.Column(db.String(25),nullable=False)
    subtitle = db.Column(db.String(50),nullable=False)
    date = db.Column(db.String(100),nullable=True)

# class Credential():
#      Sr_no = db.Column(db.Integer , primary_key=True)
#      email = db.Column(db.String(25) , nullable=False)
#      UserName = db.Column(db.String(10) , nullable=False)
#      Password = db.Column(db.String(15) , nullable=False)
#      flag = db.Column(db.Integer , nullable=False)
#      block = db.Column(db.Integer , nullable=False)
     
     
     





# Routs / API calls

# Index file route
@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    if('user' in session and session['user']==params['admin_name']):
        return render_template('index.html', param=params, posts=posts, prev=prev, next=next,login=1)
    return render_template('index.html', param=params, posts=posts, prev=prev, next=next,login=0)


# Dashboard / admin route
@app.route("/dashboard" , methods =['GET','POST'])
def login():
    #check whther user already logged in 
    if('user' in session and session['user']==params['admin_name']):
        post=Posts.query.all()
        return render_template('dashboard.html',param=params,post=post,login=1)
    #authentication
    if(request.method=='POST'):
        username=request.form.get('user_name')
        password=request.form.get('password')
        if(username == params['admin_name'] and password== params['admin_password']):
            session['user'] = username
            post = Posts.query.all()
            return render_template('dashboard.html',param=params,post=post,login=1) 
        else:
             return render_template('login.html',param=params,msg = "wrong credentials")
    else:
             return render_template('login.html',param=params)

@app.route("/logout")
def logout():
      if('user' in session and session['user']==params['admin_name']):
            session.pop('user', None)
            return render_template('login.html',param=params) 
      return render_template('login.html',param=params)

          

#add new post 
@app.route("/add/<string:serial_no>",methods=['GET','POST'])
def add(serial_no):
     #from Post table / class query is filtered by condition given if multiple select first
     if('user' in session and session['user']==params['admin_name']):
            if(request.method=='POST'):
                title = request.form.get('title')
                slug=request.form.get('slug')
                content = request.form.get('content')
                img_url = request.form.get('img_url')
                subtitle = request.form.get('subtitle')
                entry = Posts(title = title,slug=slug,content=content,img_url = img_url,subtitle=subtitle,date = datetime.now())
                db.session.add(entry)
                db.session.commit()
     return render_template('add.html',param = params,sr=serial_no,login=1)



#edit existing post
@app.route("/edit/<string:sr_no>",methods=['GET','POST'])
def edit(sr_no):
     #from Post table / class query is filtered by condition given if multiple select first
     if('user' in session and session['user']==params['admin_name']):
            post = Posts.query.filter_by(serialNo =sr_no).first()
            if(request.method=="POST"):
                title = request.form.get('title')
                slug=request.form.get('slug')
                content = request.form.get('content')
                img_url = request.form.get('img_url')
                subtitle = request.form.get('subtitle')

                post.title = title
                post.slug=slug
                post.content=content
                post.img_url=img_url
                post.subtitle=subtitle
                post.date = datetime.now()
                db.session.commit()
                return redirect('/edit/'+sr_no)
     return render_template('edit.html',param = params,post= post,sr=sr_no,login=1)



#delete existing post
@app.route("/delete/<string:sr_no>")
def delete(sr_no):
     if('user' in session and session['user']==params['admin_name']):
          post = Posts.query.filter_by(serialNo=sr_no).first()
          db.session.delete(post)
          db.session.commit()
          return redirect('/dashboard',login=1)



#show post explicitily
@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
     #from Post table / class query is filtered by condition given if multiple select first
     post = Posts.query.filter_by(slug = post_slug).first()
     if('user' in session and session['user']==params['admin_name']):
         return render_template('post.html',param = params,post=post,login=1)
     return render_template('post.html',param = params,post=post,login=0)


#about route
@app.route("/about")
def about():
     if('user' in session and session['user']==params['admin_name']):
        return render_template('about.html',param=params,login=1)
     return render_template('about.html',param=params,login=0)


# fill contact table
@app.route("/contact", methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
            name = request.form.get('Name')
            email = request.form.get('Email')
            phone = request.form.get('Phone')
            message = request.form.get('message')
            entry = Contacts(Name = name,Email = email, Phone = phone , mes= message)
            db.session.add(entry)
            db.session.commit() 
        # mail send to host by guest
            mail.send_email(
            from_email=email,
            to_email=params['gmail_user'],
            subject='Mail',
            text=message,
            )  
    if('user' in session and session['user']==params['admin_name']):
         return render_template('contact.html',param=params,login=1)
    return render_template('contact.html',param=params,login=0)


# run automatically changes would be saved
app.run(debug=True)





# dump code
# @app.route("/register",methods=['GET','POST'])
# def register():
#      if(request.method=='POST'):
#           email = request.form.get('user_email')
#           user_name = request.form.get('user_name')
#           password = request.form.get('user_password')
#           flag = 1
#           block= 0
#           cred = Credential.query.filter_by(UserName=user_name).first()
#           if(cred.flag==0):
#             reg = Credential(email=email,UserName=user_name,Password=password,flag=flag,block=block)
#             db.session.add(reg)
#             db.session.commit()
#           else:
#                return redirect('/dashboard')