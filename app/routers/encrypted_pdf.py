from fastapi import APIRouter, UploadFile, HTTPException, Form, File
import os
from PyPDF2 import PdfReader, PdfWriter
from typing import List
import glob

router = APIRouter(
    prefix=("/mogui-pdf"),
    tags=["Encriptador de PDF"]
)

@router.post("/encriptar-pdf")
async def encrypted_pdf(files: List[UploadFile] = File(...), folder: str = Form(None), password: str = Form(...)):
    # Verifico si se proporcionaron archivos o una carpeta
    if not files and not folder:
        raise HTTPException(status_code=400, detail="No se proporcionaron archivos PDF ni carpeta.")
    
    # Creo una carpeta temporal para guardar los archivos encriptados
    temp_folder = "/Users/guzmanbluis/Documents/moguipdf_temporal"
    os.makedirs(temp_folder, exist_ok=True)

    encrypted_files = []

    try:
        # Proceso de encriptación para archivos individuales
        for file in files:
            if file.filename.lower().endswith(".pdf"):
                reader = PdfReader(file.file)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                writer.encrypt(password)

                encrypted_file = os.path.join(temp_folder, f"encriptado_{file.filename}")
                with open(encrypted_file, "wb") as f:
                    writer.write(f)

                encrypted_files.append(encrypted_file)

        # Proceso de encriptación para archivos dentro de una carpeta
        if folder:
            pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
            for pdf_file in pdf_files:
                reader = PdfReader(pdf_file)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                writer.encrypt(password)

                encrypted_file = os.path.join(temp_folder, f"encriptado_{os.path.basename(pdf_file)}")
                with open(encrypted_file, "wb") as f:
                    writer.write(f)

                encrypted_files.append(encrypted_file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante el proceso de encriptación: {str(e)}")

    return {"archivos_encriptados": encrypted_files}
