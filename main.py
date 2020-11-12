import pickle
import re
import string

from flask import Flask, render_template, request, redirect
# import mysql.connector
from nltk import word_tokenize, WordNetLemmatizer, pos_tag

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


@app.route('/', methods=["GET", "POST"])
def predict():
    if request.method == 'POST':
        data = request.form['comment']
        print("Data")
        custom_tokens = remove_noise(word_tokenize(data))
        response = model.classify(dict([token, True] for token in custom_tokens))
        return render_template("senti.html", comment=data, response=response)
    else:
        return render_template("senti.html", comment="Try writing a comment.", response="Response shown here")


app.run(debug=True)
