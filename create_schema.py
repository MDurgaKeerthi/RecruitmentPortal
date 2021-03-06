
## PREREQUISITE : There is already a database created and named as recruitment portal.
## Password and user name can be changed in the connect statement.

'''This code corresponds to creating the tables and types in the database.
   main_table - It corresponds to the table where the personal info of the applicant is stored.
   education - It corresponds to the table where the education qualifications of the applicant is stored.
   teaching_experience - It corresponds to the table where the experience of the applicant is stored.
   attachments - It stores the cv,teaching statement,research statement, list of publications of the applicant.
   This is a table that can be modified even after submitting the application. '''

import psycopg2

conn = psycopg2.connect(database="recruitment_portal", user = "postgres", password = "root", host = "127.0.0.1", port = "5432")

print "Opened database successfully"

cur = conn.cursor()

#### CREATING TYPES

cur.execute('''CREATE TYPE name_info AS (first_name text, middle_name text, last_name text); ''')

cur.execute('''CREATE TYPE education_info AS (date_studied date, university text,institute text,
	specialization text,cgpa decimal , scale integer);''')


cur.execute('''CREATE TYPE phd_thesis_info AS (date_thesis date,
	date_defence date  );''')

cur.execute('''CREATE TYPE gate_info AS (year integer,gate_score integer); ''')

cur.execute('''CREATE TYPE position_info AS (position text, pay_band text, grade_pay text,
	consolidated_salary text);''')


cur.execute('''CREATE TYPE referee_info AS (email text,name text,desgn text,
	address text);''')

####CREATING TABLES

cur.execute('''CREATE TABLE main_table (application_no serial primary key, status text,
	position_applied text,name name_info, address1 text,address2 text,address3 text,email text,
	alt_email text, nationality text, age integer, date_of_birth text, caste text,
	disability text,other_info text,gender text,marital_status text,date_submitted date, attachment_status text,freeze_status text );''')

cur.execute('''CREATE TABLE education (application_no integer references main_table(application_no), status text,
	bachelors education_info,bachelors2 education_info,masters education_info,masters2 education_info,phd education_info,phd_thesis phd_thesis_info,
	gate gate_info,research_specialization text,research_interest text[]);''')

cur.execute('''CREATE TABLE teaching_experience (application_no integer references main_table(application_no),
	status text, post_doc text[],position position_info,experience_organization text[],experience_start_date date[],
	experience_end_date date[], experience_total_period text[], experience_full_time text[],
	experience_desgn text[],experience_type_of_work text[],project_type text[],
	project_title text[],project_amount text[],project_details text[],
	google_scholar text, dblp text, linkedin text,
	referee1 referee_info,referee2 referee_info,referee3 referee_info,remarks text);''')

cur.execute('''CREATE TABLE attachments (application_no integer references main_table(application_no), type text, 
	filename text, time_submitted timestampTZ DEFAULT NOW());''')

cur.execute('''CREATE TABLE admins (email text);''')

conn.commit()
conn.close()
