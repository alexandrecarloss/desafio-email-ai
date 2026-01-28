def classify_stage(text: str, features: dict):
    if features["has_thanks"] and not features["has_question"]:
        return "encerramento"
    if features["has_question"]:
        return "inicio"
    return "em_andamento"
