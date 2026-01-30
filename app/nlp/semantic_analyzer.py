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

def analyze_email(text: str) -> dict:
    logger.info("Executando analyze_email (Modo Completo)")
    prompt = f"""
Você é um sistema de triagem de emails corporativos do setor financeiro.

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
        logger.info("JSON decodificado com sucesso em analyze_email")
        return data
    except Exception as e:
        logger.error(f"Erro ao decodificar JSON em analyze_email: {e}")
        raise

def analyze_email_with_intent_hint(text: str, intent_hint: str) -> dict:
    logger.info(f"Executando analyze_email_with_intent_hint | Hint: {intent_hint}")
    prompt = f"""
Você é um sistema de triagem de emails financeiros. 
Nossa inteligência local já classificou este email como: "{intent_hint}".

Sua tarefa é validar essa classificação e extrair os metadados.

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
        logger.info("JSON decodificado com sucesso em analyze_email_with_intent_hint")
        return data
    except Exception as e:
        logger.warning(f"Falha ao processar JSON com hint. Aplicando recuperação. Erro: {e}")
        return {
            "intent": intent_hint,
            "classificacao": "Produtivo",
            "stage": "em_andamento",
            "action": "resposta_padrao",
            "resposta_automatica": "Recebemos sua mensagem sobre "
        }