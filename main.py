
import re
from flask import *
# from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy.model import Model
import sqlite3
import os
from markupsafe import escape
import datetime
from database import * 


#initializing web framework / Flask class
app = Flask(__name__)




#Specify which funtion to run or the webpage 
@app.route('/')
def index():
    return render_template('index.html')

# app.route('/yuta') --> Create new webpage and look for yuta function to execute
@app.route('/agent_list/<name>')
def agent_list(name):
    #Create an instance of class database 
    conn = WarehouseDB('warehouse.db')
    #Create connection to DB
    conn1 = conn.create_connection()
    
    cur = conn1.cursor()
    cur.execute("select * from agent_list")
    rows = cur.fetchall()
    # print(rows, type(rows))
    conn.close_connection()
    return render_template('agent_list.html', rows = rows, name = name)

@app.route('/view_all/<name>')
def view_all(name):
    #Create an instance of class database 
    conn = WarehouseDB('warehouse.db')
    #Create connection to DB
    conn1 = conn.create_connection()
    
    cur = conn1.cursor()
    cur.execute("select * from trx")
    rows = cur.fetchall()
    # print(rows, type(rows))
    conn.close_connection()
    return render_template('view_all.html', rows = rows, name = name)


@app.route('/form_page/<name>', methods = ['GET', 'POST'])
def form_page(name):
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            #Format the time and date 
            Date = datetime.datetime.now()
            currTime = Date.strftime("%H:%M:%S")
            currDate = Date.strftime("%Y-%m-%d")
            msg = 'No response yet'
            #Create an instance of class database 
            conn = WarehouseDB('warehouse.db')
            #Create connection to DB
            conn1 = conn.create_connection()
            
            device_name = request.form['Device_Name']
            #request.form['userName'] = name
            note = request.form['Note']

            cur = conn1.cursor()
            cur.execute("INSERT INTO trx(Time, Data, Device_Name, Note, Agent, Result) VALUES(?, ?, ?, ?, ?, ?)", (currTime, currDate, device_name, note, name, msg))
            # cur.execute("INSERT INTO agent_list(Name) VALUES(?)", name)
            conn1.commit()
            
            conn.close_connection()
            return render_template('msg_page.html', name = name)
        
    else:
        #Create an instance of class database 
        conn = WarehouseDB('warehouse.db')
        #Create connection to DB
        conn1 = conn.create_connection()

        cur = conn1.cursor()
        # cur.execute("INSERT INTO agent_list(Name) VALUES(?)", [name])
        cur.execute("select * from agent_list where Name = (?)", [name])
        rows = cur.fetchall()

        conn.close_connection()

        if (len(rows) > 0):
            return render_template('form_page.html', name = name)

        else:
            #Create an instance of class database 
            conn = WarehouseDB('warehouse.db')
            #Create connection to DB
            conn1 = conn.create_connection()

            cur = conn1.cursor()
            cur.execute("INSERT INTO agent_list(Name) VALUES(?)", [name])
            conn1.commit()

            conn.close_connection()
            
            return render_template('form_page.html', name = name)
       

@app.route('/login/', methods=['POST', 'GET'])
def login():
    try: 
        if request.method == 'POST':
            if request.form["submit"] == "Login":
                #Create an instance of class database 
                conn = WarehouseDB('warehouse.db')
                #Create connection to DB
                conn1 = conn.create_connection()
                    
                userName = request.form['uname']
                password = request.form['psw']
                
                cur = conn1.cursor()
                cur.execute("select * from userLog where nameUser = (?) and password = (?)", (userName, password))
                rows = cur.fetchall()
                print(rows)

                conn.close_connection()
                
                if len(rows) == 1:
                    return redirect(url_for('userHome', name = userName))
    
                else:
                    msg1 = 'The username or password is not valid'
                    return render_template('login.html', msg1 = msg1)
                

            elif request.form["submit"] == "Go":
                #Create an instance of class database 
                conn = WarehouseDB('warehouse.db')
                #Create connection to DB
                conn1 = conn.create_connection()
                        
                adminName = request.form['adname']
                adminpassword = request.form['adpsw']

                cur = conn1.cursor()
                cur.execute("select * from adminLog where nameAd = (?) and passwordAd = (?)", (adminName, adminpassword))
                rows = cur.fetchall()
                conn.close_connection()
        
                if len(rows) == 1:
                    # return redirect('/admin/')
                    return redirect(url_for('admin', name = adminName))
                    
                else:
                    msg2 = 'The username or password is not valid'
                    return render_template('login.html', msg2 = msg2)
            
        else:
            return render_template('login.html')

    except Exception as e:
            print(str(e))

@app.route('/userHome/<name>')
def userHome(name):
    return render_template('userHome.html', name = name)

@app.route('/check_page/<name>')
def checkPage(name):
    #Create an instance of class database 
    conn = WarehouseDB('warehouse.db')
    #Create connection to DB
    conn1 = conn.create_connection()
    
    cur = conn1.cursor()
    cur.execute("select * from trx where Agent = (?)", [name])
    rows = cur.fetchall()

    return render_template('check_page.html', name = name, rows = rows)

