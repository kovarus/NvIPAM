from flask import Flask, json, url_for
from flask_restplus import Resource, Api
from run import api, app

app.config['SERVER_NAME'] = 'localhost'

def see_json():
	urlvars = False # Build query strings in URLs
	swagger = True # Export Swagger specifications
	data = api.as_postman(urlvars=urlvars, swagger=swagger)
	print(json.dumps(data))

with app.app_context():
	see_json()


