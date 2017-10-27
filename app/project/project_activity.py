from flask import Flask, render_template, redirect, url_for, request, jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import session as login_session
from datetime import datetime
import decimal
from . import project
import json
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('project_activities')
table_user = dynamodb.Table('wecslabsuser')
table_activity_stats = dynamodb.Table('activity_stats')
table_project = dynamodb.Table('project')

@project.route('/project_activities/<project_name>')
def project_activities(project_name):
	print(project_name)
	return render_template('project/project_activity.html', project_name=project_name)

@project.route('/project_activities/fetch_activities/<date>/<project_name>')
def fetch_activities(date, project_name):
	try:
		current_date = datetime.now().strftime('%m/%d/%Y')
		current_date = date[0:2]+'/'+date[2:4]+'/' +date[4:]
		print(current_date)

		project_name = project_name

		response = table.get_item (
			Key={
				'project_name': project_name,
				'date': current_date
			})
		item = json.loads(response['Item']['activities'])
		print(item)

		return json.dumps(item)

	except:
		return jsonify([])

@project.route('/project_activities/fetch_current_date')
def fetch_current_date():
	current_date = datetime.now().strftime('%m/%d/%Y')

	date = {'date': current_date}

	print(date)

	return jsonify(date)

@project.route('/project_activities/save_activities', methods=['POST'])
def save_activiies():
	info =  request.form['info']
	project_name =  request.form['project_name']
	date =  request.form['date']
	toggler_status = int(request.form['toggler_status'])
	activities_added = int(request.form['activities_added'])
	print(info,project_name,date)
	response = table.put_item(
		Item = {
		'project_name': project_name,
		'date': date,
		'activities': info
		}
	)
	response = table_user.update_item(
		Key = {
		'titan_id': login_session['titan_id']
		},
		UpdateExpression = 'set comp_day_tasks = comp_day_tasks + :val, comp_tot_tasks = comp_tot_tasks + :val',
		ExpressionAttributeValues = {
			':val': decimal.Decimal(toggler_status)
		},
		ReturnValues = 'ALL_NEW'
		)

	try:
		response = table_activity_stats.update_item(
			Key = {
			'date': date
			},
			UpdateExpression = 'set tot_tasks = tot_tasks + :tot_tasks, comp_tot_tasks = comp_tot_tasks + :comp_tot_tasks',
			ExpressionAttributeValues = {
				':tot_tasks': decimal.Decimal(activities_added),
				':comp_tot_tasks': decimal.Decimal(toggler_status)
			},
			ReturnValues = 'ALL_NEW'
			)
	except:
		response = table_activity_stats.put_item(
			Item = {
			'date': date,
			'tot_tasks': activities_added,
			'comp_tot_tasks': toggler_status
			}
		)

	try:
		response = table_activity_stats.update_item(
			Key = {
			'date': 'all'
			},
			UpdateExpression = 'set tot_tasks = tot_tasks + :tot_tasks, comp_tot_tasks = comp_tot_tasks + :comp_tot_tasks',
			ExpressionAttributeValues = {
				':tot_tasks': decimal.Decimal(activities_added),
				':comp_tot_tasks': decimal.Decimal(toggler_status)
			},
			ReturnValues = 'ALL_NEW'
			)
	except:
		response = table_activity_stats.put_item(
			Item = {
			'date': 'all',
			'tot_tasks': activities_added,
			'comp_tot_tasks': toggler_status
			}
		)

	return ("Success")

@project.route('/edit_project')
def edit_project():
	projects = []
	response = table_project.scan()
	items = response['Items']
	for item in items:
		projects.append(item['project_name'])
	return render_template('project/edit_project.html', projects = projects)

@project.route('/edit_project/delete', methods=['POST'])
def delete_project():
	project = request.form['project']
	table_project.delete_item(
	    Key={
	        'project_name': project
	    }
	)
	return "Success"