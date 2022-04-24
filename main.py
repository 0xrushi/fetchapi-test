from typing import Optional
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd

# Fast API application to manage API
app = FastAPI()

# Player Points Database
df = pd.DataFrame({
    "payer":[],
    "points":[],
    "timestamp":[]
})

# Database of points remaining after spend
persondf = pd.DataFrame()

# Transaction Schema
class Item(BaseModel):
    payer: str
    points: int
    timestamp: Optional[datetime] = None

# GET transactions endpoint
# Show player points database
@app.get("/transactions")
def read_root():
    global df
    return df.to_dict('records')

# POST add endpoint
# Add a transaction to points database
@app.post("/add")
async def create_item(item: Item):
    global df
    if not item.timestamp:
        item.timestamp = datetime.now()
    points_single_record = pd.DataFrame([[item.payer, item.points, item.timestamp]], columns=df.columns)
    df = pd.concat([points_single_record, df])
    return {'messsage': 'Added Successfully', 'payload': item}

# Testing example endpoint
# To initialize the points database
# Use by developer only
@app.get("/init")
def initdf():
    init()

# Spend Endpoint
# Amount of points to be spent
@app.post("/spend")
async def spend(request: Request):
    global df
    global persondf
    persondf = pd.DataFrame()
    df = df.sort_values(by='timestamp')
    persondf = df.groupby('payer')['points'].sum()
    persondf = persondf.to_frame()
    persondf_cpy = persondf.copy()
    amt = await request.json()
    amt = int(amt["points"])
    for row in df.iterrows():
        tpt = row[1]['points']
        tpayer = row[1]['payer']
        if amt > 0 and amt >= tpt:
            amt -= tpt
            persondf.loc[tpayer, 'points'] -= tpt
        elif amt > 0:
            persondf.loc[tpayer, 'points'] -= amt
            amt = 0
    if amt==0:
        return (persondf-persondf_cpy).reset_index().to_dict('records')
    else: 
        return {'message': 'Spend amount error'}

# pointsbalance endpoint
# Subsequent call to this endpoint after calling spend
# gives the points balance.
@app.get("/pointsbalance")
def getpoints():
    return persondf.reset_index().to_dict('records')
def init():
    global df
    items = [
    { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]
    for item in items:
        df2 = pd.DataFrame([[item['payer'], item['points'], item['timestamp']]], columns=df.columns)
        df = pd.concat([df2, df])