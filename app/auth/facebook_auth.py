from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from datetime import datetime

from . import auth
from .helper import getUser, createUser, calc_stats

# --------------------------------------------------------------------------------------------------------------------------
#                  Facebook Login and Logout
#---------------------------------------------------------------------------------------------------------------------------
@auth.route('/fbconnect', methods=['POST'])

#-----------------------------------  FACEBOOK LOGIN -----------------------------------------------------------------------
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data.decode('utf-8')

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)

    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')

    userinfo_url = "https://graph.facebook.com/v2.8/me"

    token0 = result.split(",")[0]
    token = token0.split('"')[3]

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token

    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')
    data = json.loads(result)

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.9/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    user = getUser(login_session['email'])
    if not user:
        titan_id = createUser(login_session)
    if user:
        login_session['titan_id'] = str(user["titan_id"])
        login_session["username"] = str(user["username"])
        login_session["user_location"] = str(user["user_location"])
        login_session["position"] = str(user["user_position"])
        login_session["current_project"] = str(user["current_project"])
        login_session['motivation'] = str(user["motivation"])
        login_session['fb_link'] = str(user["fb_link"])
        login_session['insta_link'] = str(user["insta_link"])
        login_session['linkedin_link'] = str(user["linkedin_link"])
        login_session['phone'] = str(user["phone"])
        login_session['ideas'] = str(user["ideas"])
        login_session["projects"] = (user["projects"])
        login_session['work_days'] = int(user["work_days"])
        login_session['work_streak'] = int(user["work_streak"])
        login_session['tasks'] = str(user["tasks"])
        login_session['awards'] = (user["awards"])
        login_session['award_tag'] = (user["award_tag"])
        login_session['max_tasks'] = int(user["max_tasks"])
        login_session['comp_day_tasks'] = int(user["comp_day_tasks"])
        login_session['tot_day_tasks'] = int(user["tot_day_tasks"])
        login_session['comp_tot_tasks'] = int(user["comp_tot_tasks"])
        login_session['tot_tot_tasks'] = int(user["tot_tot_tasks"])
        login_session['display'] = []

        calc_stats()
    return "Welcome"


#-----------------------------------  FACEBOOK LOGOUT -----------------------------------------------------------------------
@auth.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']

    if access_token is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)

    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    """Reset the user's session"""
    del login_session['facebook_id']
    del login_session['state']
    del login_session['access_token']
    del login_session["email"],
    del login_session['titan_id'],
    del login_session["username"],
    del login_session["user_location"],
    del login_session["position"],
    del login_session["current_project"],
    del login_session['motivation'],
    del login_session['fb_link'],
    del login_session['insta_link'],
    del login_session['linkedin_link'],
    del login_session['phone'],
    del login_session['ideas'],
    del login_session["projects"],
    del login_session['work_days'],
    del login_session['work_streak'],
    del login_session['tasks'],
    del login_session['awards'],
    del login_session['max_tasks'],
    del login_session['comp_day_tasks'],
    del login_session['tot_day_tasks'],
    del login_session['comp_tot_tasks'],
    del login_session['tot_tot_tasks'],
    del login_session['display']
    del login_session['award_tag']


    return redirect(url_for("home.homepage"))