@app.route('/checkRes/<name>')
def checkRes(name):
    #Create an instance of class database 
    conn = WarehouseDB('warehouse.db')
    #Create connection to DB
    conn1 = conn.create_connection()
    
    cur = conn1.cursor()
    cur.execute("select * from trx where Agent = (?)", [name])
    rows = cur.fetchall()

    return render_template('checkRes.html', name = name, rows = rows)

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # print(request.method, 'post')
        if request.form['submit'] == 'Sign-Up':

            userName = request.form['uname']
            password = request.form['psw']
            repassword = request.form['repsw']

            if (password == repassword):
                #Create an instance of class database 
                conn = WarehouseDB('warehouse.db')
                #Create connection to DB
                conn1 = conn.create_connection()

                cur = conn1.cursor()
                cur.execute("select * from userLog where nameUser =(?)", [userName])
                row = cur.fetchall()

                conn.close_connection()

                if (len(row) > 0):
                    msg = 'Your username is already exist, please try with other username'
                    return render_template('signup.html', msg = msg)

                else:
                    #Create an instance of class database 
                    conn = WarehouseDB('warehouse.db')
                    #Create connection to DB
                    conn1 = conn.create_connection()

                    cur = conn1.cursor()
                    cur.execute("INSERT INTO userLog(nameUser, password) VALUES(?, ?)", (userName, password))
                    conn1.commit()
                    conn.close_connection()
                    return redirect('/login/') 
                    
            
            else:
                msg = 'Your re-typed password not matched with an orginal password'
                return render_template('signup.html', msg = msg)

    else:    
        # print(request.method, 'else')
        return render_template('signup.html')

@app.route('/admin/<name>')
def admin(name):
    return render_template('admin.html', name = name)

@app.route('/user_list/<name>')
def user_list(name):
    #Create an instance of class database 
    conn = WarehouseDB('warehouse.db')
    #Create connection to DB
    conn1 = conn.create_connection()
    
    cur = conn1.cursor()
    cur.execute("select * from userLog")
    rows = cur.fetchall()

    return render_template('user_list.html', rows = rows, name = name)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        #Create an instance of class database 
        conn = WarehouseDB('warehouse.db')
        #Create connection to DB
        conn1 = conn.create_connection()

        cur = conn1.cursor()
        cur.execute("DELETE from userLog WHERE ID = (?)", [id])
        conn1.commit()

    except:
        conn1.rollback()
    
    finally:
        conn.close_connection()
        return redirect('/admin/')

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        if request.form["submit"] == "Update":
            #Create an instance of class database 
            conn = WarehouseDB('warehouse.db')
            #Create connection to DB
            conn1 = conn.create_connection()
                
            name = request.form['Update-name']
            password1 = request.form['Update-psw']
            
            cur = conn1.cursor()
            cur.execute("UPDATE userLog SET nameUser = (?), password = (?) WHERE ID = (?)", (name, password1, escape(id)))
            conn1.commit()
            
            conn.close_connection()

            return redirect('/admin/')

    else:
        #Create an instance of class database 
        conn = WarehouseDB('warehouse.db')
        #Create connection to DB
        conn1 = conn.create_connection()
        
        cur = conn1.cursor()
        cur.execute("select * from userLog where ID = (?)", escape(id))
        row = cur.fetchone()

        return render_template('update.html', row = row) 

@app.route('/delete_trx/<int:id>/<name>')
def delete_trx(id = None, name = None):
    
    #Create an instance of class database 
    conn = WarehouseDB('warehouse.db')
    #Create connection to DB
    conn1 = conn.create_connection()

    cur = conn1.cursor()
    cur.execute("DELETE from trx WHERE ID = (?)", [id])
    conn1.commit()

    conn.close_connection()
    return redirect(url_for('checkPage', name = name))

@app.route('/update_trx/<int:id>/<name>', methods = ['POST', 'GET'])
def update_trx(id = None, name = None):
    if request.method == 'POST':
        if request.form["submit"] == "Update":
            #Create an instance of class database 
            conn = WarehouseDB('warehouse.db')
            #Create connection to DB
            conn1 = conn.create_connection()
                
            dname = request.form['Update-device']
            dnote = request.form['Update-note']
            
            cur = conn1.cursor()
            cur.execute("UPDATE trx SET Device_Name = (?), Note = (?) WHERE ID = (?)", (dname, dnote, id))
            conn1.commit()
            
            conn.close_connection()

            return redirect(url_for('checkPage', name = name))

        elif request.form["submit"] == "Cancel":
            return redirect(url_for('checkPage', name = name))

    else:
        #Create an instance of class database 
        conn = WarehouseDB('warehouse.db')
        #Create connection to DB
        conn1 = conn.create_connection()
        
        cur = conn1.cursor()
        cur.execute("select * from trx where ID = (?)", [id])
        row = cur.fetchone()
        print(row)
        return render_template('update_trx.html', row = row) 

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)

if(__name__) == "__main__":
    app.run(port=8080,debug=True)
    

