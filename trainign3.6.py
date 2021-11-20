import numpy as np
from os import listdir
from os.path import isfile, join
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import cv2
from sklearn.externals import joblib
X = []
y = []

# load all the images and convert them
files_name = [f for f in listdir('data') if isfile(join('data', f)) and f != '.DS_Store']
for name in files_name:
    try:
        # load the image
        print (name)
        img = cv2.imread(join('data', name))
        print (img)
        # blur to remove details
        img = cv2.blur(img, (5, 5))
        # convert to binary
        retval, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
        # resize to improve performance
        img = cv2.resize(img, (24, 24))
        # convert to array
        image_as_array = np.ndarray.flatten(np.array(img))
        # add our image to the dataset
        X.append(image_as_array)
        # retrive the direction from the filename
        y.append(name.split('_')[1].split('.')[0])
    except Exception as inst:
        print(name)
        print(inst)

# split for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# scale the data
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


clf = MLPClassifier(solver='lbfgs', alpha=100.0, random_state=1, hidden_layer_sizes=50)
clf.fit(X_train, y_train)
print('score: ', clf.score(X_test, y_test))
clf = MLPClassifier(solver='lbfgs', alpha=100.0, random_state=1, hidden_layer_sizes=50)
clf.fit(X, y)
print('score2: ', clf.score(X, y))
joblib.dump(clf, 'expo2.pkl') 

