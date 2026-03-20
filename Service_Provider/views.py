
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse
import csv


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import CountVectorizer


from sklearn.tree import DecisionTreeClassifier
#model selection
from sklearn.metrics import confusion_matrix, accuracy_score,classification_report

# Create your views here.
from Remote_User.models import ClientRegister_Model,early_detection_of_human_diseases,early_detection_of_human_diseases1,detection_ratio,detection_accuracy


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            detection_accuracy.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def View_Prediction_Of_early_detection_of_human_Ratio(request):
    detection_ratio.objects.all().delete()
    rratio = ""
    kword = 'Not Detected'
    print(kword)
    obj = early_detection_of_human_diseases.objects.all().filter(Q(Prediction=kword))
    obj1 = early_detection_of_human_diseases.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Detected'
    print(kword1)
    obj1 = early_detection_of_human_diseases.objects.all().filter(Q(Prediction=kword1))
    obj11 = early_detection_of_human_diseases.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)


    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_early_detection_of_human_Ratio.html', {'objs': obj})

def Upload_Datasets(request):
    if "GET" == request.method:
        return render(request, 'SProvider/Upload_Datasets.html', {})
    else:

        early_detection_of_human_diseases1.objects.all().delete()

        csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            early_detection_of_human_diseases1.objects.create(
                Fid=row['Fid'],
                Age=row['Age'],
                Sex=row['Sex'],
                Bmi=row['BMI'],
                Fbg=row['Fasting_Blood_Glucose'],
                hbA1c=row['HbA1c'],
                Bps=row['Blood_Pressure_Systolic'],
                Bpd=row['Blood_Pressure_Diastolic'],
                Ct=row['Cholesterol_Total'],
                Ggt=row['GGT'],
                Su=row['Serum_Urate'],
                Pal=row['Physical_Activity_Level'],
                Dic=row['Dietary_Intake_Calories'],
                Ac=row['Alcohol_Consumption'],
                Ss=row['Smoking_Status'],
            )

    obj = early_detection_of_human_diseases1.objects.all()

    return render(request, 'SProvider/Upload_Datasets.html', {'csvdatasets': obj})

def View_All_Uploaded_Datasets(request):
    obj =early_detection_of_human_diseases1.objects.all()
    return render(request, 'SProvider/View_All_Uploaded_Datasets.html', {'csvdatasets': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = early_detection_of_human_diseases.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_Of_early_detection_of_human_diseases(request):
    obj =early_detection_of_human_diseases.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_early_detection_of_human_diseases.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Predicted_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Data.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = early_detection_of_human_diseases.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.Age, font_style)
        ws.write(row_num, 2, my_row.Sex, font_style)
        ws.write(row_num, 3, my_row.Bmi, font_style)
        ws.write(row_num, 4, my_row.Fbg, font_style)
        ws.write(row_num, 5, my_row.hbA1c, font_style)
        ws.write(row_num, 6, my_row.Bps, font_style)
        ws.write(row_num, 7, my_row.Bpd, font_style)
        ws.write(row_num, 8, my_row.Ct, font_style)
        ws.write(row_num, 9, my_row.Ggt, font_style)
        ws.write(row_num, 10, my_row.Su, font_style)
        ws.write(row_num, 11, my_row.Pal, font_style)
        ws.write(row_num, 12, my_row.Dic, font_style)
        ws.write(row_num, 13, my_row.Ac, font_style)
        ws.write(row_num, 14, my_row.Ss, font_style)
        ws.write(row_num, 15, my_row.Prediction, font_style)


    wb.save(response)
    return response

def train_model(request):
    detection_accuracy.objects.all().delete()
    df = pd.read_csv('Datasets.csv')

    def apply_response(Label):
        if (Label == 0):
            return 0  # Not Detected
        elif (Label == 1):
            return 1  # Detected

    df['results'] = df['Label'].apply(apply_response)

    X = df['Fid']
    y = df['results']

    cv = CountVectorizer()
    x = cv.fit_transform(X)


    models = []
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
    X_train.shape, X_test.shape, y_train.shape

    print("Artificial Neural Network (ANN)")

    from sklearn.neural_network import MLPClassifier
    mlpc = MLPClassifier().fit(X_train, y_train)
    y_pred = mlpc.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('MLPClassifier', mlpc))
    detection_accuracy.objects.create(names="Artificial Neural Network (ANN)",
                                      ratio=accuracy_score(y_test, y_pred) * 100)

    # SVM Model
    print("SVM")
    from sklearn import svm

    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print("ACCURACY")
    print(svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)

    print("Random Forest Classifier")
    from sklearn.ensemble import RandomForestClassifier
    rf_clf = RandomForestClassifier()
    rf_clf.fit(X_train, y_train)
    rfpredict = rf_clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, rfpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, rfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, rfpredict))
    models.append(('RandomForestClassifier', rf_clf))
    detection_accuracy.objects.create(names="Random Forest Classifier", ratio=accuracy_score(y_test, rfpredict) * 100)



    print("Gradient Boosting Classifier")

    from sklearn.ensemble import GradientBoostingClassifier
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(
        X_train,
        y_train)
    clfpredict = clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, clfpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, clfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, clfpredict))
    models.append(('GradientBoostingClassifier', clf))
    detection_accuracy.objects.create(names="Gradient Boosting Classifier",
                                      ratio=accuracy_score(y_test, clfpredict) * 100)

    print("KNeighborsClassifier")

    from sklearn.neighbors import KNeighborsClassifier
    kn = KNeighborsClassifier()
    kn.fit(X_train, y_train)
    knpredict = kn.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, knpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, knpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, knpredict))
    detection_accuracy.objects.create(names="KNeighborsClassifier", ratio=accuracy_score(y_test, knpredict) * 100)

    labeled = 'Labled_data.csv'
    df.to_csv(labeled, index=False)
    df.to_markdown

    obj = detection_accuracy.objects.all()
    return render(request,'SProvider/train_model.html', {'objs': obj})