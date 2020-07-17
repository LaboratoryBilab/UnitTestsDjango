from django.test import TestCase
from BI.models import *
from datetime import datetime


class DBTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass


    '''
    - Тестируется база данных
    - Проверяется запись в базу данных сущность типа [Request]
    - Успешная запись в базу данных
    '''


    def test_DB_SaveEntityRequestToDB_SuccessSaveToDB(self):
        # Arrange
        request = Request()
        request.rmse = 1
        request.mape = 2
        request.mae = 3
        request.datetime = datetime.utcnow()

        # Act
        request.save()
        entityFromDb = Request.objects.last()

        # Assert
        self.assertEqual(request.mae, entityFromDb.mae)
        self.assertEqual(request.mape, entityFromDb.mape)
        self.assertEqual(request.rmse, entityFromDb.rmse)


    '''
    - Тестируется база данных
    - Проверяется запись в базу данных сущность типа [CSVFile]
    - Успешная запись в базу данных
    '''


    def test_DB_SaveEntityCSVFileToDB_SuccessSaveToDB(self):
        # Arrange
        csvfile = CSVFile()
        csvfile.filecontent = "1,2,3,4"
        csvfile.countrows = 1
        csvfile.namefile = "namefile.csv"

        # Act
        csvfile.save()
        entityFromDb = CSVFile.objects.last()

        # Assert
        self.assertEqual(csvfile.filecontent, entityFromDb.filecontent)
        self.assertEqual(csvfile.countrows, entityFromDb.countrows)
        self.assertEqual(csvfile.namefile, entityFromDb.namefile)


    '''
    - Тестируется база данных
    - Проверяется запись в базу данных сущность типа [Monitoring]
    - Успешная запись в базу данных
    '''


    def test_DB_SaveEntityMonitoringToDB_SuccessSaveToDB(self):
        # Arrange
        monitoring = Monitoring()
        monitoring.memory = 12512.124
        monitoring.cpu = 0.5
        monitoring.time = 100.531

        # Act
        monitoring.save()
        entityFromDb = Monitoring.objects.last()

        # Assert
        self.assertEqual(monitoring.memory, entityFromDb.memory)
        self.assertEqual(monitoring.cpu, entityFromDb.cpu)
        self.assertEqual(monitoring.time, entityFromDb.time)
