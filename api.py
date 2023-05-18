from flask import *
from database import *

import demjson
import uuid
# from predict import *


api=Blueprint('api',__name__)


@api.route('/login',methods=['get','post'])
def login():
	data={}
	
	username = request.args['username']
	password = request.args['password']
	q="SELECT * from login inner join user using(login_id) where username='%s' and password='%s'" % (username,password)
	
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='login'
	return  demjson.encode(data)
@api.route('/regi',methods=['get','post'])
def regi():
	data={}
	fname=request.args['fname']
	lname=request.args['lname']
	email=request.args['email']
	place=request.args['place']
	phone=request.args['phone']
	age=request.args['age']
	emnum=request.args['emnum']
	username = request.args['username']
	password = request.args['password']
	q1="SELECT * FROM login where username='%s'"%(username)
	print(q1)
	res=select(q1)
	print(res)
	if res:
		data['status'] = 'duplicate'
		data['method'] = 'regi'
	else:
		q="INSERT INTO `login` VALUES(NULL,'%s','%s','user')"%(username,password)
		lid=insert(q)
		qr="INSERT INTO `user` values(null,'%s','%s','%s','%s','%s','%s','%s','%s')" %(lid,fname,lname,place,phone,email,age,emnum)
		id=insert(qr)
		if id>0:
			data['status'] ='success'
		else:

			data['status'] ='failed'
		data['method'] ='regi'
	return demjson.encode(data)
