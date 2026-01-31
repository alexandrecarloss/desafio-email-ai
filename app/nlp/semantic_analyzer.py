import json
import logging
from app.providers.gemini_provider import generate_text_with_fallback

logger = logging.getLogger(__name__)

LABELS = [
    "nova solicitacao",
    "resposta a solicitacao existente",
    "envio de documento",
    "confirmacao ou agradecimento",
    "duvida ou pergunta",
    "mensagem social",
    "marketing ou spam"
]

TERMINAL_INTENTS = {
    "mensagem social",
    "confirmacao ou agradecimento"
}

DEFAULT_RESPONSES = {
    "abrir_chamado": "Recebemos sua solicitação e abrimos um chamado. Nossa equipe retornará em breve.",
    "atualizar_chamado": "Sua solicitação já está em andamento. Em breve enviaremos uma atualização do status.",
    "anexar_documento": "Documento recebido com sucesso. Seguiremos com a análise.",
    "analisar_suporte": "Estamos analisando sua solicitação. Retornaremos o mais breve possível.",
    "arquivar": "Mensagem registrada. Nenhuma ação adicional é necessária no momento.",
    "ignorar_ou_arquivar": "Mensagem recebida. Não é necessária nenhuma ação adicional.",
    "resposta_padrao": "Recebemos sua mensagem e em breve retornaremos."
}


def ensure_response(result: dict) -> dict:
    action = result.get("action")
    if not result.get("resposta_automatica"):
        result["resposta_automatica"] = DEFAULT_RESPONSES.get(
            action,
            "Recebemos sua mensagem."
        )
    return result


def sanitize_llm_result(result: dict) -> dict:
    if result.get("intent") in TERMINAL_INTENTS:
        result["classificacao"] = "Improdutivo"
        result["stage"] = "encerramento"
        result["action"] = "ignorar_ou_arquivar"
        result["resposta_automatica"] = ""

    return ensure_response(result)


def analyze_email(text: str) -> dict:
    logger.info("Executando analyze_email (Modo Completo)")
    prompt = f"""
Você é um sistema de triagem de emails corporativos do setor financeiro.

REGRAS DE NEGÓCIO (OBRIGATÓRIAS):
- Emails classificados como "mensagem social" ou "confirmacao ou agradecimento" são SEMPRE:
  - classificacao: Improdutivo
  - stage: encerramento
  - action: ignorar_ou_arquivar
  - resposta_automatica: ""

- Gere resposta apenas quando necessário.

TAREFAS:
1. Classifique o email em UMA das categorias abaixo:
{LABELS}

2. Determine se o email é:
- Produtivo
- Improdutivo

3. Determine o estágio do atendimento:
- inicio
- em_andamento
- encerramento

4. Defina a ação do sistema:
- abrir_chamado
- atualizar_chamado
- anexar_documento
- analisar_suporte
- arquivar
- ignorar_ou_arquivar
- resposta_padrao

5. Gere a resposta automática final (se aplicável).

REGRAS IMPORTANTES:
- Retorne APENAS JSON válido
- Não use markdown
- Não use texto fora do JSON

FORMATO EXATO:
{{
  "intent": "",
  "classificacao": "",
  "stage": "",
  "action": "",
  "resposta_automatica": ""
}}

EMAIL:
{text}
"""
    raw = generate_text_with_fallback(prompt)
    logger.debug(f"Resposta bruta Gemini (analyze_email): {raw}")

    try:
        data = json.loads(raw)
        data = sanitize_llm_result(data)
        logger.info("JSON decodificado com sucesso em analyze_email")
        return data
    except Exception as e:
        logger.error(f"Erro ao decodificar JSON em analyze_email: {e}")
        raise

def analyze_email_with_intent_hint(text: str, intent_hint: str) -> dict:
    logger.info(f"Executando analyze_email_with_intent_hint | Hint: {intent_hint}")
    prompt = f"""
Você é um sistema de triagem de emails financeiros.

REGRAS DE NEGÓCIO (OBRIGATÓRIAS):
- Emails classificados como "mensagem social" ou "confirmacao ou agradecimento" são SEMPRE:
  - classificacao: Improdutivo
  - stage: encerramento
  - action: ignorar_ou_arquivar
  - resposta_automatica: ""

- Gere resposta apenas quando necessário.

Nossa inteligência local já classificou este email como: "{intent_hint}".

FORMATO EXATO DE RETORNO (JSON APENAS):
{{
  "intent": "{intent_hint}",
  "classificacao": "Produtivo ou Improdutivo",
  "stage": "inicio, em_andamento ou encerramento",
  "action": "abrir_chamado, atualizar_chamado, anexar_documento, analisar_suporte, arquivar ou resposta_padrao",
  "resposta_automatica": "texto da resposta"
}}

EMAIL:
{text}
"""
    raw = generate_text_with_fallback(prompt)
    logger.debug(f"Resposta bruta Gemini (with_hint): {raw}")

    try:
        data = json.loads(raw)
        data = sanitize_llm_result(data)
        logger.info("JSON decodificado com sucesso em analyze_email_with_intent_hint")
        return data
    except Exception as e:
        logger.warning(f"Falha ao processar JSON com hint. Aplicando recuperação. Erro: {e}")
        return ensure_response({
            "intent": intent_hint,
            "classificacao": "Improdutivo",
            "stage": "encerramento",
            "action": "ignorar_ou_arquivar",
            "resposta_automatica": ""
        })
