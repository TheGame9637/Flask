from flask import Flask, render_template, request, redirect
# import mysql.connector
from nltk import word_tokenize

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def predict():


if __name__=='__main__':
    app.run(debug=True)
