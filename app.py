from flask import Flask, render_template,  request, session, url_for, redirect, send_file
import os
import uuid
import hashlib
import pymysql.cursors
from datetime import datetime
from functools import wraps
import time

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

conn = pymysql.connect(host='localhost',
                       port = 20001,
                       user='root',
                       password='root',
                       db='finstagram',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return dec

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("index.html")

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
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()

        with conn.cursor() as cursor:
            query = "SELECT * FROM person WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashedPassword))
        data = cursor.fetchone()
        if data:
            session["username"] = username
            return redirect(url_for("home"))

        error = "Incorrect username or password."
        return render_template("login.html", error=error)

    error = "An unknown error has occurred. Please try again."
    return render_template("login.html", error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()
        firstName = requestData["firstName"]
        lastName = requestData["lastName"]
        
        try:
            with conn.cursor() as cursor:
                query = "INSERT INTO person (username, password, firstName, lastName) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, hashedPassword, firstName, lastName))
        except pymysql.err.IntegrityError:
            error = "%s is already taken." % (username)
            return render_template('register.html', error=error)    

        return redirect(url_for("login"))

    error = "An error has occurred. Please try again."
    return render_template("register.html", error=error)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username")
    return redirect("/")

@app.route('/home')
@login_required
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
@login_required
def fullPhotoInfo():
    user = session['username']
    photoID = request.form["photoID"]
    cursor = conn.cursor()
    query = '''SELECT photoID ,photoPoster, firstName, lastName, filepath, postingDate, caption FROM 
    Photo JOIN Person ON Person.username = Photo.photoPoster WHERE photoID=%s'''
    # query = "SELECT * FROM Photo WHERE photoPoster = %s ORDER BY postingDate DESC"
    cursor.execute(query, (photoID))
    data = cursor.fetchone()
<<<<<<< HEAD
    
    query2 = "SELECT username, rating FROM likes WHERE photoID = %s"
    cursor.execute(query2, (photoID))
    likeData = cursor.fetchall()
    
    query3 = 'SELECT username FROM tagged WHERE photoID = %s'
    cursor.execute(query3, photoID)
    tagData = cursor.fetchall()
 
    return render_template('full_photo_info.html', username=user, photo=data, likes = likeData, tagged_users=tagData)
=======
    cursor.close()
    cursor = conn.cursor()
    query2 = "SELECT username, rating FROM likes WHERE photoID = %s"
    cursor.execute(query2, (photoID))
    likeData = cursor.fetchall()
    cursor.close()
    print(user)
    print(data)
    print(likeData)
    return render_template('full_photo_info.html', username=user, photo=data, likes = likeData)
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1

@app.route('/post_page')
@login_required
def postPage():
    return render_template('post_page.html')

@app.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    user = session['username']
    followee = request.form["username"]
    cursor = conn.cursor()
    ins = "INSERT INTO Follow VALUES( %s, %s, %s)"
    cursor.execute(ins, (followee,user, 0))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    user = session['username']
    photoID = request.form["photoID"]
    rating = request.form["rating"]
    cursor = conn.cursor()
    ins = ("INSERT INTO Likes VALUES( %s, %s, %s, %s)")
    cursor.execute(ins, (user,photoID, datetime.now().isoformat(), rating))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))
<<<<<<< HEAD

@app.route('/tag', methods=['GET', 'POST'])
@login_required
def tag(tagged = None):
    if (tagged == None):
	    tagged = request.form['tagged']
    user = session['username']
    getID = "SELECT max(photoID) FROM Photo"
    cursor = conn.cursor()
    cursor.execute(getID,)
    photoID = cursor.fetchone()
    taggedUsers = tagged.split(",")
    ins = ("INSERT INTO Tagged VALUES( %s, %s, %s)")
    for user in taggedUsers:  
        sanatizedUser = user.strip()
        cursor.execute(ins, (sanatizedUser,photoID[max(photoID)], 0))
=======
    
@app.route('/tag', methods=['GET', 'POST'])
@login_required
def tag():
    user = session['username']
    tagged = request.form["tagged"]
    photoID = request.form["photoID"]
    taggedUsers = tagged.split(",")
    cursor = conn.cursor()
    ins = ("INSERT INTO Tagged VALUES( %s, %s, %s)")
    for user in taggedUsers:  
        sanatizedUser = user.replace(" ","")
        cursor.execute(ins, (sanatizedUser,photoID, 0))
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1
        conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/follow_accept', methods=['GET', 'POST'])
@login_required
def followAccept():
    user = session['username']
    follower = request.form["follower"]
    cursor = conn.cursor()
    ins = "UPDATE Follow SET followstatus=1 WHERE username_followed = %s AND username_follower = %s"
    cursor.execute(ins, (user, follower))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/tag_accept', methods=['GET', 'POST'])
