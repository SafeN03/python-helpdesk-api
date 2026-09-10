from fastapi import FastAPI

app = FastAPI(title="Python Helpdesk API")

@app.get("/health")

def health_check():

    return {"status": "ok"}