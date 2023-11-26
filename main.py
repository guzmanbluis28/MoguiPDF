from fastapi import FastAPI
import uvicorn
from app.routers import encrypted_pdf

app = FastAPI(
title="MoguiPDF",
version="0.1.0",
description="Esta API contiene rutas para manipulación de PDF´s, inicialmente para encriptar y en siguientes versiones contará con más funciones",
contact={"nombre":"Luis Guzmán", "email":"guzmanbluis@gmail.com"},


)
app.include_router(encrypted_pdf.router)


if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)