from flask import Flask, url_for, render_template, request
import random, string

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)



@app.route("/")
def render_start():
    return render_template('start.html')




if __name__=="__main__":
    app.run(debug=True)
