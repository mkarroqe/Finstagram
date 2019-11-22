from flask import Flask, render_template,  request, session, url_for, redirect
import pymysql.cursors

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

app.secret_key = '57902857h20398572h034fj059jf832457h24'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)