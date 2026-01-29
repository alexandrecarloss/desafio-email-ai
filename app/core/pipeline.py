import logging
from app.nlp.semantic_analyzer import analyze_email
from app.nlp.feature_extractor import extract_features

logger = logging.getLogger(__name__)

def process_email(text: str):
    features = extract_features(text)
    
    try:
        result = analyze_email(text)
    except Exception as e:
        logger.error(f"Falha na IA: {e}")
        return {
            "intent": "indefinido",
            "classificacao": "Indisponível",
            "stage": "N/A",
            "action": "resposta_padrao",
            "resposta_automatica": "Não foi possível processar sua mensagem no momento."
        }

    logger.info(
        f"Processado: {result['intent']} | {result['classificacao']} | {result['action']}"
    )

    return result