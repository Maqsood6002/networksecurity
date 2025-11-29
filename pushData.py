import os
import sys
import json

import pandas as pd
import numpy as np
import pymongo
from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

import certifi
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("MONGO_URI not found in environment variables.")
    sys.exit(1)

ca=certifi.where()

class networkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            json_data = df.to_dict(orient='records')
            return json_data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def push_data_to_mongo(self, records, database, collection):
        try:
            self.data=records
            self.database_name=database
            self.collection_name=collection

            client = pymongo.MongoClient(MONGO_URI, tlsCAFile=ca)
            db = client[database]
            collection = db[collection]
            if isinstance(records, list):
                collection.insert_many(records)
            else:
                collection.insert_one(records)
            logging.info(f"Data pushed to MongoDB database: {database}, collection: {collection}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    file_path="NetworkData\phisingData.csv"
    Database="NetworkSecurity"
    Collection="NetworkData"
    networkobj=networkDataExtract()
    records=networkobj.csv_to_json(file_path)
    print(records)
    no_of_records=networkobj.push_data_to_mongo(records,Database,Collection)
    print(f"No of records inserted: {no_of_records}")