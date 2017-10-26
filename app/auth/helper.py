from flask import Flask, url_for, redirect
import hashlib
import io
import urllib
import uuid
from . import auth
import boto3
import base64
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from flask_mail import Mail, Message
from flask import session as login_session
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wecslabsuser')
table_history = dynamodb.Table('wecslabs_history')
s3 = boto3.resource('s3')

#----------------------  Adds a user ----------------------------------------------------------------------------------------
def createUser(login_session):
    hash_object = hashlib.md5(login_session['email'].encode('utf-8'))
    titan_id = str(hash_object.hexdigest())
    login_session["titan_id"] = titan_id
    login_session["user_location"] = "City, Country"
    login_session["position"] = "Unassigned"
    login_session["current_project"] = "No Projects"
    login_session["motivation"] = "Hardwork beats Talent"
    login_session["fb_link"] = "http://www.facebook.com"
    login_session["insta_link"] = "http://www.instagram.com"
    login_session["linkedin_link"] = "http://www.linkedin.com"
    login_session["phone"] = "+1 716 604 7625" 
    login_session["ideas"] = 0
    login_session["projects"] = []
    login_session["work_days"] = 0
    login_session["work_streak"] = 0
    login_session["tasks"] = 0
    login_session["awards"] = ['A','A','B']
    login_session["award_tag"] = ['No Award', 'No Award', 'Joined WecsLabs']
    login_session["max_tasks"] = 1
    login_session["comp_day_tasks"] = 1
    login_session["tot_day_tasks"] = 1
    login_session["comp_tot_tasks"] = 1
    login_session["tot_tot_tasks"] = 1

    login_session['display'] = [{'id': 1,'award': '/static/img/awards/B.png', 'desc': 'Joined WecsLabs Award'}]


    
    binary_data = io.BytesIO(urllib.request.urlopen(login_session["picture"]).read())
    name = "dp" + str(titan_id) + ".jpg"
    s3.Bucket('wecslabspropic').put_object(Key=name, Body=binary_data, ACL= 'public-read')

    table.put_item(Item = {
    'email': login_session["email"],
    'titan_id': login_session['titan_id'],
    'username': login_session["username"],
    'user_location': login_session["user_location"],
    'user_position': login_session["position"],
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
    'max_tasks':login_session['max_tasks'],
    'comp_day_tasks': login_session['comp_day_tasks'],
    'tot_day_tasks': login_session['tot_day_tasks'],
    'comp_tot_tasks': login_session['comp_tot_tasks'],
    'tot_tot_tasks': login_session['tot_tot_tasks'],
    'award_tag': login_session['award_tag']
    })

    current_date = datetime.now().strftime('%m/%d/%Y')

    table_history.put_item(Item = {
    'titan_id': login_session['titan_id'],
    'recent_date': current_date,
    'user_tot_task': 0,
    'extra_task': 0
    })
    return titan_id

#----------------------  Gets user Info -------------------------------------------------------------------------------------

def getUser(email):
    hash_object = hashlib.md5(email.encode('utf-8'))
    titan_id = str(hash_object.hexdigest())
    try:
        response= table.get_item(
            Key={ 
                'titan_id': titan_id
            })
        return response['Item']
    except:
        return False


