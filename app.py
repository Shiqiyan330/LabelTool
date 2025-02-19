# app.py
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/data/{index}")
async def get_data(index: int):
    df = pd.read_csv('data.csv')
    if 0 <= index < len(df):
        record = df.iloc[index].to_dict()
        return record
    return {"error": "Index out of range"}

@app.post("/data/{index}")
async def update_data(index: int, content: dict):
    df = pd.read_csv('data.csv')
    if 0 <= index < len(df):
        for key, value in content.items():
            df.at[index, key] = value
        df.to_csv('data.csv', index=False)
        return {"message": "Record updated successfully"}
    return {"error": "Index out of range"}