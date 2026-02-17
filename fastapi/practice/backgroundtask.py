from fastapi import FastAPI,Query,Path
from pydantic import BaseModel
from fastapi import BackgroundTasks,Depends
from pydantic import BaseModel
from typing import Optional,Annotated
# anoted add the metadeta to perameter
app = FastAPI()


class Item(BaseModel):
    name: str =""
    id : int
    description : Optional[str] =None


def utility_background(task):
    print("executing in background")
@app.get("/")
def send_data(Backgroundtask : BackgroundTasks):
    Backgroundtask.add_task(utility_background,"task")

@app.get("/api/")
def send_data(q : Annotated[str,Query(max_length=50)]):
    pass

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of item", gt=0, le=1000)],
    q: str,
):

@app.post("/get-data/")
def send_background_task(item:Item):
    return item