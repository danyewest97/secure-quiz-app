from flask import Flask, url_for, render_template, request
import random, string, json, os

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)



@app.route("/")
def render_start():
    print(getQuestion(0))
    return render_template('start.html')

# @app.route("/nextquestion")
# def render_start():
    # return render_template('question.html')



def getQuestion(index):
    with open("static/questions.json") as data:
        questions = json.load(data)
    
    return questions[index]


if __name__=="__main__":
    app.run(debug=True)
