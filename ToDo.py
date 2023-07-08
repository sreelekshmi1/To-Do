from ast import Try
from itertools import count
from os import curdir
from turtle import title
from flask import Flask, render_template, request, redirect, url_for,session,flash
import sqlite3


app = Flask(__name__)

########################################################################################################################################################################################

#Intial database setup


def table_notexists(table_name):
    conn = sqlite3.connect('ToDo.db')  
    cursor = conn.cursor()
    # Check if the table exists in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    # Close the connection
    conn.close()
    if result is not None:
        return False
    else:
        return True
conn = sqlite3.connect('ToDo.db');
if table_notexists("user"):
     conn.execute(
    'CREATE TABLE user (username VARCHAR(50) PRIMARY KEY, FirstName VARCHAR(50), LastName VARCHAR(50), Mobile INT, Email VARCHAR(100),password VARCHAR(100))'
    );
if table_notexists("login"):
    conn.execute(
    'CREATE TABLE login (username VARCHAR(50) PRIMARY KEY, password VARCHAR(100),status INT)'
    );
if table_notexists("todo"):
    conn.execute(
    'CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR(50), description VARCHAR(200),username VARCHAR(50),status int)'
    );

conn.commit()
conn.close()  


app = Flask(__name__)
app.secret_key = 'ToDo@7012'




#end of database setup

###################################################################################################################################################################################
 
 #registration starts

@app.route('/register') 
def register():
    return render_template('registration.html')

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    userna = request.form['username']
    mob=int(request.form['mob'])
    email=request.form['email']
    password=request.form['psw']
    conect=sqlite3.connect("ToDo.db")
    curreg = conect.cursor()
    curreg.execute("INSERT INTO user (username,FirstName,LastName,Mobile,Email,Password) VALUES (?,?,?,?,?,?)",(userna,firstname,lastname,mob,email,password))
    curreg.execute("INSERT INTO login (username,password,status) VALUES (?,?,?)",(userna,password,0))
    #flash("User registered succesfully")
    conect.commit()
    conect.close()
    return render_template('login.html')


 #registration ends

########################################################################################################################################################################################

#index page start

@app.route('/index', methods=['GET', 'POST'])
def index():
    conn1 = sqlite3.connect('ToDo.db')  
    cur2 = conn1.cursor()
    username=session['user_id']
    cur2.execute("SELECT * FROM todo WHERE username=? and status=0", (username,))
    rows = cur2.fetchall()
    conn1.close()
   
    if rows is None:
        msg = 'Please add a task.'
        return render_template('todos1.html', msg=msg)
    else:
        return render_template('todos1.html',rows=rows)
#index page ends

###############################################################################################################################################################

#login start

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn1 = sqlite3.connect('ToDo.db')  
        cur = conn1.cursor()
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
        rows = cur.fetchall()
        session['user_id'] = username
        
        if rows is None:
            # Authentication failed, display an error message
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
        else:
             
             # Authentication successful, redirect to a protected page
             conn1 = sqlite3.connect('ToDo.db')  
             cur2 = conn1.cursor()
             cur2.execute("SELECT * FROM todo WHERE username=? and status=0", (username,))
             rows = cur2.fetchall()
             conn1.close()
             conn1 = sqlite3.connect('ToDo.db')  
             cur = conn1.cursor()
             conn1.close()
             
             if rows is None:
                 
                 msg = 'Please add a task.'
                 return render_template('todos1.html', msg=msg)
             else:
                 
                 return render_template('todos1.html',rows=rows)
@app.route('/') 
def index1():
    return render_template('login.html') 
                  
 #login ends


 #######################################################################################################################################################################################

 #add task start

