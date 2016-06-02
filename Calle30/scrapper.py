import xmltodict
import requests
import json
import csv
import time
from time import gmtime, strftime

url = "http://www.mc30.es/images/xml/DatosTrafico.xml"

headers = {'headersHost': 'www.mc30.es', 'User-Agent': 'Python script', 'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive'}

fieldnames = ['totalVehiculosTunel', 'totalVehiculosTunelCalle30',
              'velocidadmediaTunel', 'velocidadMediaSuperficie',
              'fecha']

last_time_request = ""


def get_new_values():
    r = requests.get(url, headers=headers)
    o = xmltodict.parse(r.text)
    j = json.loads(json.dumps(o))
    x = j["DatosTrafico"]["DatoGlobal"]
    values = {'totalVehiculosTunel'        : x[0]['VALOR'],
              'totalVehiculosTunelCalle30' : x[1]['VALOR'],
              'velocidadmediaTunel'        : x[2]['VALOR'],
              'velocidadMediaSuperficie'   : x[3]['VALOR'],
              'fecha'                      : x[0]['FECHA']}
    return values


# start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
name = "datasetTraficoCalle30"
extension = ".csv"
path = "./data/"


with open(path + name + extension, 'w+') as csvfile:
    header = csvfile.readline()
    if (header != fieldnames):
            spamwrite = csv.writer(csvfile, delimiter=' ',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


with open(path + name + extension, 'a') as csvfile:
    while True:
        values = get_new_values()
        if (str(last_time_request) != values['fecha']):
            # Peticiones periodicas de los datos
            last_time_request = values['fecha']
            spamwrite = csv.writer(csvfile, delimiter=' ',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(values)
            print(values)
        else:
            print("Mismos datos desde " + values['fecha'])
        time.sleep(240)   # 4 minutos de espera antes de buscar nuevos datos
