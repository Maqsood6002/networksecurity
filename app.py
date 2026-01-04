import os
import sys

import certifi

from networkSecurity.utils.mlUtils.model.estimator import NetworkModel
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")

import pymongo
from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.pipeline.trainingPipeline import trainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Request, UploadFile, requests
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networkSecurity.utils.mainUtils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networkSecurity.constant.trainingPipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME

database_name = client[DATA_INGESTION_DATABASE_NAME]
collection_name = database_name[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route_api():
    try:
        train_pipeline = trainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("finalModel/preprocessor.pkl")
        model=load_object("finalModel/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor, model=model)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        df['predicted_column']=y_pred
        df.to_csv("predictionOutput/output.csv")
        table_html=df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

if __name__=="__main__":
    try:
        app_run(app, host="localhost", port=8000)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e