@app.route('/add',methods = ['POST', 'GET'])
def add():
   title = request.form['title']
   desc = request.form['desc']
   user= session['user_id']
   con=sqlite3.connect("ToDo.db")
   cur = con.cursor()
   cur.execute("INSERT INTO todo (task,description,username,status) VALUES (?,?,?,?)",(title,desc,user,0))
   con.commit()
   con.close()
   conn1 = sqlite3.connect('ToDo.db')  
   cur1 = conn1.cursor()
   cur1.execute("SELECT * FROM todo WHERE username=? and status=0", (user,))
   rows = cur1.fetchall()
   conn1.close()
   if rows is None:
       
       msg = 'Please add a task.'
       return render_template('todos1.html', msg=msg)
   else:
        
        return render_template('todos1.html',rows=rows)
   return render_template('todos1.html')

   

 #add start ends

 ################################################################################################################################################################################

 #delete data start
@app.route('/delete_task/<int:id1>', methods=['POST'])
def delete_task(id1):
    conn1 = sqlite3.connect('ToDo.db')  
    cur = conn1.cursor()
    user= session['user_id']
    cur.execute("DELETE FROM todo WHERE username=? AND id=?", (user,id1))
    conn1.commit()
    conn1.close()
    conn3 = sqlite3.connect('ToDo.db')  
    cur3 = conn3.cursor()
    cur3.execute("SELECT * FROM todo WHERE username=? and status=0", (user,))
    rowsdel = cur3.fetchall()
    conn3.close()
    if rowsdel is None:
        msg = 'Please add a task.'
        return render_template('todos1.html', msg=msg)
    else:
        return render_template('todos1.html',rows=rowsdel)
    
 #delete data ends

 #######################################################################################################################################################################################

#update data start
@app.route('/update_task', methods=['POST'])
def update_task():
    id2 = request.form.get('task_id')
    if id2 is None:
        print("no task id")
    title1 = request.form.get('task_name')
    desc = request.form.get('task_desc')
    user1= session['user_id']
    conn1 = sqlite3.connect('ToDo.db') 
    cur = conn1.cursor()
    cur.execute("UPDATE todo SET task= ?,description=? WHERE username=? AND id=?", (title1,desc,user1,id2))
    conn1.commit()
    conn1.close()
    conn3 = sqlite3.connect('ToDo.db')  
    cur3 = conn3.cursor()
    cur3.execute("SELECT * FROM todo WHERE username=? and status=0", (user1,))
    rowsup = cur3.fetchall()
    conn3.close()
    if rowsup is None:
        msg = 'Please add a task.'
        return render_template('todos1.html', msg=msg)
    else:
        flash('Succesfully updated','success')
        return render_template('todos1.html',rows=rowsup)
    
 #update data ends

 ###################################################################################################################################################################################

 #set task to done
@app.route('/done_task/<int:id12>', methods=['POST'])
def done_task(id12):
    user1= session['user_id']
    conn1 = sqlite3.connect('ToDo.db') 
    cur = conn1.cursor()
    cur.execute("UPDATE todo SET status= ? WHERE username=? AND id=?", (1,user1,id12))
    conn1.commit()
    conn1.close()
    conn3 = sqlite3.connect('ToDo.db')  
    cur3 = conn3.cursor()
    cur3.execute("SELECT * FROM todo WHERE username=? and status=0" , (user1,))
    rowsup = cur3.fetchall()
    conn3.close()
    if rowsup is None:
        msg = 'Please add a task.'
        return render_template('todos1.html', msg=msg)
    else:
        flash('Task completed Succesfully','success')
        return render_template('todos1.html',rows=rowsup)
    

 #set task to done ends

 ###################################################################################################################################################################################

 
 #view task status

@app.route('/status', methods=['POST','GET'])
def status():
     user1= session['user_id']
     conn3 = sqlite3.connect('ToDo.db')  
     cur3 = conn3.cursor()
     cur3.execute("SELECT * FROM todo WHERE username=?" , (user1,))
     rowsview = cur3.fetchall()
     conn3.close()
     if rowsview is None:
        msg = 'No Task found.'
        return render_template('task.html', msg=msg)
     else:
        return render_template('task.html',rows=rowsview)
     

#view task statusend 
 
 #######################################################################################################################################################################################
   
  #view inprogress task

