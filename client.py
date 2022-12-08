import requests
import random as r
import time

url = 'http://193.203.12.121/sensor'
id = r.randint(0,50)

while True:
    temp = r.uniform(5,40)
    sensor = {"id": id, "temp":temp}

    print(sensor)
    requests.post(url, json = sensor)
    time.sleep(2)