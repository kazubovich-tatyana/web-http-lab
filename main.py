from fastapi import FastAPI

app = FastAPI(title="Notes API", version="0.1.0")

@app.get('/health')
def check_health():
  return {'status':'ok'}

@app.get('/hello')
def say_hello():
  return {"message": "Hello from Notes API"}