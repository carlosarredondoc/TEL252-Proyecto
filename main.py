from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

app = FastAPI()

data_sensor = {}

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

##




# Perform key derivation.


class Sensor(BaseModel):
    id: str
    timestamp: None | datetime
    temp: str
    peer_priv_key: str
    device_priv_key: str
    shared_key: str
import sys
def str_to_class(str):
    return getattr(sys.modules[__name__], str)


@app.post("/sensor")
async def upload_data(sensor:Sensor):
    
    peer_priv_key = str_to_class(sensor.peer_priv_key)
    
    device_private_key = str_to_class(sensor.device_priv_key)
    

    shared_key_dev = sensor.shared_key
    print("a")

    same_shared_key = peer_priv_key.exchange(
    ec.ECDH(), device_private_key.public_key())
    
    same_derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=128,
    salt=None,
    info='tel252_loselipticos'.encode(),
    ).derive(same_shared_key)

    if same_derived_key == shared_key_dev:
        sensor.timestamp = datetime.now()
        json_compatible_item_data = jsonable_encoder(sensor)      
        data_sensor[sensor.id] = json_compatible_item_data
        return JSONResponse(content=json_compatible_item_data)
    else:
        return JSONResponse(status_code=403, content="Forbidden Request!")
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    print(data_sensor)
    return templates.TemplateResponse("item.html", {"request": request, "data_sensor":data_sensor})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

#Para la ejecucion
#uvicorn main:app --reload