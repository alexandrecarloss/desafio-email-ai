import logging
from app.nlp.feature_extractor import extract_features
from app.nlp.intent_classifier import classify_intent
from app.nlp.stage_classifier import classify_stage
from app.core.decision_engine import decide_action
from app.nlp.response_generator import generate_response

logger = logging.getLogger(__name__)

def process_email(text: str):
    features = extract_features(text)
    intent = classify_intent(text) 
    stage = classify_stage(text, features)
    action = decide_action(intent, stage)
    
    produtivo_labels = ["nova solicitacao", "resposta a solicitacao existente", "envio de documento", "duvida ou pergunta"]
    status_frontend = "Produtivo" if intent in produtivo_labels else "Improdutivo"

    if status_frontend == "Improdutivo":
        reply = "Nenhuma resposta automática necessária para este tipo de mensagem."
        action = "ignorar_ou_arquivar"
    else:
        reply = generate_response(intent, stage, action)

    logger.info(f"Processado: {intent} -> {action} ({status_frontend})")

    return {
        "intent": intent,
        "classificacao": status_frontend,
        "stage": stage,
        "action": action,
        "resposta_automatica": reply
    }