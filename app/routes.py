import logging
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from .core.pipeline import process_email 
import pdfplumber
import io
from google.genai.errors import ClientError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/processar-email")
async def processar_email_endpoint(
    texto: Optional[str] = Form(None),
    arquivo: Optional[UploadFile] = File(None)
):
    conteudo = ""
    
    if arquivo:
        filename = arquivo.filename.lower()
        bytes_content = await arquivo.read()
        if filename.endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(bytes_content)) as pdf:
                conteudo = "\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
        else:
            conteudo = bytes_content.decode("utf-8")
    elif texto:
        conteudo = texto

    if not conteudo:
        return JSONResponse(status_code=400, content={"erro": "Nenhum conteúdo enviado."})

    try:
        resultado = process_email(conteudo) 

        return {
            "intent": resultado["intent"],
            "classificacao": resultado["classificacao"],
            "estagio": resultado["stage"],
            "acao": resultado["action"],
            "resposta_automatica": resultado["resposta_automatica"]
        }
    except Exception as e:
        print(f"ERRO: {str(e)}")
        return JSONResponse(status_code=500, content={"erro": str(e)})