from fastapi import FastAPI
from backend.routers import operadoras, despesas, estatisticas


app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(operadoras.router, prefix="/api")
app.include_router(despesas.router, prefix="/api")
app.include_router(estatisticas.router, prefix="/api")