from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

data_sensor = {}

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

class Sensor(BaseModel):
    id: str
    timestamp: None | datetime
    temp: str

@app.post("/sensor")
async def upload_data(sensor:Sensor):
    sensor.timestamp = datetime.now()
    json_compatible_item_data = jsonable_encoder(sensor)      
    data_sensor[sensor.id] = json_compatible_item_data
    return JSONResponse(content=json_compatible_item_data)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    print(data_sensor)
    return templates.TemplateResponse("item.html", {"request": request, "data_sensor":data_sensor})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

#Para la ejecucion
#uvicorn main:app --reload