from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from elasticsearch import Elasticsearch
import os
from datetime import datetime

app = FastAPI()

ES_HOST = os.environ.get('ES_HOST', 'http://elasticsearch:9200')
es = Elasticsearch([ES_HOST])
INDEX_NAME = 'service-status'

class ServiceStatus(BaseModel):
    service_name: str
    service_status: str
    host_name: str
    timestamp: str

@app.post("/add")
async def add_status(status_data: ServiceStatus):
    try:
        doc = status_data.dict()
        doc['@timestamp'] = doc.pop('timestamp')
        res = es.index(index=INDEX_NAME, document=doc)
        return {"result": "created", "_id": res['_id']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthcheck")
async def healthcheck_all():
    try:
        expected_services = ['httpd', 'rabbitMQ', 'postgreSQL']
        
        overall_status = "UP"
        details = {}
        
        for service in expected_services:
            query = {
                "size": 1,
                "sort": [{"@timestamp": "desc"}],
                "query": {
                    "term": {"service_name.keyword": service}
                }
            }
            
            try:
                res = es.search(index=INDEX_NAME, body=query)
                hits = res['hits']['hits']
                
                if hits:
                    status = hits[0]['_source']['service_status']
                    details[service] = status
                    if status != "UP":
                        overall_status = "DOWN"
                else:
                    details[service] = "UNKNOWN"
                    overall_status = "DOWN"
            except Exception:
                 details[service] = "UNKNOWN"
                 overall_status = "DOWN"

        return {"status": overall_status, "details": details}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthcheck/{service_name}")
async def healthcheck_service(service_name: str):
    try:
        query = {
            "size": 1,
            "sort": [{"@timestamp": "desc"}],
            "query": {
                "term": {"service_name.keyword": service_name}
            }
        }
        
        res = es.search(index=INDEX_NAME, body=query)
        hits = res['hits']['hits']
        
        if hits:
            status = hits[0]['_source']['service_status']
            return {"service_name": service_name, "status": status}
        else:
            raise HTTPException(status_code=404, detail="Service status not found")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
