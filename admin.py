from public import *


admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	return render_template('admin_home.html')


@admin.route('/admin_view_complaint_reply',methods=['get','post'])
def admin_view_complaint_reply():
	data={}
	q="SELECT *,CONCAT(`fname`,' ',`lname`) AS `name` FROM `complaint` INNER JOIN `user` using(user_id)"
	res=select(q)
	data['complaints']=res

	j=0
	for i in range(1,len(res)+1):
		print('submit'+str(i))
		if 'submit'+str(i) in request.form:
			reply=request.form['reply'+str(i)]
			print(reply)
			print(j)
			print(res[j]['complaint_id'])
			q="update complaint set reply='%s' where complaint_id='%s'" %(reply,res[j]['complaint_id'])
			print(q)
			update(q)
			flash("success")
			return redirect(url_for('admin.admin_view_complaint_reply')) 	
		j=j+1
	return render_template("admin_view_complaint_reply.html",data=data)



@admin.route('/admin_view_user')
def admin_view_user():
	data={}
	q="select * from user"
	res=select(q)
	if res:
		data['user']=res
		print(res)
	return render_template('admin_view_user.html',data=data)