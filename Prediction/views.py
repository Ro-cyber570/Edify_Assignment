from pickle import FALSE
from django.shortcuts import render
import csv,io
from django.http import HttpResponse
from django.http import *
import pandas as pd
from django.contrib import messages
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from .models import Diabetes
import plotly.express as px

def index(request):
    df=pd.read_csv(r'C:\Users\G15-D560542WIN9W\Desktop\projects\DS_Project\Prediction\diabetes.csv')
    tb=df.to_html()
    list1=["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]
    x=df.columns
    y=df.Outcome
    #print(metrics.accuracy_score(y_test,y_pred))

    return HttpResponse(tb)
    #return HttpResponse("Hello, world. You're at the Prediction.")

# Create your views here.

def csv_upload(request):
	template="index.html"
	if request.method=="GET":
		return render(request,template)
	csv_file=request.FILES['file']
	if not csv_file.name.endswith('.csv'):
		messages.error(request,"Not a csv file")
	df=pd.read_csv(csv_file)
	target=request.POST.get("target",False)
	s=False
	for column in df.columns:
		if column==target:
			s=True
	list1=[]
	if s==True:
		for coloumn in df.columns:
			if coloumn==target:
				y=df[target]
			else:
				list1.append(coloumn)
		x=df[list1]
		X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
		n_neighbours=request.POST.get("n_neighbours",False)
		weights=request.POST.get("weights",False)
		knn = KNeighborsClassifier(n_neighbors=int(n_neighbours),weights=weights)
		knn.fit(X_train, y_train)
		y_pred=knn.predict(X_test)
		context={"accuracy":metrics.accuracy_score(y_test,y_pred)}
		y_score = knn.predict_proba(X_test)[:,1]

		fig = px.scatter(
   		X_test, x= 'Glucose', y="Insulin",
    	color=y_score, color_continuous_scale='RdBu',
    	symbol=y_test, symbol_map={'0': 'square-dot', '1': 'circle-dot'},
    	labels={'symbol': 'label', 'color': 'score of <br>first class'}
		)
		fig.update_traces(marker_size=12, marker_line_width=1.5)
		fig.update_layout(legend_orientation='h')
		context['graph']=fig.to_html()
		return render(request,template,context)
	else:
		context={"error":"Target value not valid"}
		return (request,template,context)


	
	


