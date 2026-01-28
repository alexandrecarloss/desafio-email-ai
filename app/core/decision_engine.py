import logging

logger = logging.getLogger(__name__)

DECISION_TABLE = {
    ("resposta a solicitacao existente", "em_andamento"): "atualizar_chamado",
    ("nova solicitacao", "inicio"): "abrir_chamado",
    ("duvida ou pergunta", "inicio"): "analisar_suporte",
    ("confirmacao ou agradecimento", "encerramento"): "arquivar",
    ("envio de documento", "em_andamento"): "anexar_documento",
    ("mensagem social", "encerramento"): "arquivar",
    ("mensagem social", "em_andamento"): "arquivar",
}

def decide_action(intent: str, stage: str):
    action = DECISION_TABLE.get((intent, stage))
    if not action:
        if intent in ["mensagem social", "marketing ou spam"]:
            return "arquivar"
            
        logger.warning(f"Combinação não mapeada: {intent} | {stage}")
        return "resposta_padrao"
    return action