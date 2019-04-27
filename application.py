import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application = Blueprint('application', __name__, template_folder='templates', static_folder='static')   


@application.route('new_application', methods=['GET'])
def new_application():
	sql = "INSERT INTO main_table(email,status) VALUES ('%s','%s') RETURNING application_no" %(session['email'],"new")
	cursor.execute(sql)
	rows = cursor.fetchall()
	db.commit()
	session['application_number'] = rows[0][0]
	
	sql = "INSERT INTO education(application_no,status) VALUES ('%s','%s') " %(session['application_number'],"new")
	cursor.execute(sql)
	db.commit()

	sql = "INSERT INTO teaching_experience(application_no,status) VALUES ('%s','%s') " %(session['application_number'],"new")
	cursor.execute(sql)
	db.commit()

	# sql = "INSERT INTO attachments(application_no,status) VALUES ('%s','%s') " %(session['application_number'],"new")
	# cursor.execute(sql)
	# db.commit()

	return render_template('application_part1.html', email_=session['email'], application_number=session['application_number'])


@application.route('part1', methods=['GET','POST'])       
def part1(): 
	if (request.method =='POST'):		#modifying the existing application
		session['application_number'] = request.form['application_no']
	sql = "SELECT * FROM main_table WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows = cursor.fetchall()
	rows = list(rows[0])
	name_list = rows[3][1:-1].split(",")
	print rows
	params_ = [rows[2],name_list,rows[9],rows[10],rows[11],rows[12],rows[8],rows[13], rows[4],rows[5],rows[6],rows[14]]
	print "retrieved properly"
	return render_template('application_placeholders_part1.html',params=params_, application_number=session['application_number'])



@application.route('insert_1', methods=['GET','POST'])       #on submission of login details
def insert_1(): 
	if (request.method =='POST'):
		position = request.form['position']
		firstname = request.form['first_name']
		middlename = request.form['middle_name']
		lastname = request.form['last_name']
		if middlename == "":
			name =  "(\""+firstname+"\", ,\""+lastname+"\")"
		else:	
			name =  "(\""+firstname+"\",\""+middlename+"\",\""+lastname+"\")"
		address1 = request.form['address_1']
		address2 = request.form['address_2']
		address3 = request.form['address_3']
		altemail = request.form['alt_email']
		nationality = request.form['nationality']
		age = request.form['age']
		date_of_birth = request.form['date_of_birth']
		caste = request.form['caste']
		disability = request.form['disability']
		other_info = request.form['other_info']
		
		params = [position,[firstname,middlename,lastname],nationality,age,date_of_birth,
		caste,altemail,disability,address1,address2,address3,other_info]

		status = "modified"

		sql = "UPDATE main_table SET position_applied = '%s', name='%s',address1='%s', address2='%s', address3='%s',\
		alt_email='%s',nationality='%s',age='%d',date_of_birth='%s',caste='%s', status='%s',\
		disability='%s',other_info='%s' WHERE application_no = '%d';" % (position,name,address1,address2,address3,\
		altemail,nationality,int(age),date_of_birth,caste,status,disability,other_info,int(session['application_number']))

		print sql
		print session['application_number']

		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Form personal info is stored"
		except:
			print "Info error"

	return render_template('application_placeholders_part1.html',params=params, email_=session['email'], application_number=session['application_number'])

