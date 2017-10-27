from flask import Flask, render_template, redirect, url_for, request, jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import session as login_session
from datetime import datetime
from . import project
import json
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('project')
tableusers = dynamodb.Table('wecslabsuser')

@project.route('/project_central')
def project_central():
	return render_template('project/projectmain.html')

@project.route('/create_project')
def create_project():
	try:
		message = login_session['project_message']
	except:
		message = ''
	return render_template('project/create_project.html', message = message)

@project.route('/create_project/submit', methods=['POST'])
def register():
	project_name = request.form['project_name']
	from_date = request.form['from']
	to_date = request.form['to']

	if project_name == '':
		login_session['project_message'] = "Enter a Project name"
		return redirect(url_for('project.create_project'))
	try:
		from_date = datetime.strptime(from_date, '%m/%d/%Y')
		to_date = datetime.strptime(to_date, '%m/%d/%Y')
		current_date = datetime.now().strftime('%m/%d/%Y')
		current_date = datetime.strptime(current_date, '%m/%d/%Y')
	except:
		login_session['project_message'] = "Either from or to date is missing"
		return redirect(url_for('project.create_project'))
	if current_date>from_date:
		login_session['project_message'] = "Project start date is in the past"
		return redirect(url_for('project.create_project'))
	if from_date>to_date:
		login_session['project_message'] = "Project end date before start date"
		return redirect(url_for('project.create_project'))

	response= table.get_item(
		Key={ 
			'project_name': project_name
		})
	try:
		print(response['Item'])
		login_session['project_message'] = "Project already exist"
		return redirect(url_for('project.create_project'))
	except:
		table.put_item(Item = {
		'project_name': project_name,
		'from_date': str(from_date),
		'to_date': str(to_date),
		'added_by':{"username": login_session['username'], 'titan_id': login_session['titan_id']},
		'usersname': {}
	})

	return redirect(url_for('project.add_project_mem', project_name=project_name))

@project.route('/project/delete', methods=['POST'])
def delete():
	try:
		del login_session['project_message']
	except:
		pass
	return 'deleted'

@project.route('/create_project/add_project_mem/<project_name>')
def add_project_mem(project_name):
	return render_template('project/add_project_mem.html', project_name=project_name)

@project.route('/create_project/add_project_mem/fetch_users')
def fetch_users():
	response = tableusers.scan()
	x = []
	items = response['Items']
	for i in range(len(items)):
		dict = {
		'titan_id':'https://s3.us-east-2.amazonaws.com/wecslabspropic/dp'+items[i]['titan_id']+'.jpg',
		'name': items[i]['username'],
		'position':'Add a role'
		}
		x.append(dict)
	return jsonify(x)

@project.route('/create_project/add_project_mem/submit', methods=['POST'])
def submit_members():
	data = json.loads(request.form['info'])
	project_name = request.form['project_name']

	for item in data:
		titan_id = item['titan_id'].split('propic/dp')[1].split('.jpg')[0]
		position = item['position']

		response = tableusers.get_item(
		Key = {
		'titan_id': titan_id
		})

		project_array = response['Item']['projects']
		project_array.append(project_name)

		if titan_id == login_session['titan_id']:
			login_session['position'] = position
			login_session['current_project'] = project_name
			login_session["projects"] = project_array

		response = tableusers.update_item(
		Key = {
		'titan_id': titan_id
		},
		UpdateExpression = 'set user_position = :user_position, current_project = :current_project, projects = :project_array',
		ExpressionAttributeValues = {
			':user_position': position,
			':current_project': project_name,
			':project_array': project_array
		},
		ReturnValues = 'ALL_NEW'
		)

		result = tableusers.update_item(
		Key = {
			'titan_id': titan_id
		},
		UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
		ExpressionAttributeNames = {
  			"#attrName" : "awards",
  			"#attrName1" : "award_tag"
		},
		ExpressionAttributeValues = {
 			":attrValue" : ['C'],
 			":attrValue1" : ['Joined a Project']
		})

		if titan_id == login_session['titan_id']:
			login_session['awards'].append('C')
			login_session['award_tag'].append('Joined a project')
			login_session['display'].append({'id': 1,'award': '/static/img/awards/C.png', 'desc': 'Joined a Project'})


	return "Success"
