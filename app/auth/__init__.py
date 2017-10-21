from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
from . import helper
from . import facebook_auth

import boto3
import random
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')