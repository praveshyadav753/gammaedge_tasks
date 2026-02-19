from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse
# from llm.app.app import app
from uuid import uuid4
import logging
import time
import asyncio


logger = logging.getLogger(__name__)
# @app.middleware('http')
async def cust_logging(request:Request,call_next):
    starttime = time.time()
    request_id = uuid4()
    request_endpoint = request.url
    response = await call_next(request)
    process_time = time.time() - starttime

    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = str(request_id)
    response.headers["X-Endpoint"] = str(request_endpoint)  
    
    logger.info(f"Request-Id: {request_id}|Process-Time:{process_time} |Endpoint:{request_endpoint}")
    return response

class RequestTimeoutException(HTTPException):
    def __init__(self):
        super().__init__(status_code=408, detail="Request processing time exceeded the 30-second limit")

async def timeout_middlewar(request:Request,call_next):
    try:
        response = await asyncio.wait_for(
            call_next(request),
            timeout=120
        )
        return response

    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"detail": "Request timeout"},
        )
        

