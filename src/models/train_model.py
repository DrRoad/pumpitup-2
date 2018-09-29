import pandas as pd
import os

from scipy import stats
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier

from src.visualization.visualize import ValidationError

def chi_squared_test(df, col_x, col_y, p_threshold):
    contingency_tmp = pd.crosstab(df[col_y],df[col_x])
    #(contingency_tmp)
    chi2, p, dof, expected = stats.chi2_contingency(contingency_tmp.values)
    if p <= p_threshold:
        print("Correlated. Has a p-value of ",p)
        #contingency_tmp
    else:
        print("Not Correlated. Has a p-value of  ",p)


def create_model_svc():
    """

    Checks for the existence of training data files in the data/processed folder and trains a linear svc model using it.

    """

    is_file_exists = os.path.isfile("data/processed/X_train.csv") and os.path.isfile("data/processed/y_train.csv")
    if not is_file_exists:
        raise ValidationError("Training data files doesn't exist", "data/processed")
    else:
        X_train = pd.read_csv("data/processed/X_train.csv")
        y_train = pd.read_csv("data/processed/y_train.csv")
        X_test  = pd.read_csv("data/processed/X_test.csv")
        y_test  = pd.read_csv("data/processed/y_test.csv")
    pipe_svc = Pipeline([('clf', LinearSVC(dual=False))])
    param_grid = {'clf__C':[0.001, 0.01, 0.1, 1.0],
                      'clf__class_weight':[None, 'balanced']}
    estimator = GridSearchCV(estimator=pipe_svc,
                                 param_grid=param_grid,
                                 n_jobs=-1)
    y_shape_c, y_shape_r = y_train.shape
    y_train = y_train.values.reshape(y_shape_c,)
    clf = RandomForestClassifier(n_estimators= 1000,max_depth= 10,random_state= 0)
    clf.fit(X_train,y_train)
    pred = clf.predict(X_test)
    random_forest_accuracy = accuracy_score(y_test,pred)
    print(random_forest_accuracy)
    #try:
    #    estimator.fit(X_train, y_train)
    #except:
    #    print("Error")    
    #validation_accuracy = estimator.score(X_test, y_test)
    #print(validation_accuracy)


create_model_svc() 