import psycopg2

conn = psycopg2.connect(database="recruitment_portal", user = "postgres", password = "root", host = "127.0.0.1", port = "5432")

print "Opened database successfully"

cur = conn.cursor()


#### CREATING TYPES

cur.execute('''CREATE TYPE name_info AS (first_name text, middle_name text, last_name text); ''')

# cur.execute('''CREATE TYPE address_info AS (house_no text, locality text, city text,
# 	district text,state text,pin_code integer,country text ); ''')

cur.execute('''CREATE TYPE education_info AS (date_studied date, university text,
	specialization text,cgpa decimal);''')


cur.execute('''CREATE TYPE phd_thesis_info AS (date_thesis date,
	date_defence date  );''')

cur.execute('''CREATE TYPE gate_info AS (type text,gate_score integer); ''')

# cur.execute('''CREATE TYPE research_info AS (specialization text, interest text[]);''')

cur.execute('''CREATE TYPE position_info AS (position text, pay_band integer, grade_pay integer,
	consolidated_salary integer);''')

cur.execute('''CREATE TYPE experience_info AS (organization text,start_date date,end_date date,
	total_period integer,full_time boolean, desgn text, type_of_work text);''')

cur.execute('''CREATE TYPE project_info AS (project_number integer,amount integer );''')

cur.execute('''CREATE TYPE referee_info AS (email text,name text,desgn text,
	address text);''')

####CREATING TABLES


cur.execute('''CREATE TABLE main_table (application_no serial primary key, status text,
	position_applied text,name name_info, address1 text,address2 text,address3 text,email text,
	alt_email text, nationality text, age integer, date_of_birth text, caste text,
	disability boolean, photo text, signature text,other_info text,date_submitted date );''')

cur.execute('''CREATE TABLE education (application_no integer references main_table(application_no), status text,
	bachelors education_info,masters education_info,phd education_info,phd_thesis phd_thesis_info,post_doc text[],
	gate gate_info,research_specialization text,research_interest text[]);''')

cur.execute('''CREATE TABLE teaching_experience (application_no integer references main_table(application_no),
	status text, postion position_info, experience experience_info,
	google_scholar text, dblp text, linkedin text, sponsored_project project_info,
	consultancy_project project_info,referee referee_info[]);''')

cur.execute('''CREATE TABLE attachments (application_no integer references main_table(application_no), status text,
	cv text,list_of_publications text,research_statement text,teaching_statement text);''')


conn.commit()
conn.close()
