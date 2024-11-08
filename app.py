from flask import Flask, url_for, render_template, request
import random, string, json, os

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)


app.secret_key=os.environ["SECRET_KEY"]; #secret key, very secret, make a new one using python -c "import secrets; print(secrets.token_hex())" in cmd prompt
#stored in key.txt

@app.route("/")
def render_start():
    return render_template('start.html')

@app.route("/next")
def render_start():
    return render_template('question.html')







def checkAnswer(questionIndex, givenAnswer):
    question = getQuestion(questionIndex)
    rightAnswer = question["correct"]
    
    return givenAnswer == rightAnswer


def getQuestion(index):
    with open("static/questions.json") as data:
        questions = json.load(data)
    
    return questions[index]





if __name__=="__main__":
    app.run(debug=True)
