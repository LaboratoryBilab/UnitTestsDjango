from datetime import datetime
import json
import time
import sys
from io import StringIO
from django.test import Client
import psutil
# from guppy import hpy
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from BI.forecast import Forecast
from io import TextIOWrapper
import csv
from BI.models import *


def checkData(x):
    return True  # x[0] != 0 and x[1] != 0 and x[4] != 0


@csrf_exempt
def Hello(request: HttpRequest):
    return HttpResponse("General Kenobi!")


@csrf_exempt
def AutoRequest(request: HttpRequest):
    with open('Data.csv', 'rb') as f:
        client = Client()
        response = client.post("/predict/", {'test.csv': f})
        print(response)
    return response


def GetFile(namefile, bytes, encoding):
    file = CSVFile()
    file.namefile = namefile

    data = TextIOWrapper(bytes, encoding=encoding)
    file.filecontent = data.read()
    file.countrows = len(file.filecontent.split('\n'))
    return file


def SaveToDB(metrix, date, file, monitoringParams):
    # Monitoring
    monitoring = Monitoring()
    monitoring.cpu = monitoringParams.get('cpu')
    monitoring.memory = monitoringParams.get('memory')
    monitoring.time = monitoringParams.get('time')

    # Request
    request = Request()
    request.datetime = date
    request.rmse = metrix.get("RMSE")[0]
    request.mae = metrix.get("MAE")[0]
    request.mape = metrix.get("MAPE")[0]

    request.csvfile = file
    request.monitoring = monitoring
    request.save()
    request.csvfile.save()
    request.monitoring.save()

@csrf_exempt
def Predict(request: HttpRequest):
    dateTime = datetime.utcnow()
    # Засекаем время начала обработки запроса
    start_time = time.clock()
    # Засекаем как сильно загрузился процессор во время обработки заброса
    psutil.cpu_percent(interval=None, percpu=True)
    try:
        data = []
        if len(request.FILES) == 1:
            # Имя обрабатываемого файла можно найти как request.FILES['file']
            for key in request.FILES:
                csvfile = GetFile(key, request.FILES[key].file, request.encoding)
                data = handle_files(csvfile.filecontent)
        else:
            return HttpResponseServerError("<h2>No file</h2>")

        try:
            date = [y[0] for y in data]

            revenue = [float(y[1]) for y in data if (y[1] is not "")]
            crop = [float(y[2]) for y in data if (y[2] is not "")]
            temp = [float(y[3]) for y in data if (y[3] is not "")]
            rain = [float(y[4]) for y in data if (y[4] is not "")]
            cost = [float(y[5]) for y in data if (y[5] is not "")]

        except Exception as e:
            return HttpResponseServerError("<h2>Wrong file: " + str(e) + "</h2>")

        crop_forecast_rf = CropForecast(crop, temp, rain, "RF")
        cost_forecast_rf = CostForecast(cost, crop + crop_forecast_rf[len(crop):], temp, rain, "RF")
        revenue_forecast_train_rf, revenue_forecast_test_rf = RevenueForecast(revenue,
                                                                              cost + cost_forecast_rf[len(cost):],
                                                                              crop + crop_forecast_rf[len(crop):], temp,
                                                                              rain,
                                                                              "RF")

        rf_rmse = Forecast.RMSE(revenue, (revenue_forecast_train_rf + revenue_forecast_test_rf)[0:len(revenue)])
        rf_mae = Forecast.MAE(revenue, (revenue_forecast_train_rf + revenue_forecast_test_rf)[0:len(revenue)])
        rf_mape = Forecast.MAPE(revenue, (revenue_forecast_train_rf + revenue_forecast_test_rf)[0:len(revenue)])

        crop_forecast_lr = CropForecast(crop, temp, rain, "LR")
        cost_forecast_lr = CostForecast(cost, crop + crop_forecast_lr[len(crop):], temp, rain, "LR")
        revenue_forecast_train_lr, revenue_forecast_test_lr = RevenueForecast(revenue,
                                                                              cost + cost_forecast_lr[len(cost):],
                                                                              crop + crop_forecast_lr[len(crop):], temp,
                                                                              rain,
                                                                              "LR")
        lr_rmse = Forecast.RMSE(revenue, (revenue_forecast_train_lr + revenue_forecast_test_lr)[0:len(revenue)])
        lr_mae = Forecast.MAE(revenue, (revenue_forecast_train_lr + revenue_forecast_test_lr)[0:len(revenue)])
        lr_mape = Forecast.MAPE(revenue, (revenue_forecast_train_lr + revenue_forecast_test_lr)[0:len(revenue)])

        # crop_forecast_net = CropForecast(crop, temp, rain, "NET")
        # cost_forecast_net = CostForecast(cost, crop + crop_forecast_net[len(crop):], temp, rain, "NET")
        # revenue_forecast_train_net, revenue_forecast_test_net = RevenueForecast(revenue,
        #                                                                       cost + cost_forecast_net[len(cost):],
        #                                                                       crop + crop_forecast_net[len(crop):], temp,
        #                                                                       rain,
        #                                                                       "NET")
        # net_rmse = Forecast.RMSE(revenue, (revenue_forecast_train_net + revenue_forecast_test_net)[0:len(revenue)])
        # net_mae = Forecast.MAE(revenue, (revenue_forecast_train_net + revenue_forecast_test_net)[0:len(revenue)])
        # net_mape = Forecast.MAPE(revenue, (revenue_forecast_train_net + revenue_forecast_test_net)[0:len(revenue)])

        # print("rf_rmse: ", str(rf_rmse))
        # print("rf_mae: ", str(rf_mae))
        # print("rf_mape: ", str(rf_mape))
        #
        # print("lr_rmse: ", str(lr_rmse))
        # print("lr_mae: ", str(lr_mae))
        # print("lr_mape: ", str(lr_mape))

        # print("net_rmse: ", str(net_rmse))
        # print("net_mae: ", str(net_mae))
        # print("net_mape: ", str(net_mape))

        response = {
            'date': [y for y in date],
            'revenue': {
                'fact': [y for y in revenue],
                'forecast': [y for y in revenue_forecast_train_rf + revenue_forecast_test_rf],
                'RMSE': [rf_rmse],
                'MAE': [rf_mae],
                'MAPE': [rf_mape]
            },
            'crop': {
                'fact': [y for y in crop],
                'forecast': [y for y in crop_forecast_rf]
            },
            'cost': {
                'fact': [y for y in cost],
                'forecast': [y for y in cost_forecast_rf]
            },
            'temp': [y for y in temp],
            'rain': [y for y in rain]
        }
        # Засекаем время конца обработки запроса
        end_time = time.clock()
        # h - данные о количестве используемой памяти в программе
        # h = hpy()
        # memory_data = h.heap()
        # Через регулярку вытаскиваю сколько в байтах памяти занимает программа
        # res = re.search('size = (.*) bytes', str(memory_data))
        memory_usage = 123  # res.group(1)
        # Нахожу сколько весит массив с данными (по идее столько же сколько файл)
        data_size = sys.getsizeof(data)
        # Как сильно был загружен процессор с момента последнего запроса команды
        cpu_percent = psutil.cpu_percent(interval=None, percpu=False)

        # Логирую в файл данные для дальнейшей обработки
        file = open("log.txt", "a")
        file.write(make_scv_str(data, memory_usage, end_time - start_time, cpu_percent))
        monitoring = {
            'cpu': cpu_percent,
            'memory': memory_usage,
            'time': end_time - start_time
        }
        file.close()

        empty_response = {
            'metrics': {
                'RMSE': [rf_rmse],
                'MAE': [rf_mae],
                'MAPE': [rf_mape]
            }
        }
        SaveToDB(empty_response['metrics'], dateTime, csvfile, monitoring)
        return HttpResponse(json.dumps(empty_response))
    except Exception as e:
        return HttpResponseServerError("<h2>An error occured " + str(e) + "</h2>")


