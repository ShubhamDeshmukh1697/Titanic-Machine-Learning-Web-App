# Create your views here.
from django.shortcuts import render
import pickle
from predict.models import Predictions
from django.core.paginator import Paginator

curId = 0

def home(request):
    return render(request, 'index.html')
    
def getPredictions(name,sex,age,fare,family,C,Q,S):
    global curId
    if sex==1:
        g="Male"
    else:
        g = "Female"
    model = pickle.load(open("titanic_survival_model.sav", "rb"))
    scaled = pickle.load(open("scaler.sav", "rb"))
    prediction = model.predict(scaled.transform([[sex, age, fare, family, C, Q, S]]))
    if C==1:
        emb = "Cherbourg"
    elif(Q==1):
        emb= "Queenstown"
    else:
        emb = "Southampton"

    if prediction == 0:
        obj = Predictions(name=name, gender=g, age=age, fare=fare, family_cnt=family,Embarked=emb,prediction="Not Survived")
        obj.save()
        curId = obj.pid
        return "not survived"
    elif prediction == 1:
        obj = Predictions(name=name, gender=g, age=age, fare=fare, family_cnt=family,Embarked=emb,prediction="Survived")
        obj.save()
        curId = obj.pid
        return "survived"
    else:
        return "error"

def result(request):
    C=0
    Q=0
    S = 0
    #Name Sex	Age Fare Family Embarked from(C,Q,S)
    name = request.GET['Name']
    sex = int(request.GET['Gender'])
    age = int(request.GET['Age'])
    fare = int(request.GET['Fare'])
    family = int(request.GET['Family'])
    embarked = request.GET['Embarked']
    if embarked == "C":
        C=1
    elif(embarked == "Q"):
        Q=1
    else:
        S=1

    # call function
    result = getPredictions(name,sex,age,fare,family,C,Q,S)
    
    # all predictions
    preds = Predictions.objects.all().order_by('-predicted_date')
    count = len(preds)
    p = Paginator(preds, 8)
    print(p.num_pages)
    
    # survived and not survived objects
    surv_cnt = len(Predictions.objects.filter(prediction = "Survived"))
    nsurv_cnt = len(Predictions.objects.filter(prediction = "Not Survived"))
    return render(request , 'result.html',{'preds':preds,'curId':curId,'count':count,'surv_cnt':surv_cnt,'nsurv_cnt':nsurv_cnt})

