from app.config import GEMINI_API_KEY
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_text(prompt: str) -> str:
    response = client.models.generate_content(
        # model="gemini-3-flash-preview", 
        model="gemini-2.5-flash", 
        # model="gemini-2.5-flash-lite", 
        contents=prompt
    )
    return response.text.strip()

def classify_zero_shot(text: str, labels: list) -> str:
    prompt = f"""
    Classifique o texto abaixo em APENAS UMA das seguintes categorias: {labels}

    REGRAS:
    - Responda apenas com o nome da categoria, exatamente como escrita acima.
    - Não use pontuação ou palavras extras.

    TEXTO:
    {text}
    """
    return generate_text(prompt)

