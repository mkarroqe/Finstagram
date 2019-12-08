# Finstagram
the fake social network for the real databases class

# Getting Started:
Two pieces: MAMP, and Flask.
### Flask
1. Enter the virtual environment by running `source /venv/bin/activate` in the terminal.
2. `export FLASK_ENV=development`
<<<<<<< HEAD
3. `export FLASK_ENV=app.py`
=======
3. `export FLASK_APP=app.py`
>>>>>>> 6874b74248601afbb5e1fbff7903e521c2e1fff1
4. `python -m flask run`
You should see the following success message:
```bash
 * Serving Flask app "app"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
The above IP address is where your local website is hosted.

### MAMP
1. Start your MAMP server
2. Create the **finstagram** database with the following code:
```
CREATE TABLE Person(
    username VARCHAR(20), 
    password CHAR(64), 
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    bio VARCHAR(1000),
    PRIMARY KEY (username)
);

CREATE TABLE Friendgroup(
    groupOwner VARCHAR(20), 
    groupName VARCHAR(20), 
    description VARCHAR(1000), 
    PRIMARY KEY (groupOwner, groupName),
    FOREIGN KEY (groupOwner) REFERENCES Person(username)
);

CREATE TABLE Photo (
    photoID int AUTO_INCREMENT, 
    postingdate DATETIME,
    filepath VARCHAR(100),
    allFollowers Boolean,
    caption VARCHAR(100),
    photoPoster VARCHAR(20),
    PRIMARY KEY (photoID),
    FOREIGN KEY(photoPoster) REFERENCES Person(username)
);

CREATE TABLE Likes (
    username VARCHAR(20), 
    photoID int, 
    liketime DATETIME, 
    rating int,
    PRIMARY KEY(username, photoID), 
    FOREIGN KEY(username) REFERENCES Person(username),
    FOREIGN KEY(photoID) REFERENCES Photo(photoID)
);  


CREATE TABLE Tagged (
    username VARCHAR(20), 
    photoID int, 
    tagstatus Boolean, 
    PRIMARY KEY(username, photoID), 
    FOREIGN KEY(username) REFERENCES Person(username),
    FOREIGN KEY(photoID)REFERENCES Photo(photoID)
);              

CREATE TABLE SharedWith ( 
    groupOwner VARCHAR(20), 
    groupName VARCHAR(20), 
    photoID int, 
    PRIMARY KEY(groupOwner, groupName, photoID),
    FOREIGN KEY(groupOwner, groupName) REFERENCES Friendgroup(groupOwner, groupName), 
    FOREIGN KEY (photoID) REFERENCES Photo(photoID)
);

CREATE TABLE BelongTo (
    member_username VARCHAR(20), 
    owner_username VARCHAR(20),
    groupName VARCHAR(20), 
    PRIMARY KEY(member_username, owner_username, groupName), 
    FOREIGN KEY(member_username) REFERENCES Person(username),
    FOREIGN KEY(owner_username, groupName)REFERENCES Friendgroup(groupOwner, groupName)
);

CREATE TABLE Follow (
    username_followed VARCHAR(20), 
    username_follower VARCHAR(20), 
    followstatus Boolean,
    PRIMARY KEY(username_followed , username_follower),
    FOREIGN KEY(username_followed) REFERENCES Person(username),
    FOREIGN KEY(username_follower) REFERENCES Person(username)
);
```
