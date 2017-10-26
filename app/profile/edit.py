from flask import Flask, url_for, redirect, render_template, request
from flask import session as login_session
from . import profile
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wecslabsuser')

@profile.route('/edit')
def editprofile():
	return render_template('profile/edit.html', location=login_session['user_location'],
		motivation=login_session['motivation'],
		fb_link=login_session['fb_link'],
		insta_link=login_session['insta_link'],
		linkedin_link=login_session['linkedin_link'],
		email=login_session['email'],
		phone=login_session['phone'])


@profile.route('/editinfo', methods=['POST'])
def editinfo():
	login_session['user_location'] = request.form['address']
	login_session['motivation'] = request.form['self_motivate']
	login_session['fb_link'] = request.form['fb_link']
	login_session['insta_link'] = request.form['insta_link']
	login_session['linkedin_link'] = request.form['linkedin_link']
	login_session['email'] = request.form['email']
	login_session['phone'] = request.form['phone']

	response = table.update_item(
		Key = {
		'titan_id': login_session['titan_id']
		},
		UpdateExpression = 'set user_location = :address, motivation = :motivation, fb_link = :fb_link, insta_link = :insta_link, linkedin_link = :linkedin_link, email = :email, phone = :phone',
		ExpressionAttributeValues = {
			':address': login_session['user_location'],
			':motivation': login_session['motivation'],
			':fb_link': login_session['fb_link'],
			':insta_link': login_session['insta_link'],
			':linkedin_link': login_session['linkedin_link'],
			':email': login_session['email'],
			':phone': login_session['phone']
		},
		ReturnValues = 'ALL_NEW'
		)

	return redirect(url_for('profile.profile_redirect'))


