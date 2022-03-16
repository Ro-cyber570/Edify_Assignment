from http.client import HTTPResponse
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
import json

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
	n_neighbours=request.POST.get("n_neighbours",False)
	weights=request.POST.get("weights",False)
	s=False
	for column in df.columns:
		if column==target:
			s=True
	if s==True:
		list1=[]
		for coloumn in df.columns:
			if coloumn==target:
				y=df[target]
			else:
				list1.append(coloumn)
		x=df[list1]
		X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
		knn = KNeighborsClassifier(n_neighbors=int(n_neighbours),weights=weights)
		knn.fit(X_train, y_train)
		y_pred=knn.predict(X_test)
		context={"accuracy":metrics.accuracy_score(y_test,y_pred),"usedcols":list1}
		list2=request.POST.getlist("checks[]")
		if len(list2)>1:
			x=df[list2]
			X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
			knn = KNeighborsClassifier(n_neighbors=int(n_neighbours),weights=weights)
			knn.fit(X_train, y_train)
			y_pred=knn.predict(X_test)
			context={"accuracy":metrics.accuracy_score(y_test,y_pred),"usedcols":list2}
			return render(request,template,context)
		return render(request,template,context)
		
			
	#else:
	#	list1=request.POST.getlist("checks[]")
	#	csv_file=request.FILES['file']
	#	df=pd.read_csv(csv_file)
	#	x=df[list1]
	#	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
	#	knn = KNeighborsClassifier(n_neighbors=int(n_neighbours),weights=weights)
	##	y_pred=knn.predict(X_test)
	#	context={"accuracy":metrics.accuracy_score(y_test,y_pred),"usedcols":list1}
	#	return render(request,template,context)



	
	


