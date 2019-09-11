# -*- coding: utf-8 -*-
"""
	Predict Customer Churn
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	An example web application for making predicions using a saved WLM model
	using Flask and the IBM WLM APIs.

	Created by Rich Tarro
	Updated by Sidney Phoon
	May 2017
"""

import os, urllib3, requests, json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash


app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
))

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/MortgageDefault'
#postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/mydb
#db = SQLAlchemy(app)


def predictDefault(Gender,Status,Children,EstIncome,CarOwner,Age,AvgMonthlySpend,CustomerSupportCalls,Paymethod,MembershipPlan):
	
	
	apikey = '*******'
	
	# Get an IAM token from IBM Cloud
	url     = "https://iam.bluemix.net/oidc/token"
	headers = { "Content-Type" : "application/x-www-form-urlencoded" }
	data    = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
	IBM_cloud_IAM_uid = "bx"
	IBM_cloud_IAM_pwd = "bx"
	response  = requests.post( url, headers=headers, data=data, auth=( IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd ) )
	iam_token = response.json()["access_token"]
	
	ml_instance_id='******'
	
	header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': ml_instance_id}

	
	#scoring_href = 'https://us-south.ml.cloud.ibm.com/v3/wml_instances/55808dd2-bc65-446b-8c1a-ac08a4c1ab3b/deployments/b813db9e-0144-45dd-b858-10c2b9535bca/online'
	scoring_endpoint='https://us-south.ml.cloud.ibm.com/v3/wml_instances/2d66a4d8-b28f-47c3-a667-8d7409861f75/deployments/116be511-c167-472f-ad7a-720d52fd9680/online'
	
	payload_scoring={
    "fields": [
    "Gender",
    "Status",
    "Children",
    "EstIncome",
    "CarOwner",
    "Age",
    "AvgMonthlySpend",
    "CustomerSupportCalls",
    "Paymethod",
    "MembershipPlan"
    ],
    "values": [ [Gender,Status,Children,EstIncome,CarOwner,Age,AvgMonthlySpend,CustomerSupportCalls,Paymethod,MembershipPlan] ]} 


	response_scoring = requests.post(scoring_endpoint, json=payload_scoring, headers=header)
	
	result = response_scoring.text
	print("Result:")
	print(result)
	return response_scoring


@app.route('/',  methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		ID = 999
		#Gender='F'
		#Status='S'
		#Children=0.000000
		#EstIncome=5185.310000
		#CarOwner='N'
		#Age=62.053333
		#AvgMonthlySpend=16.390000
		#CustomerSupportCalls=0.000000
		#Paymethod='CC'
		#MembershipPlan=2.000000

		Gender=request.form['Gender']
		Status='S'
		Children=int(request.form['Children'])
		EstIncome=int(request.form['EstIncome'])
		CarOwner=request.form['CarOwner']
		Age=int(request.form['Age'])
		AvgMonthlySpend=int(request.form['AvgMonthlySpend'])
		CustomerSupportCalls=int(request.form['CustomerSupportCalls'])
		Paymethod=request.form['Paymethod']
		MembershipPlan=int(request.form['MembershipPlan'])
		
		
		
		session[Gender]=Gender
		session[Status]=Status
		session[Children]=Children
		session[EstIncome] = EstIncome
		session[CarOwner]=CarOwner
		session[Age]=Age
		session[AvgMonthlySpend]=AvgMonthlySpend
		session[CustomerSupportCalls]=CustomerSupportCalls
		session[Paymethod]=Paymethod
		session[MembershipPlan]=MembershipPlan



		response_scoring = predictDefault(Gender,Status,Children,EstIncome,CarOwner,Age,AvgMonthlySpend,CustomerSupportCalls,Paymethod,MembershipPlan)
		print(response_scoring)
		prediction=response_scoring.json()['values'][0][20]
		probability= response_scoring.json()['values'][0][19][1]

		session['prediction'] = prediction
		session['probability'] = probability

		#flash('Successful Prediction')
		return render_template('scoreSQL.html', response_scoring=response_scoring, request=request)


	else:
		return render_template('input.html')


#if __name__ == '__main__':
#   app.run()
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
