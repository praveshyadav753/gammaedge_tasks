from fastapi import FastAPI,BackgroundTasks
import asyncio 
import httpx

app = FastAPI()

async def fetchdata():
        async with httpx.AsyncClient() as client:
                await asyncio.sleep(3)
                response = await client.get('https://api.restful-api.dev/objects')
                print(response.text,"hello")


@app.get('/')
async def fetch(background_tasks: BackgroundTasks):
        background_tasks.add_task(fetchdata)
        return {"msg": "data fetched "}
