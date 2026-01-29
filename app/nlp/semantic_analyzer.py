import json
from app.providers.gemini_provider import generate_text_with_fallback

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
    return json.loads(raw)
