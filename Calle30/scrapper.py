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


def new_values(writer, last_time_request):
    r = requests.get(url, headers=headers)
    o = xmltodict.parse(r.text)
    j = json.loads(json.dumps(o))
    x = j["DatosTrafico"]["DatoGlobal"]
    values = {'totalVehiculosTunel'        : x[0]['VALOR'],
              'totalVehiculosTunelCalle30' : x[1]['VALOR'],
              'velocidadmediaTunel'        : x[2]['VALOR'],
              'velocidadMediaSuperficie'   : x[3]['VALOR'],
              'fecha'                      : x[0]['FECHA']}
    if (str(last_time_request) != x[0]['FECHA']):
        print(values)
        writer.writerow(values)
        return x[0]['FECHA']
    else:
        print("Mismos datos siendo los ultimos de " + last_time_request)
        return last_time_request


start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
extension = ".csv"
path = "./data/"

with open(path + start_time + extension, 'w') as csvfile:
    spamwrite = csv.writer(csvfile, delimiter=' ',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while True:
        # Peticiones periodicas de los datos
        last_time_request = new_values(writer, last_time_request)
        time.sleep(240)   # 4 minutos de espera antes de buscar nuevos datos
