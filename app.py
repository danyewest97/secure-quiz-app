from flask import Flask, url_for, render_template, request
import random, string, main

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

states = main.get_state_options()

@app.route("/")
def render_home():
    return render_template('home.html')
    
@app.route("/turbines")
def render_turbines():
    return render_template('turbines.html', options=states)

@app.route("/turbineform")
def render_turbine_form():
    state = request.args["state"]
    if state == "<none>":
        data = main.get_data("Turbine", request.args["key"], request.args["highlow"])
        keyString = str(request.args["key"]).lower()
        keyString = keyString.replace("_", " ")
        if request.args["highlow"] == "average":
            return render_template('turbines.html', response=data, keyhighlow="The average " + keyString + " of all turbines in the US is: ", options=states)
        else:
            return render_template('turbines.html', response=main.turbineToString(data), keyhighlow="Here is the info on the turbine with the " + request.args["highlow"] + "est " + keyString + ": ", options=states)

    else:
        data = main.get_data_by_state("Turbine", request.args["key"], request.args["highlow"], state)
        keyString = str(request.args["key"]).lower()
        keyString = keyString.replace("_", " ")
        if request.args["highlow"] == "average":
            return render_template('turbines.html', response=data, keyhighlow="The average " + keyString + " of all turbines in " + state + " is: ", options=states)
        else:
            return render_template('turbines.html', response=main.turbineToString(data), keyhighlow="Here is the info on the turbine in " + state + " with the " + request.args["highlow"] + "est " + keyString + ": ", options=states)
    
    return null
    
@app.route("/projects")
def render_projects():
    return render_template('projects.html', options=states)

@app.route("/projectform")
def render_project_form():
    state = request.args["state"]
    if state == "<none>":
        data = main.get_data("Project", request.args["key"], request.args["highlow"])
        keyString = str(request.args["key"]).lower()
        keyString = keyString.replace("_", " ")
        if (keyString == "Number Turbines"):
            keyString == "Number of Turbines"
        if request.args["highlow"] == "average":
            return render_template('projects.html', response=(data), keyhighlow="The average " + keyString + " of all turbine projects in the US is: ", options=states)
        else:
            return render_template('projects.html', response=main.turbineToString(data), keyhighlow="Here is the info on one of the turbines in the project with the " + request.args["highlow"] + "est " + keyString + ": ", options=states)
    else:
        data = main.get_data_by_state("Project", request.args["key"], request.args["highlow"], state)
        keyString = str(request.args["key"]).lower()
        keyString = keyString.replace("_", " ")
        if (keyString == "Number Turbines"):
            keyString == "Number of Turbines"
        if request.args["highlow"] == "average":
            return render_template('projects.html', response=(data), keyhighlow="The average " + keyString + " of all turbine projects in " + state + "is: ", options=states)
        else:
            return render_template('projects.html', response=main.turbineToString(data), keyhighlow="Here is the info on one of the turbines in the project with the " + request.args["highlow"] + "est " + keyString + ": ", options=states)
    
    
    
@app.route("/locations")
def render_locations():
    # print(main.get_data_for_pie())
    return render_template('locations.html', options=states)

@app.route("/locationform")
def render_location_form():
    state = request.args["state"]
    if state == "<none>":
        return render_template('locations.html', options=states)
    else:
        data = main.get_state_data(state)
        return render_template('locations.html', options=states, response=data)

@app.route("/growth")
def render_growth():
    # print(main.get_data_for_bar())
    try:
        if request.args["state"] != "<none>":
            return render_template("growth.html", options=states, state=request.args["state"], data=main.get_state_data_for_bar(request.args["state"]))
        else:
            return render_template("growth.html", options=states, state="the US", data=main.get_data_for_bar())
    except:
        return render_template("growth.html", options=states, state="the US", data=main.get_data_for_bar())

if __name__=="__main__":
    app.run(debug=False)
