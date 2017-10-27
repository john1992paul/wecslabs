from flask import Flask, render_template, redirect, url_for, request, jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import session as login_session
from datetime import datetime
from . import teambase
import json
dynamodb = boto3.resource('dynamodb')
tableusers = dynamodb.Table('wecslabsuser')

@teambase.route('/teambase')
def teambase_display():
	response = tableusers.scan()
	users = []
	items = response['Items']
	for i in range(len(items)):
		dict = {
		'profile_pic':'https://s3.us-east-2.amazonaws.com/wecslabspropic/dp'+items[i]['titan_id']+'.jpg',
		'name': items[i]['username'],
		'titan_id': items[i]['titan_id']
		}
		users.append(dict)
	return render_template('teambase/teambase.html', users = users)