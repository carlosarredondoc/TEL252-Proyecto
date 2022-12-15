import requests
import random as r
import time
from ecdsa import SigningKey, BRAINPOOLP160r1


url = 'http://localhost:8000/sensor'
id = 1

#######################
# Encriptación ECDSA  #
#######################
sk = SigningKey.generate(curve=BRAINPOOLP160r1)
vk = sk.verifying_key
certificado1 = vk.to_string()
certificado =certificado1.hex()
##########################################
while True:
    temp = r.uniform(5,40)
    sensor = {"id": id, "temp":temp, "cert": certificado }
    print(type(certificado1),certificado1)
    print(type(certificado),certificado)
    #print()
    print(sensor)
    requests.post(url, json = sensor)
    time.sleep(3) 