@api.route('/viewusers',methods=['get','post'])
def viewusers():
	data={}
	loginid=request.args['lid']
	q="SELECT *,CONCAT (fname,' ',lname) AS names FROM user WHERE login_id != '%s' AND user_id NOT IN (SELECT IF(user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),friend_id,user_id) FROM friends WHERE (friend_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') AND STATUS='Accept') OR (friend_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') AND STATUS='pending') OR (user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')  AND STATUS='Accept') OR (user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')  AND STATUS='pending'))" %(loginid,loginid,loginid,loginid,loginid,loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='viewusers'
	return  demjson.encode(data)
@api.route('/viewuserss',methods=['get','post'])
def viewuserss():
	data={}
	loginid=request.args['lid']
	search="%"+request.args['search']+"%"
	q="select *,concat (fname,' ',lname) as names from user where (fname like '%s' and  login_id != '%s') or (lname like '%s' and  login_id != '%s')" %(search,loginid,search,loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='viewusers'
	return  demjson.encode(data)
@api.route('/view_request',methods=['get','post'])
def view_request():
	data={}
	loginid=request.args['loginid']
	q="SELECT * FROM `user` INNER JOIN `friends` USING(user_id) where friend_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')" %(loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='view_request'
	return  demjson.encode(data)


@api.route('/user_send_request',methods=['get','post'])
def user_send_request():
	data={}
	loginid=request.args['loginid']
	friend_id=request.args['friend_id']
	q="SELECT * FROM `friends` WHERE `friend_id`='%s' AND `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(friend_id,loginid)
	print(q)
	res=select(q)
	if res:
		data['status']='duplicate'
		data['method'] ='user_send_request'
	else:
		q="INSERT INTO `friends` VALUES(NULL,'%s',(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),NOW(),'pending')"%(friend_id,loginid)
		print(q)
		id=insert(q)
		if id>0:
			data['status'] ='success'
		else:
			data['status'] ='failed'
		data['method'] ='user_send_request'
		return  demjson.encode(data)
	
@api.route('/request_accept',methods=['get','post'])
def request_accept():
	data={}
	frnd_id=request.args['frnd_id']
	q="UPDATE `friends` SET `status`='Accept' WHERE `friends_id`='%s'"%(frnd_id)
	print(q)
	id=update(q)
	if id>0:
		data['status'] ='success'
	else:
		data['status'] ='failed'
	data['method'] ='request_accept'
	return  demjson.encode(data)
@api.route('/reject_request',methods=['get','post'])
def reject_request():
	data={}
	frnd_id=request.args['frnd_id']
	q="DELETE FROM `friends` WHERE `friends_id`='%s'"%(frnd_id)
	print(q)
	id=update(q)
	if id>0:
		data['status'] ='success'
	else:
		data['status'] ='failed'
	data['method'] ='reject_request'
	return  demjson.encode(data)
@api.route('/view_friends',methods=['get','post'])
def view_friends():
	data={}
	loginid=request.args['loginid']
	# friend_id=request.args['friend_id']
	q="SELECT * FROM `user` WHERE user_id IN(SELECT IF(user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),friend_id,user_id) FROM friends WHERE (friend_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') AND STATUS='Accept') OR (user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')  AND STATUS='Accept'))" %(loginid,loginid,loginid)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='view_friends'
	return  demjson.encode(data)


@api.route('/user_upload_file',methods=['get','post'])
def user_upload_file():
	data={}
	loginid=request.form['logid']
	images=request.files['image']
	title=request.form['title']
	lati=request.form['lati']
	longi=request.form['longi']

	# cmm = predictfn(title)
	# print(cmm)

	# # ______sentence_analysis______
	# cmd.execute("select * from bullying")
	# s = cmd.fetchall()
	# bull = ""
	# for i in s:
	# 	bull = bull + " " + str(i[2])
	# print(bull)

	# documents = [title, bull]
	# tfidf = TfidfVectorizer().fit_transform(documents)
	# # no need to normalize, since Vectorizer will return normalized tf-idf
	# pairwise_similarity = tfidf * tfidf.T

	# marks = str(pairwise_similarity).split('\n')
	# per = 0.0
	# print(pairwise_similarity)
	# if (len(marks) >= 4):
	# 	print('iffffff')
	# 	pp = marks[0].split('\t')[1]
	# 	per = float(pp)
	# 	print("per", per)
	# if ((per != 0) or (cmm == 'Negative')):
	# 	print("bully", cmm)
	# 	data['status'] ='B'


	# else:
	path = "static/uploads/" + str(uuid.uuid4()) + images.filename
	images.save(path)

		# from newcnn import predictcnn
	rs=""

	q="INSERT INTO `post` VALUES(null,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s','%s',NOW(),'pending')"%(loginid,title,path)
	print(q)
	id=insert(q)
	data['status'] ='success'

	data['status'] ='B'

	data['method'] ='user_upload_file'
	return  demjson.encode(data)

@api.route('/my_post',methods=['get','post'])
def my_post():
	data={}
	loginid=request.args['loginid']
	q="SELECT * ,post as caption FROM `post` WHERE user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')" %(loginid)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='my_post'
	return  demjson.encode(data)
@api.route('/others_post',methods=['get','post'])
def others_post():
	data={}
	# lid=request.args['lid']
	frnd_id=request.args['frnd_id']
	# q="SELECT * FROM `post` WHERE `user_id`!=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(frnd_id)
	q="SELECT * FROM `post` WHERE `user_id`='%s'"%(frnd_id)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='others_post'
	return  demjson.encode(data)


@api.route('/User_view_all_post',methods=['get','post'])
def User_view_all_post():
	data={}
	# lid=request.args['lid']
	# frnd_id=request.args['frnd_id']
	# q="SELECT * FROM `post` WHERE `user_id`!=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(frnd_id)
	q="SELECT * FROM `post` "
	res=select(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='User_view_all_post'
	return  demjson.encode(data)


@api.route('/report_post',methods=['get','post'])
def report_post():
	data={}
	imageid=request.args['image_id']
	loginid=request.args['loginid']
	q="INSERT INTO `reportings` VALUES(null,'%s',(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'pending',NOW())"%(imageid,loginid)
	print(q)
	res=insert(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='report_post'
	return  demjson.encode(data)
@api.route('/Comment',methods=['get','post'])
def Comment():
	data={}
	image_id=request.args['image_id']
	q="select * from comments where image_id='%s'"%(image_id)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='Comment'
	return  demjson.encode(data)
@api.route('/user_comment_post',methods=['get','post'])
def user_comment_post():
	data={}
	comment=request.args['comment']

	loginid=request.args['loginid']
	image_id=request.args['image_id']
	# cmm = predictfn(comment)
	# print(cmm)

	# # ______sentence_analysis______
	# cmd.execute("select * from bullying")
	# s = cmd.fetchall()
	# bull = ""
	# for i in s:
	# 	bull = bull + " " + str(i[2])
	# print(bull)

	# documents = [comment, bull]
	# tfidf = TfidfVectorizer().fit_transform(documents)
	# # no need to normalize, since Vectorizer will return normalized tf-idf
	# pairwise_similarity = tfidf * tfidf.T

	# marks = str(pairwise_similarity).split('\n')
	# per = 0.0
	# print(pairwise_similarity)
	# if (len(marks) >= 4):
	# 	print('iffffff')
	# 	pp = marks[0].split('\t')[1]
	# 	per = float(pp)
	# 	print("per", per)
	# if ((per != 0) or (cmm == 'Negative')):
	# 	print("bully", cmm)
	# 	data['status'] ='B'
	# import transformers
	import torch

	# # Load the pre-trained BERT model
	# tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
	# model = transformers.BertForSequenceClassification.from_pretrained('bert-base-uncased')

	# # Define the text to classify
	# text = "You're such a loser, no one likes you."

	# # Encode the text using the BERT tokenizer
	# encoded_text = tokenizer.encode_plus(
	#     text,                      # Text to encode
	#     add_special_tokens=True,   # Add '[CLS]' and '[SEP]'
	#     max_length=512,           # Pad/truncate all sentences
	#     pad_to_max_length=True,   # Pad to the max length
	#     return_attention_mask=True,  # Return attention mask
	#     return_tensors='pt',      # Return PyTorch tensors
	# )

	# # Make predictions on the encoded text
	# with torch.no_grad():
	# 	outputs = model(
	# 		input_ids=encoded_text['input_ids'],
	# 		attention_mask=encoded_text['attention_mask']
	# 	)

	# Extract the predicted labels
	# predicted_label = torch.argmax(outputs[0]).item()
	predicted_label = 0
	q="INSERT INTO `comments` VALUES(null,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s','%s',NOW(),'pending')"%(loginid,image_id,comment)
	print(q)
	res=insert(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:

		data['status']	= 'failed'
	data['method'] ='user_comment_post'
	return  demjson.encode(data)


# /////////////////////////////////////////

# @api.route('/usercheckimage',methods=['get','post'])
# def usercheckimage():
# 	data={}
# 	images=request.files['image']
	
# 	path="test_data/test.jpg"
# 	images.save(path)
# 	# q="INSERT INTO `comments` VALUES(null,(SELECT `user_id` FROM `users` WHERE `login_id`='%s'),'%s','%s',NOW(),'pending')"%(loginid,image_id,comment)
# 	# print(q)
# 	# res=insert(q)
# 	# print(res)
# 	s=gen_text(path)
# 	# vals=vals.remove('startseq','')
# 	vals=s[0]
# 	nval=vals.split("startseq")
# 	nval1=nval[1].split("endseq")
# 	print(vals)

# 	data['status']='success'
# 	data['data'] = nval1[0]
	
# 	data['method'] ='usercheckimage'
# 	return  demjson.encode(data)







@api.route('/upload_audio',methods=['get','post'])
def upload_audio():
	data={}
	title=request.form['title']
	file=request.files['audio']
	print("FFFFFFFFFFFF : ",file)
	logid=request.form['logid']
	print("************************************************")

	# cmm = predictfn(title)
	# print(cmm)

	# # ______sentence_analysis______
	# cmd.execute("select * from bullying")
	# s = cmd.fetchall()
	# bull = ""
	# for i in s:
	# 	bull = bull + " " + str(i[2])
	# print(bull)

	# documents = [title, bull]
	# tfidf = TfidfVectorizer().fit_transform(documents)
	# # no need to normalize, since Vectorizer will return normalized tf-idf
	# pairwise_similarity = tfidf * tfidf.T

	# marks = str(pairwise_similarity).split('\n')
	# per = 0.0
	# print(pairwise_similarity)
	# if (len(marks) >= 4):
	# 	print('iffffff')
	# 	pp = marks[0].split('\t')[1]
	# 	per = float(pp)
	# 	print("per", per)
	# if ((per != 0) or (cmm == 'Negative')):
	# 	print("bully", cmm)
	# 	data['status'] ='B'
	# else:
		

	# 	import speech_recognition as sr

	# 	# initialize the recognizer
	# 	r = sr.Recognizer()

	path = "static/uploads/" + str(uuid.uuid4()) + file.filename
	print(path)
	file.save(path)

	# 	# open the audio file
	# 	# with sr.AudioFile("audio_file.wav") as source:
	# 	print("______________--",path)
	# 	with sr.AudioFile(path) as source:
	# 		print("............... : ",path)
	# 		audio_data = r.record(source)  # read the entire audio file

	# 	# recognize speech using Google Speech Recognition
	# 	text = r.recognize_google(audio_data)

	# 	# print the transcribed text
	# 	print(text)

	# 	cmm = predictfn(text)
	# 	print(cmm)
	# 	# ______sentence_analysis______
	# cmd.execute("select * from bullying")
	# s = cmd.fetchall()
	# 	bull = ""
	# 	for i in s:
	# 		bull = bull + " " + str(i[2])
	# 	print(bull)

	# 	documents = [text, bull]
	# 	tfidf = TfidfVectorizer().fit_transform(documents)
	# 	# no need to normalize, since Vectorizer will return normalized tf-idf
	# 	pairwise_similarity = tfidf * tfidf.T

	# 	marks = str(pairwise_similarity).split('\n')
	# 	per = 0.0
	# 	print(pairwise_similarity)
	# 	if (len(marks) >= 4):
	# 		print('iffffff')
	# 		pp = marks[0].split('\t')[1]
	# 		per = float(pp)
	# 		print("per", per)
	# 	if ((per != 0) or (cmm == 'Negative')):
	# 		print("bully", cmm)
	# 		data['status'] ='B'
	# 	else:\
	# 		post=title+" - "+text
	post=""
	q="INSERT INTO `post` VALUES(null,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s','%s',NOW(),'pending')"%(logid,post,path)
	print(q)
	id=insert(q)
	data['status'] ='success'

	data['status'] ='success'


	data['method'] ='upload_audio'
	return  demjson.encode(data)
