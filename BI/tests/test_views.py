from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from BI.models import *
from datetime import datetime


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    '''
    - Тестируется Get запрос по адресу: [/helloThere/]
    - Проверяется код ответа и содержимое
    - Код результата должен быть [200] и содержать строку ["General Kenobi!"]
    '''

    def test_Hello_MethodGet_SuccessCode(self):
        # Arrange

        # Act
        response = self.client.get("/helloThere/")

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"General Kenobi!", response.content)

    '''
    - Тестируется Get запрос по адресу: [/predict/]
    - Проверяется код ответа без передачи параметров
    - Код результата должен быть [500] и содержать информацию об ошибке
    '''

    def test_Predict_MethodGetWithEmptyRequestHeaders_InternalServerErrorCode(self):
        # Arrange

        # Act
        response = self.client.get("/predict/")

        # Assert
        self.assertEqual(500, response.status_code)
        self.assertNotEqual(b"", response.content)

    '''
    - Тестируется Post запрос по адресу: [/predict/]
    - Проверяется код ответа
    - Код результата должен быть [200] и содержать информацию и выполнении метода
    '''

    def test_Predict_MethodGetWithFile_SuccessCode(self):
        # Arrange

        # Act
        with open('Data.csv', 'rb') as f:
            response = self.client.post("/predict/", {'test.csv': f})

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(b"", response.content)

    '''
    - Тестируется Post запрос по адресу: [/predict/]
    - Проверяется запись в базу данных
    - Код результата должен быть [200] и количество записей увеличиться на 1 единицу
    '''

    def test_Predict_SaveRequestToDB_NumberEntities(self):
        # Arrange
        beforeNumberRequests = len(Request.objects.all())
        beforeNumberCSVFiles = len(CSVFile.objects.all())
        beforeNumberMonitorings = len(Monitoring.objects.all())

        # Act
        with open('Data.csv', 'rb') as f:
            response = self.client.post("/predict/", {'test.csv': f})

        afterNumberRequests = len(Request.objects.all())
        afterNumberCSVFiles = len(CSVFile.objects.all())
        afterNumberMonitorings = len(Monitoring.objects.all())

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(beforeNumberRequests + 1, afterNumberRequests)
        self.assertEqual(beforeNumberCSVFiles + 1, afterNumberCSVFiles)
        self.assertEqual(beforeNumberMonitorings + 1, afterNumberMonitorings)

    '''
    - Тестируется Post запрос по адресу: [/predict/]
    - Проверяется запись в базу данных
    - Код результата должен быть [200] и количество записей увеличиться на 1 единицу 
      и содержать одинаковое количество в 3х таблицах 
    '''

    def test_Predict_SaveRequestToDB_EqualsNumberEntities(self):
        # Arrange
        beforeNumberRequests = len(Request.objects.all())
        beforeNumberCSVFiles = len(CSVFile.objects.all())
        beforeNumberMonitorings = len(Monitoring.objects.all())

        beforeEqualsNumber = beforeNumberRequests == beforeNumberCSVFiles == beforeNumberMonitorings

        # Act
        with open('Data.csv', 'rb') as f:
            response = self.client.post("/predict/", {'test.csv': f})

        afterNumberRequests = len(Request.objects.all())
        afterNumberCSVFiles = len(CSVFile.objects.all())
        afterNumberMonitorings = len(Monitoring.objects.all())

        afterEqualsNumber = afterNumberRequests == afterNumberCSVFiles == afterNumberMonitorings

        # Assert
        self.assertTrue(beforeEqualsNumber)
        self.assertTrue(afterEqualsNumber)
        self.assertEqual(beforeNumberRequests + 1, afterNumberRequests)
