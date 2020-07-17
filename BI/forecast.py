from sklearn import linear_model
from sklearn import ensemble
from sklearn import svm
from sklearn import neural_network
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from math import sqrt
import math
import numpy as np


class Forecast:
    # метод линейной регрессии
    @staticmethod
    def LinearRegression(x: list, y: list):
        model = linear_model.LinearRegression(n_jobs=-1)
        model.fit(x, y)
        return model

    # метод случайного леса
    @staticmethod
    def RandomForecast(x: list, y: list):
        model = ensemble.RandomForestRegressor(n_jobs=-1)
        model.fit(x, y)
        return model

    # метод опорных векторов
    @staticmethod
    def SVC(x: list, y: list, ):
        model: svm.SVR = svm.SVR()
        model.fit(x, y)
        return model

    # нейронная сеть
    @staticmethod
    def NeuralNetwork(x: list, y: list):
        normData = [(cur - min(y)) / (max(y) - min(y)) for cur in y]
        res = []
        for i in range(0, len(x[0])):
            res.append([n[i] for n in x[0:len(y)]])
        normFactors = [[(curr - min(cur)) / (max(cur) - min(cur)) for curr in cur] for cur in res]
        normalizedFactors = []
        for i in range(0, len(normFactors[0])):
            normalizedFactors.append([])
            for j in range(0, len(normFactors)):
                normalizedFactors[i].append(normFactors[j][i])

        model = neural_network.MLPRegressor(
            hidden_layer_sizes=(10,), activation='relu', solver='adam', alpha=0.1, batch_size='auto',
            learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
            random_state=5, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
            early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        model.fit(normalizedFactors, [float(a) for a in normData])
        result = list(model.predict(normalizedFactors))
        result = [r * (max(y) - min(y)) + min(y) for r in result]
        return result

    @staticmethod
    def Accuracy(fact: list, pred: list):
        return metrics.accuracy_score(fact, pred)

    @staticmethod
    def RMSE(fact: list, pred: list):
        return sqrt(metrics.mean_squared_error(fact, pred))

    @staticmethod
    def MAE(fact: list, pred: list):
        return metrics.mean_absolute_error(fact, pred)

    @staticmethod
    def MAPE(actual, predict):
        tmp, n = 0.0, 0
        for i in range(0, len(actual)):
            if actual[i] != 0:
                tmp += math.fabs(actual[i]-predict[i])/actual[i]
                n += 1
        return tmp / n
