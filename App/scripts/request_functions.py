import requests


def addMeasurePost(endpoint:str,_serviceId:int,_measureHeader:str,_measureBody:str):
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{ "_serviceId":' + str(_serviceId) + ', "_measureHeader":"' + _measureHeader + '", "_measureBody":"' + _measureBody + '"}'

    response = requests.post(f'http://127.0.0.1:5000/{endpoint}', headers=headers, data=data)
    assert response.status_code == 200,response.status_code
    return response


def addAlertPost(endpoint:str, _serviceId:int, _alerteConfig:str):
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{ "_serviceId":' + str(_serviceId) + ', "_alerteConfig":"' + _alerteConfig + '"}'
    #print(data)

    response = requests.post(f'http://127.0.0.1:5000/{endpoint}', headers=headers, data=data)

    assert response.status_code == 200,response.status_code
    return response