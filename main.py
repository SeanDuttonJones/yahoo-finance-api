from Scrape import Scrape
from requests import HTTPError, TooManyRedirects
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import json

app = FastAPI()

elements_to_scrape = {}

@app.on_event("startup")
def startup():
    f = open("scrape.json")
    data = f.read()
    f.close()
    global elements_to_scrape
    elements_to_scrape = json.loads(data)


@app.get("/root")
def root():
    return "Hello World!"

@app.get("/v1/{symbol}/summary/")
def summary(symbol, q: Optional[List[str]] = Query(None)):
    summary_data = {}
    try:
        s = Scrape(symbol, elements_to_scrape)
        summary_data = s.summary()
        if all (k in summary_data for k in q): # if all query parameters are keys in summary_data
            summary_data = {key: summary_data[key] for key in q} # summary_data becomes requested key-value pairs
        # else, return entire summary

    except TooManyRedirects:
        raise HTTPException(status_code=404, detail="{symbol} doesn't exist or cannot be found.")
    except HTTPError:
        raise HTTPException(status_code=500)

    return summary_data