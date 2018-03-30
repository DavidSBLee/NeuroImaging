#sciKIT_tree_dummy_sample

"""
### Generate dummy data
# (# of subjects, x, y, z, # of channels (3 in case of RGB))
x_train = np.random.random((1000, 10, 10, 10, 1))
# 2 categories, (# of subjects, # of channels, num_classes= number of label)
y_train = keras.utils.to_categorical(np.random.randint(2, size=(1000, 1)), num_classes=2)
x_test = np.random.random((100, 10, 10, 10, 1))
y_test = keras.utils.to_categorical(np.random.randint(2, size=(100, 1)), num_classes=2)
"""

# CSV to Python Numpy Array
import numpy as np
my_data = np.genfromtxt('/Users/SB/Desktop/behavioral_data.csv', delimiter=',', dtype=float, skip_header=1)
X = (my_data[:,13:16])
y = (my_data[:,0])

# Missing Value Imputation
from sklearn.preprocessing import Imputer
imp = Imputer(axis=0, missing_values='NaN', strategy='mean')
X = imp.fit_transform(X)

# Splitting Training and Test Set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2)
#print(f'X.shape = {X.shape}')
#print(f'X_test.shape = {X_test.shape}')
#print(f'X_train.shape = {X_train.shape}')

#print(f'y.shape = {y.shape}')
print(f'what are labels? = {np.unique(y)}')
#print(f'y_test.shape = {y_test.shape}')
#print(f'y_train.shape = {y_train.shape}')

# Train the model with decision tree
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm


#clf = DecisionTreeClassifier(max_depth=10, criterion='gini')
clf = svm.LinearSVC()
print (clf)
clf.fit(X_train, y_train)

# Test the model on test set 
from sklearn.metrics import (accuracy_score, precision_score, 
                             recall_score, f1_score, log_loss)

"""
Same as:
print (clf.score(X_train, y_train))
print (clf.score(X_test, y_test))
"""
y_train_pred = clf.predict(X_train)
y_test_pred = clf.predict(X_test)
print(f'training accuracy = {accuracy_score(y_train, y_train_pred)}')
print(f'testing accuracy = {accuracy_score(y_test, y_test_pred)}')

# Cross-Validation
from sklearn.model_selection import cross_validate
scores = cross_validate(clf, X_train, y_train,
                        scoring='accuracy', cv=4,
                        return_train_score=True)

print(scores.keys())
test_scores = scores['test_score']
train_scores = scores['train_score']
print(test_scores)
print(train_scores)

"""
# Tuning Hyperparameters using GridSearchCV
from sklearn.model_selection import GridSearchCV

# Instantiate a model
clf = DecisionTreeClassifier()

# Specify hyperparameter values to test
parameters = {'max_depth': range(1, 20),
              'criterion': ['gini', 'entropy']}

# Run grid search
gridsearch = GridSearchCV(clf, parameters, scoring='accuracy', cv=4)
gridsearch.fit(X_train, y_train)

# Get best model
print(f'gridsearch.best_params_ = {gridsearch.best_params_}')
print(gridsearch.best_estimator_)
"""

"""
y_pred = clf.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)
print(f'test_acc = {test_acc}')
"""


