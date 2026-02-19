import fastapi from  FastAPI,Request
import time 





@app.midddleware("http")
def mymiddleware(request: Request, call_next):

    # at time of request
    response = await call_next(request)
    # at time of response

    return response