from flask import Flask, url_for, render_template, request, make_response
import random, string, json, os

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)


app.secret_key=os.environ["SECRET_KEY"]; #secret key, very secret, make a new one using python -c "import secrets; print(secrets.token_hex())" in cmd prompt
#stored in key.txt

with open("static/questions.json") as data:
        questions = json.load(data)

length = len(questions)

@app.route("/")
def render_start():
    # Making a response with cookies
    resp = make_response(render_template('start.html'))
    resp.set_cookie("Question", "0")
    
    emptyAnswers = []
    resp.set_cookie("Answers", json.dumps(emptyAnswers))
    
    return resp

@app.route("/next", methods=["GET", "POST"])
def render_question():
    if  request.cookies.get("Question") is not None:
        qnum = int(request.cookies.get("Question"))
    else:
        return render_start()
    
    resp = make_response(question(qnum))
    
    try:
        answer = request.form["answer"]
    except:
        answer = "none"
    
    answers = json.loads(request.cookies.get("Answers"))
    
    if qnum != 0:
        answers.append(answer)
    
    
    resp.set_cookie("Question", str(qnum + 1))
    resp.set_cookie("Answers", json.dumps(answers))
    
    
    if (qnum + 1) >= length:
        score = checkScore(answers)
        return render_template("end.html", score=str(score[0]) + " / " + str(score[1]))
    
    return resp




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
