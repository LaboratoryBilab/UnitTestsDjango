from django.test import TestCase
import numpy as np
from BI.forecast import Forecast
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


class ForecastTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.NumData = 6
        cls.x = np.array([i + 1 for i in range(cls.NumData)]).reshape(-1, 1)
        cls.y = np.array([-i for i in cls.x]).reshape(-1, 1)

    def setUp(self):
        pass

    '''
    - Тестируется метод - LinearRegression
    - Проверяется возвращаемое значение
    - Результат должен быть типа sklearn LinearRegression
    '''

    def test_LinearRegression_RetunedValueType_SklearnLinearRegression(self):
        # Arrange

        # Act
        model = Forecast.LinearRegression(self.x, self.y)

        # Assert
        self.assertIsInstance(model, LinearRegression)

    '''
    - Тестируется метод - RandomForecast
    - Проверяется возвращаемое значение
    - Результат должен быть типа sklearn RandomForestRegressor
    '''

    def test_RandomForecast_RetunedValueType_SklearnRandomForestRegressor(self):
        # Arrange
        x = self.x.reshape(1, -1)
        y = self.y.reshape(1, -1)
        # Act
        model = Forecast.RandomForecast(x, y)

        # Assert
        self.assertIsInstance(model, RandomForestRegressor)

    '''
    - Тестируется метод - SVC
    - Проверяется возвращаемое значение
    - Результат должен быть типа sklearn SVR
    '''

    def test_SVC_RetunedValueType_SklearnSVR(self):
        # Arrange
        x = self.x
        y = self.y.reshape(-1)

        # Act
        model = Forecast.SVC(x, y)

        # Assert
        self.assertIsInstance(model, SVR)

    '''
    - Тестируется метод - NeuralNetwork
    - Проверяется возвращаемое значение
    - Результат должен быть типа [list] и содержать количество элементов = длине [self.x]
    '''

    def test_NeuralNetwork_RetunedValueTypeAndLength_TypeListAndLengthEqualSelfX(self):
        # Arrange

        # Act
        model = Forecast.NeuralNetwork(self.x, self.y)

        # Assert
        self.assertIsInstance(model, list)
        self.assertEqual(len(model), len(self.x))


    '''
    - Тестируется метод - MAPE
    - Проверяется возвращаемое значение
    - Результат должен быть типа [float]
    '''

    def test_MAPE_RetunedValue_TypeFloatEqualValue(self):
        # Arrange
        y = [i+1 for i in range(self.NumData)]
        y_pred = y
        y_fake_pred = [-i for i in y_pred]

        # Act
        mapeVal = Forecast.MAPE(y, y_pred)
        mapeValWithBadValues = Forecast.MAPE(y, y_fake_pred)

        # Assert
        self.assertIsInstance(mapeVal, float)
        self.assertIsInstance(mapeValWithBadValues, float)
        self.assertEqual(mapeVal, 0)
        self.assertEqual(mapeValWithBadValues, 2)

