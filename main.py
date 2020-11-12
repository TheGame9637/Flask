from flask import Flask, render_template, request, redirect
import mysql.connector
from nltk import word_tokenize

import sentiment_analysys as sn

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="studentnewdatabase"
)
app = Flask(__name__)

mycursor = mydb.cursor()


@app.route('/')
def hello_world():
    mycursor.execute("SELECT * FROM student")
    studentData = mycursor.fetchall()
    return render_template('index.html', data=studentData)


@app.route('/data', methods=["GET", "POST"])
def uploadData():
    error = ''
    try:
        if request.method == "POST":
            sql = "INSERT INTO student (Name, Division, Roll) VALUES (%s, %s , %s)"
            val = (request.form['NameOfStudent'], request.form['GrOfStudent'], request.form['RollOfStudent'])
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        return redirect('/')

    except Exception as e:
        return render_template("index.html")


classifier = sn.trainModel()


@app.route('/senti', methods=["GET", "POST"])
def analysis():
    if request.method == "POST":
        custom_tweet = request.form['comment']
        custom_tokens = sn.remove_noise(word_tokenize(custom_tweet))
        print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
        return render_template("SentimentAnalysys.html",
                               response=classifier.classify(dict([token, True] for token in custom_tokens)),
                               comment=custom_tweet)
    else:
        return render_template("SentimentAnalysys.html", response="None", comment="Try entering a a comment")


app.run(debug=True)
