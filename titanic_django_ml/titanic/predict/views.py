# Create your views here.
from django.shortcuts import render
import pickle
from predict.models import Predictions
from django.core.paginator import Paginator,EmptyPage , PageNotAnInteger
import math

curId = 0

def home(request):
    return render(request, 'index.html')
    
def search(request):
    query = request.GET['search']
    
    allPredsPred = Predictions.objects.filter(prediction__iexact = query)
    allPredsName = Predictions.objects.filter(name__icontains = query)
    allPredsGender = Predictions.objects.filter(gender__iexact = query)
    allPredsLoc = Predictions.objects.filter(Embarked__icontains = query)
    allPredsId = Predictions.objects.filter(pid__iexact = query)
    
    allPreds = allPredsPred.union(allPredsName,allPredsGender,allPredsLoc,allPredsId)
    count = len(allPreds)
    surv_cnt = 0
    nsurv_cnt = 0
    for i in allPreds:
        if i.prediction == "Survived":
            surv_cnt += 1
        else:
            nsurv_cnt += 1

    print(surv_cnt,nsurv_cnt) 
    
    return render(request , 'search.html',{'allPreds':allPreds,'count':count,'surv_cnt':surv_cnt,'nsurv_cnt':nsurv_cnt})
    
def getPredictions(name,sex,age,fare,family,C,Q,S):
    global curId
    if sex==1:
        g="Male"
    else:
        g = "Female"
    model = pickle.load(open("titanic_survival_model.sav", "rb"))
    scaled = pickle.load(open("scaler.sav", "rb"))

    # predicition after scaling of values
    prediction = model.predict(scaled.transform([[sex, age, fare, family, C, Q, S]]))
    print("scaled values are: ",scaled.transform([[sex, age, fare, family, C, Q, S]]))

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

    """# PAGINATION
    p = Paginator(preds, 8)
   
    page_num = request.GET.get('page',1)
    try:
        page=p.page(page_num)
    except EmptyPage:
        page = p.page(1)    
    """

    # survived and not survived objects
    surv_cnt = len(Predictions.objects.filter(prediction = "Survived"))
    nsurv_cnt = len(Predictions.objects.filter(prediction = "Not Survived"))
    surv_cnt_per = (surv_cnt*100)/count
    surv_cnt_per = round(surv_cnt_per,2)
    nsurv_cnt_per = (nsurv_cnt*100)/count
    nsurv_cnt_per = round(nsurv_cnt_per,2)
    context ={
        'preds':preds,
        'curId':curId,
        'count':count,
        'surv_cnt':surv_cnt,
        'nsurv_cnt':nsurv_cnt,
        'nsurv_cnt_per':nsurv_cnt_per,
        'surv_cnt_per':surv_cnt_per,
        }
    return render(request , 'result.html',context)

def predictions(request):
    allpreds = Predictions.objects.all()
    count = len(allpreds)
    surv_cnt = len(Predictions.objects.filter(prediction = "Survived"))
    nsurv_cnt = len(Predictions.objects.filter(prediction = "Not Survived"))
    
    paginator = Paginator(allpreds, 8)
    page1 = paginator.page(1)
    for i in page1:
        print(i)
    print("page 1 content" ,page1.object_list)

    page_num = request.GET.get('page',1)
    print("get page number is:",page_num)
    try:
        preds = paginator.page(page_num)
    except EmptyPage:
        preds = paginator.page(2)
    except PageNotAnInteger:
        preds = paginator.page(1)


    context = {
        # 'page': page,
        'preds':preds,
        'surv_cnt':surv_cnt,
        'nsurv_cnt':nsurv_cnt,
        'count':count,
        }
    return render(request ,'predictions.html',context)