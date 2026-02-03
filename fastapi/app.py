from fastapi import FastAPI,Depends,Response
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine,Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker,Session,declarative_base
import time
import requests
import httpx
import asyncio
import jwt



app = FastAPI()
app.title = "My FastAPI Application"
app.version = "1.0.0"
app.description = "This is a sample FastAPI application the understand the fastapi."


SQL_URL= "postgresql://postgres:XfJbolIxbIDekzeJnjjollhlDHTBkIJm@tramway.proxy.rlwy.net:46595/railway"
engine = create_engine(SQL_URL)
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base=declarative_base()
def get_db():
    db=LocalSession()
    try:
        yield db
    except Exception as e:
        print("database connection failed",e)    
    finally:
        db.close()     

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    comments = Column(Text, nullable=True) 
Base.metadata.create_all(bind=engine)


class Item(BaseModel):
    name:str
    description:str=None
    comments:str=None
    id:int=None
    
@app.get("/")
def start():
    # get_db()
    return {"message":"Hello World"}

@app.get("/items/{item_id}")
def get_item(item_id:int,db: Session = Depends(get_db)):
    data= db.query(ItemModel).filter(ItemModel.id==item_id).first()
    return {"item_id":item_id,"message":"Item fetched successfully","data": data}

@app.get("/items/")
def get_filtered_items(item_id:int=0,limit:int=10,sort:Optional[str]=None):
    return {"item_id":item_id,"limit":limit,"message":"Filtered items fetched successfully"}



@app.post("/items/")
def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = ItemModel(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
@app.get("/sync")
def sync_task():
    return  blocking_fetch_urls(["https://jsonplaceholder.typicode.com/todos/1","https://api.restful-api.dev/objects","https://api.restful-api.dev/objects?id=3&id=5&id=10"])

@app.get("/async")  
async def async_f():
    call= await background_task()
    q= await nonblocking_fetch_urls(["https://jsonplaceholder.typicode.com/todos/1","https://api.restful-api.dev/objects","https://api.restful-api.dev/objects?id=3&id=5&id=10"])
    
    return q,call


def blocking_fetch_urls(urls):
    results = []
    start_time = time.time()
    
    for url in urls:
        try:
            print(f"Fetching {url}")
            response =  requests.get(url)
            
            results.append({
                'url': url,
                'status': response.status_code,
                'length': len(response.text),
                'data':response.text,

            })
            print("success" )
        except Exception as e:
            results.append({
                'url': url,
                'error': str(e)
            })
    
    return results    


async def nonblocking_fetch_urls(urls):
    results = []
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                print(f"Fetching {url}")
                response = await client.get(url)
                print(response.status_code or "next")
                results.append({
                    'url': url,
                    'status': response.status_code,
                    'length': len(response.text),
                    'data':response.text,

                })
                print("success" )
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
        
        return results      
async def background_task():
    for i in range(5):
        print(f"Background task running {i}")
        await asyncio.sleep(1)  # simulate work        