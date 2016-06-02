import xmltodict
import requests
import json
import csv
import time
import os

# url de a la que se hace la peticion GET
url = "http://www.mc30.es/images/xml/DatosTrafico.xml"

# Headers necesarios para que la peticion GET este autorizada
headers = {'headersHost': 'www.mc30.es', 'User-Agent': 'Python script', 'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive'}

fieldnames = ['totalVehiculosTunel', 'totalVehiculosTunelCalle30',
              'velocidadmediaTunel', 'velocidadMediaSuperficie',
              'fecha']


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


name = "datasetTraficoCalle30"
extension = ".csv"
path = "./data/"
file_path = path + name + extension


if (not os.path.exists(file_path)):
    open(file_path, 'w')


with open(file_path, 'r+') as csvfile:
    header = csvfile.readline().strip().split(',')
    if (header != fieldnames):
        # spamwrite = csv.writer(csvfile, delimiter=' ',
        #                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print("Nuevo fichero creado")
        last_time_request = ""
    else:
        last = csvfile.readlines()[-1]
        last_time_request = last.strip().split(',')[-1]


with open(file_path, 'a') as csvfile:
    while True:
        values = get_new_values()
        # Comprobacion de que los datos no se encuentran ya en el fichero
        if (str(last_time_request) != values['fecha']):
            # Peticiones periodicas de los datos
            last_time_request = values['fecha']
            # spamwrite = csv.writer(csvfile, delimiter=' ',
            #                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(values)
            print(values)
        else:
            print("Mismos datos desde " + values['fecha'])
        time.sleep(240)   # 4 minutos de espera antes de buscar nuevos datos
