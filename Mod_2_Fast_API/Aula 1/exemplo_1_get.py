from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Exemplo 1 - FastAPI",
    description="Exemplo de aplicação FastAPI com Agno",
    version="0.1.0",
    contact={
        "name": "Agno",
        "email": "juvenalculino@gmail.com"
        }
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello, {name}!"} 

if __name__ == "__main__":
    uvicorn.run("exemplo_1_get:app", host="0.0.0.0", port=8000, reload=True)
     