from app.providers.gemini_provider import classify_zero_shot

LABELS = [
    "nova solicitacao",
    "resposta a solicitacao existente",
    "envio de documento",
    "confirmacao ou agradecimento",
    "duvida ou pergunta",
    "mensagem social",
    "marketing ou spam"
]

def classify_intent(text: str):
    return classify_zero_shot(text, LABELS)
