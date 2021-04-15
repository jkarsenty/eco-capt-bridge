import random
import json
import datetime as dt
import numpy as np

def random_data():

    x1 = np.random.randint(0, 55, None)         # Dummy temperature
    y1 = np.random.randint(0, 45, None)         # Dummy humidigy
    my_sensor = f"{x1},{y1}"
    return my_sensor                            # return data seperated by comma


def generate_fake_data(nb_data:int=10,path_measures_config:str="Bridge_v2/Sensors/measures_config.json"):

    measure_config_list = []
    for i in range(nb_data):
        if i%2 == 0:
            maxValue = f"000{45 + 3*i}"
            minValue = f"000{9 + 2*i}"
        else:
            maxValue = f"000{70 - 3*i}"
            minValue = f"000{20 - 2*i}"
        meanValue = str(round((int(maxValue)+int(minValue))/2.07))
        medianValue = str(round((int(maxValue)-int(minValue))/1.96))
        while len(maxValue)!=8:
            maxValue = "0"+maxValue
        while len(minValue)!=8:
            minValue = "0"+minValue
        while len(meanValue)!=8:
            meanValue = "0"+meanValue
        while len(medianValue)!=8:
            medianValue = "0"+medianValue

        idAlerte = random.choice(["0001","0002","0003","0004"])
        if int(idAlerte)==1:
            valueAlerte = str(int(maxValue) + 2*i)
        elif int(idAlerte)==2:
            valueAlerte = str(int(minValue) - 2*i)
        elif int(idAlerte)==3:
            valueAlerte = str(int(meanValue) + 3*i)
        elif int(idAlerte)==4:
            valueAlerte = str(int(medianValue) + 3*i)
        while len(valueAlerte) !=8 :
            valueAlerte = "0" + valueAlerte
        if int(valueAlerte) < 0:
            valueAlerte = "00000001"
        assert len(valueAlerte) == 8, f"{abs(8-len(valueAlerte))}"
        
        now = dt.datetime.now()
        delay = dt.timedelta(minutes=3*i)
        my_time = now + delay

        _measureHeader = {
                "version": "00.01.00",
                "date": f"{my_time.strftime('%Y%m%d%H%M')}",
                "measureType": "SON_0001",
                "timeCode": "i", #Y m d H i
                "nbTime": "001"
            }
        _measureBody = {
                "maxValue": maxValue,
                "minValue": minValue,
                "meanValue": meanValue,
                "medianValue": medianValue
            }
        _alerteConfig = {
            "version": "00.01.00",
            "idAlerte":idAlerte,
            "date": f"{my_time.strftime('%Y%m%d%H%M')}",
            "valueAlerte":valueAlerte
        }

        measure_config_list.append(
            {
                "_measureHeader":_measureHeader,
                "_measureBody":_measureBody,
                "_alerteConfig":_alerteConfig
            }
        )

    with open(path_measures_config,"w") as f:
        f.write(json.dumps(measure_config_list,indent=4,ensure_ascii=False))

if __name__ == '__main__':
    generate_fake_data(nb_data=10,path_measures_config="Bridge_v2/Sensors/measures_config.json")
    
