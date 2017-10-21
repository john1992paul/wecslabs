from flask import Flask, url_for, redirect
import hashlib
import io
import urllib
import uuid
from . import auth
import boto3
import base64
from boto3.dynamodb.conditions import Key, Attr
from flask_mail import Mail, Message
from flask import session as login_session
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wecslabsuser')
s3 = boto3.resource('s3')

#----------------------  Adds a user ----------------------------------------------------------------------------------------
def createUser(login_session):
    hash_object = hashlib.md5(login_session['email'].encode('utf-8'))
    titan_id = str(hash_object.hexdigest())
    login_session["titan_id"] = titan_id
    login_session["location"] = "City, Country"
    login_session["position"] = "Unassigned"
    login_session["current_project"] = "No Projects"
    login_session["motivation"] = "Hardwork beats Talent"
    login_session["fb_link"] = "http://www.facebook.com"
    login_session["insta_link"] = "http://www.instagram.com"
    login_session["linkedin_link"] = "http://www.linkedin.com"
    login_session["phone"] = "+1 716 604 7625" 
    login_session["ideas"] = 0
    login_session["projects"] = ['1']
    login_session["work_days"] = 0
    login_session["work_streak"] = 0
    login_session["tasks"] = 0
    login_session["awards"] = ['1','0','0']
    login_session["comp_day_tasks"] = 0
    login_session["tot_day_tasks"] = 0
    login_session["comp_tot_tasks"] = 0
    login_session["tot_tot_tasks"] = 0

    
    binary_data = io.BytesIO(urllib.request.urlopen(login_session["picture"]).read())
    name = "dp" + str(titan_id) + ".jpg"
    s3.Bucket('wecslabspropic').put_object(Key=name, Body=binary_data, ACL= 'public-read')

    table.put_item(Item = {
    'email': login_session["email"],
    'titan_id': login_session['titan_id'],
    'username': login_session["username"],
    'location': login_session["location"],
    'position': login_session["position"],
    'current_project': login_session["current_project"],
    'motivation': login_session['motivation'],
    'fb_link' : login_session[ 'fb_link'],
    'insta_link' : login_session['insta_link'],
    'linkedin_link' : login_session['linkedin_link'],
    'phone' : login_session['phone'],
    'ideas': login_session['ideas'],
    'projects' : login_session["projects"],
    'work_days': login_session['work_days'],
    'work_streak': login_session['work_streak'],
    'tasks': login_session['tasks'],
    'awards': login_session['awards'],
    'comp_day_tasks': login_session['comp_day_tasks'],
    'tot_day_tasks': login_session['tot_day_tasks'],
    'comp_tot_tasks': login_session['comp_tot_tasks'],
    'tot_tot_tasks': login_session['tot_tot_tasks']
    })
    return titan_id

#----------------------  Gets user Info -------------------------------------------------------------------------------------

def getUser(email):
    hash_object = hashlib.md5(email.encode('utf-8'))
    titan_id = str(hash_object.hexdigest())
    try:
        print("Try is working")
        response= table.get_item(
            Key={ 
                'titan_id': titan_id
            })
        return response['Item']
    except:
        return False