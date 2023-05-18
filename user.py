from public import *


user=Blueprint('user',__name__)

@user.route('/user_home')
def user_home():
	return render_template('user_home.html')


@user.route('/user_send_complaint',methods=['get','post'])
def user_send_complaint():
	data={}
	uid=session['uid']
	if 'manage' in request.form:
		com=request.form['com']
		q="insert into complaint values(null,'%s','%s','pending',now())"%(uid,com)
		insert(q)
		flash("added successfully")
		return redirect(url_for('user.user_send_complaint'))

	q="select * from complaint where user_id='%s'"%(uid)
	res=select(q)
	data['com']=res
	return render_template('user_send_complaint.html',data=data)



@user.route('/user_manage_post',methods=['get','post'])
def user_manage_post():
	data={}
	uid=session['uid']
	if 'manage' in request.form:
		post=request.form['post']
		fl=request.files['fl']
		path='static/'+str(uuid.uuid4())+fl.filename
		fl.save(path)
		q="insert into post values(null,'%s','%s','%s',curdate(),'pending')"%(uid,post,path)
		insert(q)
		flash("added successfully")
		return redirect(url_for('user.user_manage_post'))

	q="select * from post where user_id='%s'"%(uid)
	res=select(q)
	data['post']=res
	return render_template('user_manage_post.html',data=data)




@user.route('/user_view_others_post',methods=['get','post'])
def user_view_others_post():
	data={}
	uid=session['uid']
	q="select * from post where user_id!='%s'"%(uid)
	res=select(q)
	data['post']=res
	return render_template('user_view_others_post.html',data=data)



@user.route('/user_add_comments',methods=['get','post'])
def user_add_comments():
	data={}
	uid=session['uid']
	pid=request.args['pid']
	if 'manage' in request.form:
		com=request.form['com']
		q="insert into comment values(null,'%s','%s')"%(pid,com)
		insert(q)
		flash("added successfully")
		return redirect(url_for('user.user_view_others_post'))	
	return render_template('user_add_comments.html',data=data)



@user.route('/user_view_comments',methods=['get','post'])
def user_view_comments():
	data={}
	pid=request.args['pid']
	uid=session['uid']
	q="select * from comment where post_id='%s'"%(pid)
	res=select(q)
	data['post']=res
	return render_template('user_view_comments.html',data=data)



@user.route('/user_send_frnd_request',methods=['get','post'])
def user_send_frnd_request():
	data={}
	uid=session['uid']
	q="select * from user where user_id!='%s'"%(uid)
	res=select(q)
	if res:
		data['user']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		fid=request.args['fid']
	else:
		action=None
	if action=="request":
		q="INSERT INTO `friends` VALUES(NULL,'%s','%s',now(),'pending') "%(fid,uid)
		insert(q)
		flash('requested successfully')
		return redirect(url_for('user.user_send_frnd_request'))
	return render_template('user_send_frnd_request.html',data=data)



@user.route('/user_view_frnd_request',methods=['get','post'])
def user_view_frnd_request():
	data={}
	uid=session['uid']
	q="SELECT * FROM USER INNER JOIN `friends` USING(user_id) where friends.user_id!='%s'"%(uid)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['user']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		fid=request.args['fid']
	else:
		action=None
	if action=="accept":
		q="update  `friends` set status='accept' where friend_id='%s' "%(fid)
		insert(q)
		flash('accepted successfully')
		return redirect(url_for('user.user_view_frnd_request'))
	if action=="reject":
		q="update  `friends` set status='reject' where friend_id='%s' "%(fid)
		insert(q)
		flash('rejected successfully')
		return redirect(url_for('user.user_view_frnd_request'))
	return render_template('user_view_frnd_request.html',data=data)