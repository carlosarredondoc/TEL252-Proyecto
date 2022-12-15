import requests
import random as r
import time
from ecdsa import SigningKey, BRAINPOOLP160r1
import datetime

url = 'http://193.203.12.121/sensor'
id = 6

#######################
# Encriptación ECDSA  #
#######################
sk = SigningKey.generate(curve=BRAINPOOLP160r1) # se genera firma con la curva Brainpoolp160r1
vk = sk.verifying_key 
certificado = vk.to_string()
certificado = "a" # Prueba de interferencia de certificado.

certificado =certificado.hex() # Para poder trabjar con json y entregar una data cifrada del certificado. Aunque aplicando Cipher chef se puede notar que es un hexadecimal y puede ser decode. Pero aún así estaría sin contexto el atacante. No puede asumir que una firma digital y encontrar facilmente la curva.
# Por lo tanto tomará un poco más de tiempo decifrarlo.


##########################################
while True:
    temp = r.uniform(5,40)
    sensor = {"id": id, "temp":temp, "timestamp" : "" , "cert": certificado } # Ingresan los datos 
    requests.post(url, json = sensor) # Se mandan los datos
    time.sleep(3) 