@login_required
def tagAccept():
    user = session['username']
<<<<<<< HEAD
    photoID = request.form['photoID']
    cursor = conn.cursor()
    ins = "UPDATE tagged SET tagStatus=1 WHERE username= %s AND photoID = %s"
=======
    photoID = request.form["photoID"]
    cursor = conn.cursor()
    ins = "UPDATE Tagged SET tagstatus=1 WHERE username= %s AND photoID = %s"
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1
    cursor.execute(ins, (user, photoID))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/follow_requests', methods=['GET', 'POST'])
@login_required
def followRequests():
    user = session['username']
    cursor = conn.cursor()
    ins = "SELECT * FROM Follow WHERE username_followed = %s AND followstatus != 1"
    cursor.execute(ins, (user))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("follow_requests.html", requests = data)

@app.route('/tag_requests', methods=['GET', 'POST'])
@login_required
def tagRequests():
<<<<<<< HEAD
    user = session['username']
    cursor = conn.cursor()
    ins = "SELECT username, Photo.photoID, photoPoster, filepath FROM Tagged JOIN Photo ON Photo.photoID = Tagged.photoID WHERE username = %s AND tagstatus != 1"
=======
    # NOT FINISHED
    user = session['username']
    cursor = conn.cursor()
    ins = "SELECT username, photoID, photoPoster, filepath FROM Tagged WHERE username = %s AND tagstatus != 1 JOIN Photo ON Photo.photoID = Tagged.photoID"
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1
    cursor.execute(ins, (user))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
<<<<<<< HEAD
    return render_template("tag_requests.html", requests = data)
=======
    return render_template("check_tagged.html", requests = data)
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1

@app.route('/post_photo', methods=['GET', 'POST'])
@login_required
def postPhoto():
    user = session['username']

    ROOT = "static/css/imgs/posts/"
    filepath = ROOT + request.form["filepath"]

    caption = request.form["caption"]
<<<<<<< HEAD
    tagged = request.form["tagged"]
=======
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1
    time = datetime.now().isoformat()
    if "allFollowers" in request.form:
        allFollowers = 1
    else:
        allFollowers = 0
    print("All Followers val: "+ str(allFollowers))
    cursor = conn.cursor()
    ins = "INSERT INTO Photo (postingDate, filepath, allFollowers, caption, photoPoster) VALUES( %s, %s, %s, %s, %s)"
    cursor.execute(ins, (time,filepath, allFollowers, caption, user))
    conn.commit()
    cursor.close()
    if (tagged):
        tag(tagged)
    return redirect(url_for('home'))

<<<<<<< HEAD
@app.route('/newGroup', methods = ['GET', 'POST'])
@login_required
def newGroup():
	user = session['username']
	groupName = request.form['groupName']
	description = request.form['description']
	member_list = request.form['members']
	member_list = member_list.split(",")
	cursor = conn.cursor()
	query = 'SELECT username_followed FROM follow WHERE username_follower = %s'
	cursor.execute(query, user)
	follows = cursor.fetchall()
	follow_list = []
	for members in follows:
		follow_list.append(members["username_followed"])
	print(follow_list)
	cursor.close()
	for member in member_list:
		print(member)
		if member.strip() not in follow_list:
			error = "You do not follow " + member.strip()
			return render_template("friendGroups.html", error = error)
	query = "INSERT INTO belongTo (member_username, owner_username, groupName) VALUES( %s, %s, %s)"
	for member in member_list:
		cursor = conn.cursor()
		cursor.execute(query, (member, user, groupName))
		conn.commit()
		cursor.close()
	cursor = conn.cursor()
	ins = 'INSERT INTO friendgroup (groupOwner, groupName, description) VALUES (%s, %s, %s)'
	cursor.execute(ins, (user, groupName, description))
	conn.commit()
	cursor.close()
	return render_template("friendGroups.html", error = None)
	
	
@app.route('/friendGroups', methods=['GET', 'POST'])
@login_required
def seeFriendGroup():
	user = session['username']
	cursor = conn.cursor()
	query = 'SELECT DISTINCT groupName FROM belongTo WHERE ((member_username = %s) OR (owner_username = %s)) ORDER BY groupName ASC'
	cursor.execute(query, (user, user))
	groups = cursor.fetchall()
	cursor.close()
	for curr in groups:
		cursor = conn.cursor()
		curr_query = 'SELECT member_username FROM belongTo WHERE groupName = %s'
		cursor.execute(curr_query, curr["groupName"])
		curr["members"] = []
		for member in cursor:
			curr["members"].append(member["member_username"])
		cursor.close()
	return render_template('friendGroups.html', groups = groups) 
	#returns a list of dictionaries. Each dictionary contains "groupName" (which is a string) and "members" (which is a list)


=======
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1
app.secret_key = '57902857h20398572h034fj059jf832457h24'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)