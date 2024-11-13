from flask import Flask, url_for, render_template, request, session, redirect
import random, string, json, os, time

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
    
    session["Done"] = "false"
    
    session["Time"] = 0
    session["StartTime"] = time.time()
    
    return render_template("start.html")

@app.route("/next", methods=["GET", "POST"])
def render_question():
    if not "Question" in session:
        return redirect("/")
    
    
    if not session["Done"] == "true":
        currTime = time.time()
        diff = (currTime - int(session["StartTime"])) * 1000
        session["Time"] = str(diff)
    else:
        diff = int(float(session["Time"]))
    
    
    if session["Question"] is not None:
        qnum = int(session["Question"])
    else:
        return render_start()
    
    
    answers = json.loads(session["Answers"])
    
    
    if session["Done"] == "true":
        score = checkScore(answers)
        return render_template("end.html", score=str(score[0]) + " / " + str(score[1]), questionsScore=qScore(answers), qLength=(length-1), startTime=int(diff))
    
    
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
    else:
        refresh_check = 0
    
    
    if not "start" in request.form:
        print(answer)
        answers.append(answer)
        print(answers)
    
    
    
    if int(refresh_check) == qnum:
        session["Question"] = str(qnum + 1)
        session["Answers"] = json.dumps(answers)
    else:
        return render_template('question.html', question=q["question"], answers=allAnswers, questionNum=qnum, qLength=str(length - 1), startTime=int(diff))
    
    
    if (qnum + 1) >= length:
        score = checkScore(answers)
        session["Done"] = "true"
        return render_template("end.html", score=str(score[0]) + " / " + str(score[1]), questionsScore=qScore(answers), qLength=(length-1), startTime=int(diff))
    
    
    q = questions[qnum + 1]
    a1 = q["answers"][0]
    a2 = q["answers"][1]
    a3 = q["answers"][2]
    a4 = q["answers"][3]
    
    allAnswers = [a1, a2, a3, a4]
    
    return render_template('question.html', question=q["question"], answers=allAnswers, questionNum=str(qnum + 1), qLength=str(length - 1), startTime=int(diff))



def checkAnswer(questionIndex, givenAnswer):
    question = questions[questionIndex]
    rightAnswer = question["correct"]
    
    print(givenAnswer)
    
    if givenAnswer == "none":
        return False
    
    return int(givenAnswer) == int(rightAnswer)




def checkScore(answers):
    right = 0
    total = 0
    result = []
    
    
    for i in range(length - 1):
        total += 1
        if checkAnswer(i, answers[i]):
            right += 1
            
    
    result.append(right)
    result.append(total)
    
    return result
    
        
def qScore(answers):
    result = []
    answers = json.loads(session["Answers"])
    
    for i in range(length - 1):
        if checkAnswer(i, answers[i]):
            result.append("Correct")
        else:
            result.append("Incorrect")
    
    
    return result        
        



if __name__=="__main__":
    app.run(debug=True)











# Question Template for json file:

# ,
	# {
		# "question":"question_template",
		# "answers":["answer_a", "answer_b", "answer_c", "answer_d"],
		# "correct":0
	# }