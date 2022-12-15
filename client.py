import requests
import random as r
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


url = 'http://localhost:8000/sensor'
id = 1

#######################
# Encriptación ECDSA  #
#######################



device_private_key = ec.generate_private_key(
    ec.SECP384R1()
)

peer_private_key = ec.generate_private_key(
    ec.SECP384R1()
)




shared_key = device_private_key.exchange(
    ec.ECDH(), peer_private_key.public_key())

derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=128,
    salt=None,
    info="tel252_loselipticos".encode(),
).derive(shared_key)

##########################################
while True:
    temp = r.uniform(5,40)
    sensor = {"id": id, "temp":temp, "peer_priv_key": peer_private_key , "device_priv_key": device_private_key , "shared_key": str(derived_key)}
    print(sensor)
    requests.post(url, json = sensor)
    time.sleep(3) 
