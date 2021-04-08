import pandas as pd
#this dataset contains headlines of compamies and their stock values
df=pd.read_csv('Data.csv', encoding = "ISO-8859-1")   #encoding should be specified because of use of special characters in the dataset
df.head()  #previewing our dataset


###TRAINING DATASET
train = df[df['Date'] < '20150101']   #before date 01-01-2015 consider in training dataset special


###TESTING DATASET
test = df[df['Date'] > '20141231']    #after date 31-12-2014 consider in testing dataset

##PREPROCESSING

# Removing punctuations in this dataset
data=train.iloc[:,2:27]
data.replace("[^a-zA-Z]"," ",regex=True, inplace=True) #replacing everything except a-z and A-Z with space

# Renaming column names for easily accessing
#from 0-24
list1= [i for i in range(25)]
new_Index=[str(i) for i in list1]
data.columns= new_Index
data.head(5)   #printing top 5 rows to check


# Convertng headlines to lower case for ease of access
for index in new_Index:
    data[index]=data[index].str.lower()
data.head(1) #preview


#combining(using join with space) top 25 headlines to one paragraph(converting to vetor)
' '.join(str(x) for x in data.iloc[1,0:25])


#here list(headlines[]) contains list of sentences of every records(rows) after join 
headlines = []
for row in range(0,len(data.index)): #iterating over all the 26 rows
    headlines.append(' '.join(str(x) for x in data.iloc[row,0:25]))



#CountVectorizer for coverting sentences to vector
#RandomForestClassifier for classification
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


#implementing word groups
countvector=CountVectorizer(ngram_range=(2,2)) #pair of words /stop words also to be considered beacuse of news headlines
traindataset=countvector.fit_transform(headlines)



# implement RandomForest Classifier
randomclassifier=RandomForestClassifier(n_estimators=200,criterion='entropy')
randomclassifier.fit(traindataset,train['Label'])


## Predicting for the Test Dataset
#every steps same here also
test_transform= []
for row in range(0,len(test.index)):
    test_transform.append(' '.join(str(x) for x in test.iloc[row,2:27]))
test_dataset = countvector.transform(test_transform)
predictions = randomclassifier.predict(test_dataset)


## Import library to check accuracy
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score



matrix=confusion_matrix(test['Label'],predictions)      
print(matrix)	

score=accuracy_score(test['Label'],predictions)
print(score)

report=classification_report(test['Label'],predictions)
print(report)
