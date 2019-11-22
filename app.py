from flask import Flask, render_template,  request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='%0Q4xK^pBV88B!5%n83nGKCo$2rK9QIATTUmqpB0X24IfX!e#H',
                       db='finstagram',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    print("Hey!")
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    bio = request.form['bio']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        cursor.close()
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstname, lastname, bio))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/home')
def home():
    user = session['username']
    cursor = conn.cursor()
    query = '''SELECT photoID ,photoPoster, firstName, lastName, filepath, postingDate, caption FROM 
    Photo JOIN Person ON Person.username = Photo.photoPoster WHERE (photoPoster = %s  AND allFollowers = 1) OR photoPoster IN (SELECT username_followed AS photoPoster FROM Follow WHERE username_follower = %s AND followstatus=1) ORDER BY postingDate DESC '''
    # query = "SELECT * FROM Photo WHERE photoPoster = %s ORDER BY postingDate DESC"
    cursor.execute(query, (user, user))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=user, photos=data)

@app.route('/full_photo_info', methods=['GET', 'POST'])
def fullPhotoInfo():
    user = session['username']
    photoID = request.form["photoID"]
    cursor = conn.cursor()
    query = '''SELECT photoID ,photoPoster, firstName, lastName, filepath, postingDate, caption FROM 
    Photo JOIN Person ON Person.username = Photo.photoPoster WHERE photoID=%s'''
    # query = "SELECT * FROM Photo WHERE photoPoster = %s ORDER BY postingDate DESC"
    cursor.execute(query, (photoID))
    data = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()
    query2 = "SELECT username, rating FROM likes WHERE photoID = %s"
    cursor.execute(query2, (photoID))
    likeData = cursor.fetchall()
    cursor.close()
    return render_template('full_photo_info.html', username=user, photo=data, likes = likeData)

@app.route('/post_page')
def postPage():
    return render_template('post_page.html')

@app.route('/follow', methods=['GET', 'POST'])
def follow():
    user = session['username']
    followee = request.form["username"]
    cursor = conn.cursor()
    ins = "INSERT INTO Follow VALUES( %s, %s, %s)"
    cursor.execute(ins, (followee,user, 0))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/follow_accept', methods=['GET', 'POST'])
def followAccept():
    user = session['username']
    follower = request.form["follower"]
    cursor = conn.cursor()
    ins = "UPDATE Follow SET followstatus=1 WHERE username_followed = %s AND username_follower = %s"
    cursor.execute(ins, (user, follower))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/follow_requests', methods=['GET', 'POST'])
def followRequests():
    user = session['username']
    cursor = conn.cursor()
    ins = "SELECT * FROM Follow WHERE username_followed = %s AND followstatus != 1"
    cursor.execute(ins, (user))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("follow_requests.html", requests = data)

@app.route('/post_photo', methods=['GET', 'POST'])
def postPhoto():
    user = session['username']
    filepath = request.form["filepath"]
    caption = request.form["caption"]
    if "allFollowers" in request.form:
        allFollowers = 1
    else:
        allFollowers = 0
    print("All Followers val: "+ str(allFollowers))

    cursor = conn.cursor()
    ins = "INSERT INTO Photo (postingDate, filepath, allFollowers, caption, photoPoster) VALUES( %s, %s, %s, %s, %s)"
    cursor.execute(ins, (datetime.now().isoformat(),filepath, allFollowers, caption, user))
    conn.commit()
    cursor.close()
    return render_template('home.html', username=user)



app.secret_key = '57902857h20398572h034fj059jf832457h24'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)