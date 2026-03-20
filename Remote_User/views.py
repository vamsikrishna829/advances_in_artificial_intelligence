from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import VotingClassifier
#model selection
from sklearn.metrics import confusion_matrix, accuracy_score, plot_confusion_matrix, classification_report
# Create your views here.
from Remote_User.models import ClientRegister_Model,early_detection_of_human_diseases,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_early_detection_of_human_diseases(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Age= request.POST.get('Age')
            Sex= request.POST.get('Sex')
            Bmi= request.POST.get('Bmi')
            Fbg= request.POST.get('Fbg')
            hbA1c= request.POST.get('hbA1c')
            Bps= request.POST.get('Bps')
            Bpd= request.POST.get('Bpd')
            Ct= request.POST.get('Ct')
            Ggt= request.POST.get('Ggt')
            Su= request.POST.get('Su')
            Pal= request.POST.get('Pal')
            Dic= request.POST.get('Dic')
            Ac= request.POST.get('Ac')
            Ss= request.POST.get('Ss')


        df = pd.read_csv('Datasets.csv')

        def apply_response(Label):
            if (Label == 0):
                return 0  # Not Detected
            elif (Label == 1):
                return 1  # Detected

        df['results'] = df['Label'].apply(apply_response)

        X = df['Fid'].apply(str)
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

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = str(pred.replace("]", ""))

        prediction = int(pred1)

        if (prediction == 0):
            val = 'Not Detected'

        elif (prediction == 1):
            val = 'Detected'


        print(prediction)
        print(val)

        early_detection_of_human_diseases.objects.create(
            Fid=Fid,
            Age=Age,
            Sex=Sex,
            Bmi=Bmi,
            Fbg=Fbg,
            hbA1c=hbA1c,
            Bps=Bps,
            Bpd=Bpd,
            Ct=Ct,
            Ggt=Ggt,
            Su=Su,
            Pal=Pal,
            Dic=Dic,
            Ac=Ac,
            Ss=Ss,
            Prediction=val)

        return render(request, 'RUser/Predict_early_detection_of_human_diseases.html',{'objs': val})
    return render(request, 'RUser/Predict_early_detection_of_human_diseases.html')