def make_scv_str(data, memory_usage, processing_time, cpu_percent):
    scv_str = "\n"
    scv_str += str(len(data)) + ","  # Число строк в обрабатываемом файле
    scv_str += str(sys.getsizeof(data)) + ","  # Размер файла. (Не точный?)
    scv_str += str(round(processing_time, 5)) + ","  # Время обработки файла
    scv_str += str(
        round(float(memory_usage) / (1024 ** 2), 5)) + ","  # Количество использованной памяти программой в мегабайтах
    scv_str += str(cpu_percent)  # Процент использования процессора за время исполнения программы
    # Загруженность диска
    # Загруженность интернета
    return scv_str


def handle_files(f):
    reader = csv.reader(StringIO(f))
    data = []
    for row in reader:
        data.append(row)
    return data[1:]


def CropForecast(crop, temp, rain, method):
    factors = [[y] for y in temp]
    for x in range(min(len(temp), len(rain))):
        factors[x].append(rain[x])
    forecast_train, forecast_test = ForecastValue(factors, crop, method)
    return forecast_train + forecast_test


def CostForecast(cost, crop, temp, rain, method):
    factors = [[y] for y in crop]
    for x in range(len(crop)):
        factors[x].append(temp[x])
        factors[x].append(rain[x])
    forecast_train, forecast_test = ForecastValue(factors, cost, method)
    return forecast_train + forecast_test


def RevenueForecast(revenue, cost, crop, temp, rain, method):
    factors = [[y] for y in cost]
    for x in range(len(cost)):
        factors[x].append(crop[x])
        factors[x].append(temp[x])
        factors[x].append(rain[x])
    forecast_train, forecast_pred = ForecastValue(factors, revenue, method)
    return forecast_train, forecast_pred


def ForecastValue(factors, value, method):
    train_factors = [y for y in factors[0:len(value)]]
    train_value = [y for y in value[0:len(value)]]
    test_factors = [y for y in factors[len(value):]]

    if method == "RF":
        forecastModel = Forecast.RandomForecast(train_factors, train_value)
        return list(forecastModel.predict(train_factors)), list(forecastModel.predict(test_factors))
    elif method == "LR":
        forecastModel = Forecast.LinearRegression(train_factors, train_value)
        return list(forecastModel.predict(train_factors)), list(forecastModel.predict(test_factors))
    else:
        result = Forecast.NeuralNetwork(train_factors, train_value)
        result += Forecast.NeuralNetwork(test_factors, train_value)
        return result
