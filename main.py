from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ecdsa import SigningKey, BRAINPOOLP160r1, VerifyingKey

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
    cert: str

@app.post("/sensor")
async def upload_data(sensor:Sensor):
    certificado=sensor.cert
    # Controlar bloques de la firma
    try:
        ### ECDSA
        certificado=bytes.fromhex(certificado) # Decodicar verificador desde el sensor y comprobar la curva
        vk2 = VerifyingKey.from_string(certificado, curve=BRAINPOOLP160r1)    # Verificación para ver firma
        if vk2.to_string()==certificado:
            sensor.timestamp = datetime.now() 
            json_compatible_item_data   = jsonable_encoder(sensor)      
            data_sensor[sensor.id] = json_compatible_item_data
            return JSONResponse(content=json_compatible_item_data) # se muestra data en casa de ser aceptada la firma
        else:
            return JSONResponse(status_code=403, content="Forbidden Request!") # se indica que no tiene acceso y se informa para tener control y no desplegar infomación inadecuada de un sensor
    except Exception:
        return JSONResponse(status_code=403, content="Forbidden Request!")

@app.get("/", response_class=HTMLResponse)

async def read_item(request: Request):
    print(data_sensor)
    return templates.TemplateResponse("item.html", {"request": request, "data_sensor":data_sensor})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

#Para la ejecucion
#uvicorn main:app --reload