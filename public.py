from flask import *
from database import *
import uuid

public=Blueprint('public',__name__)

@public.route('/')
def home():
	data={}
	return render_template('home.html',data=data)

@public.route('/login',methods=['get','post'])
def login():
	
	if 'signup' in request.form:
		return redirect(url_for('public.user_register'))

	if 'submit' in request.form:
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(uname,pwd)
		res=select(q)
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=='admin':
				flash("login successfully....!")
				return redirect(url_for('admin.admin_home'))
			elif res[0]['usertype']=='user':
				q="select * from user where login_id='%s'"%(session['lid'])
				res=select(q)
				print(res)
				if res:
					session['uid']=res[0]['user_id']
					flash("login successfully....!")
					return redirect(url_for('user.user_home'))
		else:
			flash("INVALID USERNAME OR PASSWORD")
	return render_template('login.html')


@public.route('/user_register',methods=['get','post'])
def user_register():
	if 'submit' in request.form:
		fn=request.form['fn']
		ln=request.form['ln']
		un=request.form['un']
		place=request.form['pl']
		phone=request.form['ph']
		email=request.form['em']
		pwd=request.form['pwd']
		dob=request.form['dob']
		q="select * from login where username='%s' and password='%s'" %(un,pwd)
		res=select(q)
		if res:
			flash("USERNAME AND PASSWORD IS ALREADY EXIST")
		else:
			q="INSERT INTO `login` VALUES(null,'%s','%s','user')"%(un,pwd)
			lid=insert(q)
			q1="INSERT INTO `user` VALUES(null,'%s','%s','%s','%s','%s','%s','%s')"%(lid,fn,ln,place,phone,email,dob)
			insert(q1)
			flash('registered')
		return redirect(url_for('public.user_register'))
	return render_template("user_register.html")