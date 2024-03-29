import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from datetime import datetime

#Importar librería para usar mongo
from pymongo import MongoClient

#Ubicación del servidor de Mongo
client = MongoClient('localhost')
#La base de datos que queremos utilizar, si no existe se crea
db = client['datos_climaticos']
#Lo que queremos guardar va dentro de una colección
col = db['inamhi']

ciudades = [
    ["Tulcan", "Carchi"],
    ["Ibarra","Imbabura"],
    ["Quito", "Pichincha"],
    ["Latacunga", "Cotopaxi"],
    ["Ambato", "Tungurahua"],
    ["Guaranda", "Bolivar"],
    ["Riobamba", "Chimborazo"],
    ["Azogues", "Cañar"],
    ["Cuenca", "Azuay"],
    ["Loja", "Ecuador"]
]

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

driver = webdriver.Chrome('./chromedriver.exe')

for ciudad in ciudades:

    # Url Semilla de Inamhi
    driver.get("http://186.42.174.241/InamhiPronostico/")


    print("**************************************", ciudad[0], "**************************************")
    # Espera hasta que cargue la página
    sleep(random.uniform(6.0, 7.0))

    # Espera hasta que cargue el bloque de ingreso de ubicación
    input_lugar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="addr"]'))
    )

    try:
        # Ciudad a buscar
        # lugar = "Cayambe, Pichincha, Ecuador"
        lugar = ciudad[0] + ", " + ciudad[-1]
        print("Busqueda: ", lugar)

        # Debido a que por defecto el campo de lugar se encuentra lleno con "Quito"
        # Debemos borrarlo antes de colocar el nuevo
        input_lugar.clear()

        # Insertamos el lugar en el campo de texto
        input_lugar.send_keys(lugar)

        # Boton para iniciar la búsqueda
        boton = driver.find_element(By.XPATH, '//button[@value="buscar"]')
        # Le damos en buscar
        boton.click()

        # Se demora en mostrar un listado de posibles ubicaciones así que esperamos
        sleep(random.uniform(3.0, 4.0))

        # Enlace para seleccionar la ubicación
        enlace = driver.find_element(By.XPATH, '//ul[@class="my-new-list"]/li[1]/a')
        # Le damos en buscar
        enlace.click()

        # Espera de carga de los nuevos datos
        sleep(random.uniform(2.0, 3.0))

        # Cambio de contexto dentro del HTML
        driver.switch_to.frame(driver.find_element_by_xpath('//object'))
        hora = driver.find_element_by_xpath('//div[@class="col-xs-12 text-center fechaActual"]').text
        temperatura = driver.find_element_by_xpath('//div[@class="text-center temperaturaActual"]').text
        lluvia = driver.find_element_by_xpath('//table/tbody/tr[2]/td/span[2]').text
        humedad = driver.find_element_by_xpath('//table/tbody/tr[3]/td/span[2]').text

        fechaObjeto = datetime.now()
        fechaTexto = fechaObjeto.strftime('%d/%m/%Y')

        print("********************************")
        print("Hora: ", hora)
        print("Fecha: ", fechaTexto)
        print("Temperatura: ", temperatura)
        print("Lluvia: ", lluvia)
        print("Humedad: ", humedad)

        # Insertando datos en mongo

        col.insert_one({
            'hora': hora,
            'fecha': fechaTexto,
            'temperatura': temperatura,
            'lluvia': lluvia,
            'humedad': humedad,
            'provincia': ciudad[-1],
            'ciudad': ciudad[0]
        })
    except:
        print("No ha podido encontrar la búsqueda de: ", lugar)
        continue




