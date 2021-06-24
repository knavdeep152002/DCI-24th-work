from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd
import numpy as np


app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))



@app.route("/")
def home():
    return render_template("home.html")

def fun(index):
    if index==0:
        return "A"
    elif index==1:
        return "B"
    else:
        return "C"


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        a = []
        a.append(float(request.form["Total Income"]))
        a.append(float(request.form["Total Expenses"]))
        a.append(float(request.form["Target amount"]))
        a.append(float(request.form["surplus/defeciet"]))
        a.append(float(request.form["contributed margin"]))
        a.append(float(request.form["break even point"]))
        a.append(float(request.form["margin of safety%"]))
        a.append(float(request.form["margin of safety ₹"]))
        a.append(float(request.form["Investable Amount%"]))
        a.append(float(request.form["Investable amount"]))
        a.append(float(request.form["Target return %"]))
        a.append(float(request.form["buffer amount"]))
        x = request.form["risk abbility"]
        if x=="High":
            a.extend([0.0,0.0])
        elif x=="Medium":
            a.extend([0.0,1.0])
        else:
            a.extend([1.0,0.0])
        x = request.form["financial stability"]
        if x=="High":
            a.extend([0.0,0.0])
        elif x=="Medium":
            a.extend([0.0,1.0])
        else:
            a.extend([1.0,0.0])
        x = request.form["risk willingness"]
        if x=="High":
            a.extend([0.0,0.0])
        elif x=="Medium":
            a.extend([0.0,1.0])
        else:
            a.extend([1.0,0.0])
        x = request.form["total risk ability"]
        if x=="High":
            a.extend([0.0,0.0])
        elif x=="Medium":
            a.extend([0.0,1.0])
        else:
            a.extend([1.0,0.0])
        x = request.form["total risk"]
        if x=="High":
            a.extend([0.0,0.0])
        elif x=="Medium":
            a.extend([0.0,1.0])
        else:
            a.extend([1.0,0.0])
        
        prediction = model.predict([a])
        
        values = [9.28,9.78,9.87,10.89,10.85,11.19,15.73,19.45,19.41]

        difference_array = np.absolute(values-prediction*100)
        index = difference_array.argmin()
        # print(index)
        plan = index//3
        if plan==0:
            out = "LOW {}({}) ".format(fun(index%3),values[index]) 
        elif plan==1:
            out = "MEDIUM {}({}) ".format(fun(index%3),values[index])
        else:
            out = "HIGH {}({}) ".format(fun(index%3),values[index])
        for i in a:
            print(i)

        return render_template('index.html',prediction_text=out,pred = "{}".format(prediction*100))

    # print("HELLO")
    return render_template('index.html',prediction_text="none")




if __name__ == "__main__":
    app.debug = True
    app.run()
