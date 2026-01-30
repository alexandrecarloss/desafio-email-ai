import logging
from app.nlp.semantic_analyzer import analyze_email, analyze_email_with_intent_hint
from app.nlp.feature_extractor import extract_features
from app.ml.intent_predictor import predict_intent

logger = logging.getLogger(__name__)

def fallback_response():
    return {
        "intent": "indefinido",
        "classificacao": "Indisponível",
        "stage": "N/A",
        "action": "resposta_padrao",
        "resposta_automatica": (
            "Não foi possível processar sua mensagem no momento. "
            "Nossa equipe analisará manualmente."
        )
    }

def process_email(text: str):
    logger.info(f"Iniciando processamento de email. Tamanho: {len(text)} caracteres")
    features = extract_features(text)
    
    intent, confidence = predict_intent(text)
    logger.info(f"ML Predict: Intent={intent} | Confidence={confidence:.4f}")

    try:
        if confidence >= 0.75:
            logger.info(f"Alta confiança detectada. Usando analyze_email_with_intent_hint")
            result = analyze_email_with_intent_hint(text, intent)
        else:
            logger.info(f"Baixa confiança ({confidence:.2f}). Usando analyze_email (Zero-shot)")
            result = analyze_email(text)

        logger.info(f"Resultado final: Intent={result.get('intent')} | Action={result.get('action')}")
        return result

    except Exception as e:
        logger.error(f"Erro crítico no processamento: {str(e)}", exc_info=True)
        return fallback_response()