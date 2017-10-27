from flask import Flask, url_for, redirect, render_template, jsonify
import boto3
import base64
from boto3.dynamodb.conditions import Key, Attr
from flask import session as login_session
from . import profile
from datetime import datetime
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wecslabsuser')
table_activity_stats =dynamodb.Table('activity_stats')
s3 = boto3.resource('s3')

@profile.route('/profile/<titan_id>')
def profile_page(titan_id):
	current_date = datetime.now().strftime('%m/%d/%Y')
	response = table_activity_stats.get_item(
		Key = {
		'date': current_date
	})

	response_all = table_activity_stats.get_item(
		Key = {
		'date': 'all'
	})

	if titan_id == login_session['titan_id']:
		try:
			cdt= 100 * int(response['Item']['comp_tot_tasks'])/int(response['Item']['tot_tasks'])
			ctt= 100 * int(response_all['Item']['comp_tot_tasks'])/int(response_all['Item']['tot_tasks'])
			form= 100 * int(response['Item']['comp_tot_tasks'])/int(login_session['max_tasks'])
		except:
			cdt = 100
			try:
				ctt= 100 * int(response_all['Item']['comp_tot_tasks'])/int(response_all['Item']['tot_tasks'])
			except:
				ctt = 100
			form = 100
		pro_pic="https://s3.us-east-2.amazonaws.com/wecslabspropic/dp" + titan_id + ".jpg"

		length = len(login_session['awards'])

		award_1 = "/static/img/awards/" + login_session['awards'][length-1] + ".png"
		award_2 = "/static/img/awards/" + login_session['awards'][length-2] + ".png"
		award_3 = "/static/img/awards/" + login_session['awards'][length-3] + ".png"

		award_tag_1 = login_session['award_tag'][length-1]
		award_tag_2 = login_session['award_tag'][length-2]
		award_tag_3 = login_session['award_tag'][length-3]

		print(award_1, award_2, award_3)

		if login_session['username'] == 'John Paul':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/john-medium.png'
		if login_session['username'] == 'Abin Mittu':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/abin-medium.png'
		if login_session['username'] == 'Steve Paul':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/steve-medium.png'
		if login_session['username'] == 'Thomas George':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/thomas-medium.png'
		if login_session['username'] == 'Jobin Geo':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/jobin-medium.png'
		if login_session['username'] == 'Eldose':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/sunny-medium.png'
		if login_session['username'] == 'Philipose Kuriakose':
			cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/philipose-medium.png'

		return render_template('profile/profile.html',  titan_id=login_session['titan_id'],
															username=login_session['username'],
															pro_pic=pro_pic,
															location=login_session['user_location'],
															position=login_session['position'],
															current_project=login_session['current_project'],
															motivation=login_session['motivation'],
															fb_link=login_session['fb_link'],
															insta_link=login_session['insta_link'],
															linkedin_link=login_session['linkedin_link'],
															email=login_session['email'],
															phone=login_session['phone'],
															cartoon_image=cartoon_image,
															ideas=login_session['ideas'],
															projects=len(login_session['projects']),
															work_days=login_session['work_days'],
															work_streak=login_session['work_streak'],
															tasks=login_session['comp_tot_tasks'],
															awards=len(login_session['awards']) - 2,
															day_perc=cdt,
															tot_perc=ctt,
															form=form,
															award_1=award_1,
															award_2=award_2,
															award_3=award_3,
															award_tag_1 = award_tag_1,
															award_tag_2 = award_tag_2,
															award_tag_3 = award_tag_3)
	else:
		try:
			response=table.get_item(
				Key={
					'titan_id': titan_id
				})
			user=response['Item']
			cdt=int(100*user['comp_day_tasks']/user['tot_day_tasks'])
			ctt=int(100*user['comp_tot_tasks']/user['tot_tot_tasks'])
			form=int(100*user['comp_day_tasks']/user['max_tasks'])
			pro_pic="https://s3.us-east-2.amazonaws.com/wecslabspropic/dp" + titan_id + ".jpg"

			length = len(user['awards'])

			award_1 = "/static/img/awards/" + user['awards'][length-1] + ".png"
			award_2 = "/static/img/awards/" + user['awards'][length-2] + ".png"
			award_3 = "/static/img/awards/" + user['awards'][length-3] + ".png"

			award_tag_1 = user['award_tag'][length-1]
			award_tag_2 = user['award_tag'][length-2]
			award_tag_3 = user['award_tag'][length-3]

			if user['username'] == 'John Paul':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/john-medium.png'

			if user['username'] == 'Abin Mittu':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/abin-medium.png'

			if user['username'] == 'Steve Paul':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/steve-medium.png'
			if user['username'] == 'Thomas George':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/thomas-medium.png'
			if user['username'] == 'Jobin Geo':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/jobin-medium.png'
			if user['username'] == 'Eldose':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/sunny-medium.png'
			if user['username'] == 'Philipose Kuriakose':
				cartoon_image='https://s3.us-east-2.amazonaws.com/wecslabspropic/philipose-medium.png'

			return render_template('profile/profile_others.html',  titan_id=user['titan_id'],
																username=user['username'],
																pro_pic=pro_pic,
																location=user['user_location'],
																position=user['user_position'],
																current_project=user['current_project'],
																motivation=user['motivation'],
																fb_link=user['fb_link'],
																insta_link=user['insta_link'],
																linkedin_link=user['linkedin_link'],
																email=user['email'],
																phone=user['phone'],
																cartoon_image= cartoon_image,
																ideas=user['ideas'],
																projects=len(user['projects']),
																work_days=user['work_days'],
																work_streak=user['work_streak'],
																tasks=user['tasks'],
																awards=len(user['awards']),
																day_perc=cdt,
																tot_perc=ctt,
																form=form,
																award_1=award_1,
																award_2=award_2,
																award_3=award_3,
																award_tag_1 = award_tag_1,
																award_tag_2 = award_tag_2,
																award_tag_3 = award_tag_3)
		except:
			return "User not found"

@profile.route('/profile/display_award')
def display_award():
	return jsonify(login_session['display'])

@profile.route('/profile/reset_display', methods = ['POST'])
def reset_display():
	login_session['display'] = []
	return 'Success'
