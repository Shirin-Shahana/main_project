import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# Read dataset to pandas dataframe
df1 = pd.read_csv('data/data/Fertilizer Prediction new.csv')
# print(df1.shape)
#cols=df1.columns
#print(cols)

# df1.value_counts("Fertilizer Name")
# X=df1.iloc[:,0:8].values
# print(X)

# y=df1.iloc[:,8].values
# print👍
# y=df1['Fertilizer Name']
# df1.drop('Fertilizer Name',axis=1,inplace=True)
# print(df1.head())
attri=df1.values[:,0:8]
label=df1.values[:,8]
print(attri)
print(label)

X_train, X_test, y_train, y_test = train_test_split(attri, label, test_size=0.3)
clf=RandomForestClassifier()

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Classification report")
print("-------------------")
print(metrics.classification_report(y_test,clf.predict(X_test)))
print("Confusion matrix")
print(metrics.confusion_matrix(y_test,y_pred))
#pred=clf.predict(26,52,38,1,1,37,0,0)
#print(pred)
 # Saving the model
filename = 'RF2.sav'
pickle.dump(clf, open(filename, 'wb'))