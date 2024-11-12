from flask import Flask, url_for, render_template, request, session
import random, string, json, os

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)


app.secret_key=os.environ["SECRET_KEY"]; #secret key, very secret, make a new one using python -c "import secrets; print(secrets.token_hex())" in cmd prompt
#stored in key.txt

with open("static/questions.json") as data:
        questions = json.load(data)

length = len(questions)

@app.route("/")
def render_start():
    session["Question"] = "0"
    
    emptyAnswers = []
    session["Answers"] = json.dumps(emptyAnswers)
    
    return render_template("start.html")

@app.route("/next", methods=["GET", "POST"])
def render_question():
    if session["Question"] is not None:
        qnum = int(session["Question"])
    else:
        return render_start()
    
    answers = json.loads(session["Answers"])
    
    
    q = questions[qnum]
    a1 = q["answers"][0]
    a2 = q["answers"][1]
    a3 = q["answers"][2]
    a4 = q["answers"][3]
    
    allAnswers = [a1, a2, a3, a4]
    
    
    
    
    
    if "answer" in request.form:
        answer = request.form["answer"]
    else:
        answer = "none"
    
    
    if "refresh-check" in request.form:
        refresh_check = request.form["refresh-check"]
        print(refresh_check)
    else:
        refresh_check = 0
    
    
    if not "start" in request.form:
        answers.append(answer)
    
    if int(refresh_check) == qnum:
        session["Question"] = str(qnum + 1)
        session["Answers"] = json.dumps(answers)
    else:
        print(str(qnum) + " same question")
        return render_template('question.html', question=q["question"], answers=allAnswers, questionNum=qnum)
    
    
    if (qnum + 1) >= length:
        score = checkScore(answers)
        return render_template("end.html", score=str(score[0]) + " / " + str(score[1]))
    
    
    
    q = questions[qnum + 1]
    a1 = q["answers"][0]
    a2 = q["answers"][1]
    a3 = q["answers"][2]
    a4 = q["answers"][3]
    
    allAnswers = [a1, a2, a3, a4]
    
    return render_template('question.html', question=q["question"], answers=allAnswers, questionNum=str(qnum + 1))




def question(qnum):
    q = questions[qnum]
    a1 = q["answers"][0]
    a2 = q["answers"][1]
    a3 = q["answers"][2]
    a4 = q["answers"][3]
    
    allAnswers = [a1, a2, a3, a4]
    
    return render_template('question.html', question=q["question"], answers=allAnswers)



def checkAnswer(questionIndex, givenAnswer):
    question = questions[questionIndex]
    rightAnswer = question["correct"]
    
    if givenAnswer == "none":
        return False
    
    return int(givenAnswer) == int(rightAnswer)




def checkScore(answers):
    right = 0
    total = 0
    result = []
    
    print(answers)
    
    for i in range(length - 1):
        total += 1
        if checkAnswer(i - 1, answers[i - 1]):
            right += 1
            
    
    result.append(right)
    result.append(total)
    
    return result
    
        
        
        



if __name__=="__main__":
    app.run(debug=True)
