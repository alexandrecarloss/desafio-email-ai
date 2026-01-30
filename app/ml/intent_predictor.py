import joblib
import os
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = "app/models/intent_classifier.joblib"

if not os.path.exists(MODEL_PATH):
    logger.error(f"Arquivo de modelo não encontrado em: {MODEL_PATH}")
    raise FileNotFoundError(f"Execute o treino primeiro.")

pipeline = joblib.load(MODEL_PATH)

def predict_intent(text: str):
    if not text or len(text.strip()) < 3:
        return "mensagem social", 0.0

    probs = pipeline.predict_proba([text])[0]
    best_idx = probs.argmax()
    confidence = probs[best_idx]
    intent = pipeline.classes_[best_idx]

    logger.info(f"ML Predict: Text_Snippet='{text[:30]}...' | Label={intent} | Conf={confidence:.4f}")
    
    return intent, float(confidence)