import requests
import random as r
import time
from ecdsa import SigningKey, BRAINPOOLP160r1
import datetime

url = 'http://193.203.12.121/sensor'
id = 1

#######################
# Encriptación ECDSA  #
#######################
sk = SigningKey.generate(curve=BRAINPOOLP160r1)
vk = sk.verifying_key
certificado = vk.to_string()
certificado =certificado.hex()


##########################################
while True:
    temp = r.uniform(5,40)
    sensor = {"id": id, "temp":temp, "timestamp" : "" , "cert": certificado }
    print(f"certificado: {certificado}")
    requests.post(url, json = sensor)
    time.sleep(3) 
