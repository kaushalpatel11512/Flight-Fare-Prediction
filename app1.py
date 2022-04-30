
from datetime import date
from distutils.log import debug
from importlib.machinery import SourceFileLoader
from flask import Flask
from flask import request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd


print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
app =  Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

@app.route("/predict",methods = ["Get","Post"])
@cross_origin()
def predict():
    if request.method == "POST":

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        date_dep = request.form["Dep_Time"]
        Journey_date = int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").month)

        Dep_hour = int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").minute)


        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr,format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr,format="%Y-%m-%dT%H:%M").minute)

        dur_hour = abs(Arrival_hour-Dep_hour)
        dur_min = abs(Arrival_min-Dep_min)

        Total_stops = int(request.form["stops"])

        

        Airline = request.form['airline']

        if(Airline=='Jet Airways'):
            airline=4

        elif (Airline=='IndiGo'):
            airline=3
        
        elif (Airline=='Air India'):
            airline=1
        
        elif (Airline=='Multiple carriers'):
            airline=6
        
        elif (Airline=='SpiceJet'): 
            airline=8

        elif (Airline=='Vistara'): 
            airline=10

        elif (Airline=='Air Asia'): 
            airline=0

        elif (Airline=='GoAir'): 
            airline=2

        elif (Airline=='Multiple carriers Premium economy'): 
            airline=7

        elif (Airline=='Jet Airways Business'): 
            airline=5

        elif (Airline=='Vistara Premium economy'): 
            airline=11
        
        else :
            return 0

        
        Source = request.form['Source']
        
        if(Source=='Delhi'):
            Source = 2

        elif(Source=='Kolkata'):
            Source = 3
        
        elif(Source=='Banglore'):
            Source = 0
        
        elif(Source=='Mumbai'):
            Source = 4

        elif(Source=='Chennai'):
            Source = 1
        
        else :
            return 0
        
        destinationfinal = request.form['Destination']

        if(destinationfinal =='Cochin'):
            destination = 1

        elif(destinationfinal =='Banglore'):
            destination = 0
        
        elif(destinationfinal =='Delhi'):
            destination = 2
        
        elif(destinationfinal =='New Delhi'):
            destination = 5

        elif(destinationfinal =='Hyderabad'):
            destination = 3

        elif(destinationfinal =='Kolkata'):
            destination = 4
        else :
            return 0
        
        prediction = model.predict([[Total_stops,
        Journey_date,Journey_month,Dep_hour,Dep_min,
        Arrival_hour,Arrival_min,dur_hour,dur_min,
        Source,destination,airline]])


        print("___________________________________________________")
        print(prediction[0])

        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your fllllight price is {} INR".format(output))
    
    return render_template("home.html")


    
print("##########################")

if __name__ == "__main__":
    app.run(debug=True)

