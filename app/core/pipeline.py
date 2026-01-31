import logging
from app.nlp.semantic_analyzer import analyze_email, analyze_email_with_intent_hint
from app.nlp.feature_extractor import extract_features
from app.ml.intent_predictor import predict_intent

logger = logging.getLogger(__name__)

def fallback_response(intent):
    return {
        "intent": intent,
        "classificacao": "Indisponível",
        "stage": "N/A",
        "action": "resposta_padrao",
        "resposta_automatica": (
            "Não foi possível processar sua mensagem no momento. "
            "Nossa equipe analisará manualmente."
        )
    }

TERMINAL_INTENTS = {
    "confirmacao ou agradecimento",
    "mensagem social"
}

def is_terminal_message(features: dict) -> bool:
    return (
        features["has_thanks"]
        and not features["has_question"]
        and features["length"] < 300
    )

def process_email(text: str):
    logger.info(f"Iniciando processamento de email. Tamanho: {len(text)} caracteres")

    features = extract_features(text)
    intent, confidence = predict_intent(text)

    logger.info(
        f"ML Predict: Intent={intent} | Confidence={confidence:.4f} | Features={features}"
    )

    try:
        if intent in TERMINAL_INTENTS and is_terminal_message(features):
            logger.info("Mensagem terminal detectada via regras determinísticas")

            return {
                "intent": intent,
                "classificacao": "Improdutivo",
                "stage": "encerramento",
                "action": "ignorar_ou_arquivar",
                "resposta_automatica": ""
            }

        if confidence >= 0.85:
            logger.info("Alta confiança ML — usando LLM com hint")
            result = analyze_email_with_intent_hint(text, intent)
        else:
            logger.info("Baixa confiança ML — usando LLM zero-shot")
            result = analyze_email(text)

        logger.info(
            f"Resultado final: Intent={result.get('intent')} | Action={result.get('action')}"
        )
        return result

    except Exception as e:
        logger.error("Erro crítico no processamento", exc_info=True)
        return fallback_response(intent)