@app.route('/Inprogress', methods=['POST'])
def Inprogress():
     user1= session['user_id']
     conn3 = sqlite3.connect('ToDo.db')  
     cur3 = conn3.cursor()
     cur3.execute("SELECT * FROM todo WHERE username=? and status=0" , (user1,))
     rowsview = cur3.fetchall()
     conn3.close()
     if rowsview is None:
        msg = 'No Task found.'
        return render_template('task.html', msg=msg)
     else:
        return render_template('task.html',rows=rowsview)
     

#view inprogress task end 
 
 #######################################################################################################################################################################################
   
  
 #view completed task

@app.route('/Completed', methods=['POST'])
def Completed():
     user1= session['user_id']
     conn3 = sqlite3.connect('ToDo.db')  
     cur3 = conn3.cursor()
     cur3.execute("SELECT * FROM todo WHERE username=? and status=1" , (user1,))
     rowsview = cur3.fetchall()
     conn3.close()
     if rowsview is None:
        msg = 'No Task found.'
        return render_template('task.html', msg=msg)
     else:
        return render_template('task.html',rows=rowsview)
     

# view completed task end 
 
 #######################################################################################################################################################################################

 #delete data start1
@app.route('/delete_task1/<int:id1>', methods=['POST'])
def delete_task1(id1):
    conn1 = sqlite3.connect('ToDo.db')  
    cur = conn1.cursor()
    user= session['user_id']
    cur.execute("DELETE FROM todo WHERE username=? AND id=?", (user,id1))
    conn1.commit()
    conn1.close()
    conn3 = sqlite3.connect('ToDo.db')  
    cur3 = conn3.cursor()
    cur3.execute("SELECT * FROM todo WHERE username=? and status=0", (user,))
    rowsdel = cur3.fetchall()
    conn3.close()
    if rowsdel is None:
        msg = 'Please add a task.'
        return render_template('task.html', msg=msg)
    else:
        return render_template('task.html',rows=rowsdel)
    
 #delete data ends

 #######################################################################################################################################################################################

#update data start1
@app.route('/update_task1', methods=['POST'])
def update_task1():
    id2 = request.form.get('task_id')
    if id2 is None:
        print("no task id")
    title1 = request.form.get('task_name')
    desc=request.form.get('task_desc')
    user1= session['user_id']
    conn1 = sqlite3.connect('ToDo.db') 
    cur = conn1.cursor()
    cur.execute("UPDATE todo SET task= ?,description=? WHERE username=? AND id=?", (title1,desc,user1,id2))
    conn1.commit()
    conn1.close()
    conn3 = sqlite3.connect('ToDo.db')  
    cur3 = conn3.cursor()
    cur3.execute("SELECT * FROM todo WHERE username=? and status=0", (user1,))
    rowsup = cur3.fetchall()
    conn3.close()
    if rowsup is None:
        msg = 'Please add a task.'
        return render_template('task.html', msg=msg)
    else:
        flash('Succesfully updated','success')
        return render_template('task.html',rows=rowsup)
    
 #update data ends

 ###################################################################################################################################################################################

 #set task to done1
@app.route('/done_task1/<int:id12>', methods=['POST'])
def done_task1(id12):
    user1= session['user_id']
    conn1 = sqlite3.connect('ToDo.db') 
    cur = conn1.cursor()
    cur.execute("UPDATE todo SET status= ? WHERE username=? AND id=?", (1,user1,id12))
    conn1.commit()
    conn1.close()
    conn3 = sqlite3.connect('ToDo.db')  
    cur3 = conn3.cursor()
    cur3.execute("SELECT * FROM todo WHERE username=? and status=0" , (user1,))
    rowsup = cur3.fetchall()
    conn3.close()
    if rowsup is None:
        msg = 'Please add a task.'
        return render_template('task.html', msg=msg)
    else:
        flash('Task completed Succesfully','success')
        return render_template('task.html',rows=rowsup)
    

 #set task to done ends

 #######################################################################################################################################################################################
 

 #logout starts
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')  
 #logout end 
 
 #######################################################################################################################################################################################


if __name__ == '__main__':
    app.run()