def calc_stats():
    current_date = datetime.now().strftime('%m/%d/%Y')
    response= table_history.get_item(
            Key={ 
                'titan_id': login_session['titan_id']
            })
    
    if current_date == response['Item']['recent_date']:
        pass
    else:
        login_session['display'] = []

        if login_session['comp_tot_tasks'] > 300 and ('K' not in login_session['awards']):
            result = table.update_item(
            Key = {
                'titan_id': login_session['titan_id']
            },
            UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
            ExpressionAttributeNames = {
                "#attrName" : "awards",
                "#attrName1" : "award_tag"
            },
            ExpressionAttributeValues = {
                ":attrValue" : ['K'],
                ":attrValue1" : ['100 tasks complete']
            })

            login_session['awards'].append('K')
            login_session['award_tag'].append('100 tasks complete')
            length = len(login_session['display'])
            login_session['display'].append({'id': length + 1,'award': '/static/img/awards/K.png', 'desc': '100 tasks complete'})

        elif login_session['comp_tot_tasks']> 100 and ('H' not in login_session['awards']):
            result = table.update_item(
            Key = {
                'titan_id': login_session['titan_id']
            },
            UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
            ExpressionAttributeNames = {
                "#attrName" : "awards",
                "#attrName1" : "award_tag"
            },
            ExpressionAttributeValues = {
                ":attrValue" : ['H'],
                ":attrValue1" : ['50 tasks complete']
            })

            login_session['awards'].append('H')
            login_session['award_tag'].append('50 tasks complete')

            length = len(login_session['display'])
            login_session['display'].append({'id': length+1,'award': '/static/img/awards/H.png', 'desc': '50 tasks complete'})

        elif login_session['comp_tot_tasks']> 10 and ('D' not in login_session['awards']):
            result = table.update_item(
            Key = {
                'titan_id': login_session['titan_id']
            },
            UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
            ExpressionAttributeNames = {
                "#attrName" : "awards",
                "#attrName1" : "award_tag"
            },
            ExpressionAttributeValues = {
                ":attrValue" : ['D'],
                ":attrValue1" : ['10 tasks complete']
            })

            login_session['awards'].append('D')
            login_session['award_tag'].append('10 tasks complete')

            length = len(login_session['display'])
            login_session['display'].append({'id': length+1,'award': '/static/img/awards/D.png', 'desc': '10 tasks complete'})

        else:
            pass


        if login_session['comp_tot_tasks'] > int(response['Item']['user_tot_task']):
            login_session['work_days'] +=1

            if login_session['work_days'] > 40 and ('L' not in login_session['awards']):
                result = table.update_item(
                Key = {
                    'titan_id': login_session['titan_id']
                },
                UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                ExpressionAttributeNames = {
                    "#attrName" : "awards",
                    "#attrName1" : "award_tag"
                },
                ExpressionAttributeValues = {
                    ":attrValue" : ['L'],
                    ":attrValue1" : ['100 workdays']
                })

                login_session['awards'].append('L')
                login_session['award_tag'].append('100 workdays')
                length = len(login_session['display'])
                login_session['display'].append({'id': length + 1,'award': '/static/img/awards/L.png', 'desc': '100 workdays'})

            elif login_session['work_days']> 20 and ('I' not in login_session['awards']):
                result = table.update_item(
                Key = {
                    'titan_id': login_session['titan_id']
                },
                UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                ExpressionAttributeNames = {
                    "#attrName" : "awards",
                    "#attrName1" : "award_tag"
                },
                ExpressionAttributeValues = {
                    ":attrValue" : ['I'],
                    ":attrValue1" : ['50 workdays']
                })

                login_session['awards'].append('I')
                login_session['award_tag'].append('50 workdays')

                length = len(login_session['display'])
                login_session['display'].append({'id': length+1,'award': '/static/img/awards/I.png', 'desc': '50 workdays'})

            elif login_session['work_days']> 10 and ('E' not in login_session['awards']):
                result = table.update_item(
                Key = {
                    'titan_id': login_session['titan_id']
                },
                UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                ExpressionAttributeNames = {
                    "#attrName" : "awards",
                    "#attrName1" : "award_tag"
                },
                ExpressionAttributeValues = {
                    ":attrValue" : ['E'],
                    ":attrValue1" : ['10 workdays']
                })

                login_session['awards'].append('E')
                login_session['award_tag'].append('10 workdays')

                length = len(login_session['display'])
                login_session['display'].append({'id': length+1,'award': '/static/img/awards/E.png', 'desc': '10 workdays'})

            else:
                pass


            extra_task = login_session['comp_tot_tasks'] - int(response['Item']['user_tot_task'])
            if extra_task >= 20 and ('G' not in login_session['awards']):
                result = table.update_item(
                Key = {
                    'titan_id': login_session['titan_id']
                },
                UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                ExpressionAttributeNames = {
                    "#attrName" : "awards",
                    "#attrName1" : "award_tag"
                },
                ExpressionAttributeValues = {
                    ":attrValue" : ['G'],
                    ":attrValue1" : ['20 tasks a day']
                })

                login_session['awards'].append('G')
                login_session['award_tag'].append('20 tasks a day')
                length = len(login_session['display'])
                login_session['display'].append({'id': length + 1,'award': '/static/img/awards/G.png', 'desc': '20 tasks a day'})

            if login_session['max_tasks'] < extra_task:
                login_session['max_tasks'] = extra_task

            user_tot_task = login_session['comp_tot_tasks']

            c_date = datetime.strptime(current_date, '%m/%d/%Y')   
            p_date = datetime.strptime(response['Item']['recent_date'], '%m/%d/%Y') 
            delta = c_date - p_date
            difference = delta.days

            if difference > 1:
                login_session['work_streak'] = 0
            else:
                login_session['work_streak']+=1
                if login_session['work_streak'] > 60 and ('M' not in login_session['awards']):
                    result = table.update_item(
                    Key = {
                        'titan_id': login_session['titan_id']
                    },
                    UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                    ExpressionAttributeNames = {
                        "#attrName" : "awards",
                        "#attrName1" : "award_tag"
                    },
                    ExpressionAttributeValues = {
                        ":attrValue" : ['M'],
                        ":attrValue1" : ['60 day workstreak']
                    })

                    login_session['awards'].append('M')
                    login_session['award_tag'].append('60 day workstreak')
                    length = len(login_session['display'])
                    login_session['display'].append({'id': length + 1,'award': '/static/img/awards/M.png', 'desc': '60 day workstreak'})

                elif login_session['work_streak']> 40 and ('J' not in login_session['awards']):
                    result = table.update_item(
                    Key = {
                        'titan_id': login_session['titan_id']
                    },
                    UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                    ExpressionAttributeNames = {
                        "#attrName" : "awards",
                        "#attrName1" : "award_tag"
                    },
                    ExpressionAttributeValues = {
                        ":attrValue" : ['J'],
                        ":attrValue1" : ['40 day workstreak']
                    })

                    login_session['awards'].append('J')
                    login_session['award_tag'].append('40 day workstreak')

                    length = len(login_session['display'])
                    login_session['display'].append({'id': length+1,'award': '/static/img/awards/J.png', 'desc': '40 day workstreak'})

                elif login_session['work_streak']> 15 and ('F' not in login_session['awards']):
                    result = table.update_item(
                    Key = {
                        'titan_id': login_session['titan_id']
                    },
                    UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue), #attrName1 = list_append(#attrName1, :attrValue1)",
                    ExpressionAttributeNames = {
                        "#attrName" : "awards",
                        "#attrName1" : "award_tag"
                    },
                    ExpressionAttributeValues = {
                        ":attrValue" : ['F'],
                        ":attrValue1" : ['15 day workstreak']
                    })

                    login_session['awards'].append('F')
                    login_session['award_tag'].append('15 day workstreak')

                    length = len(login_session['display'])
                    login_session['display'].append({'id': length+1,'award': '/static/img/awards/F.png', 'desc': '15 day workstreak'})

                else:
                    pass






        else:
            user_tot_task = login_session['comp_tot_tasks']
            extra_task = login_session['comp_tot_tasks'] - user_tot_task
            login_session['work_streak'] = 0

        response = table_history.update_item(
        Key ={
        'titan_id': login_session['titan_id']
        },
        UpdateExpression = 'set recent_date = :current_date, user_tot_task = :user_tot_task, extra_task = :extra_task',
        ExpressionAttributeValues = {
            ':current_date': current_date,
            ':user_tot_task': user_tot_task,
            ':extra_task': extra_task
        },
        ReturnValues = 'ALL_NEW'
        )

        response = table.update_item(
        Key ={
        'titan_id': login_session['titan_id']
        },
        UpdateExpression = 'set work_days = :work_days, work_streak = :work_streak, max_tasks = :max_tasks',
        ExpressionAttributeValues = {
            ':work_days': login_session['work_days'],
            ':work_streak' : login_session['work_streak'],
            ':max_tasks' : login_session['max_tasks']
        },
        ReturnValues = 'ALL_NEW'
        )

                   
