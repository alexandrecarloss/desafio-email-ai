from app.providers.gemini_provider import generate_text

def generate_response(intent: str, stage: str, action: str):
    prompt = f"""
Você é um assistente de suporte por e-mail profissional de uma empresa financeira.
Sua tarefa é escrever a resposta final que será enviada ao cliente.

REGRAS CRÍTICAS:
1. Retorne APENAS o texto da resposta.
2. NÃO inclua saudações como "Aqui está sua resposta" ou "Sugestão:".
3. NÃO use aspas, markdown ou explicações.
4. Use um tom profissional e cordial.

CONTEXTO:
Intenção do cliente: {intent}
Estágio do atendimento: {stage}
Ação decidida pelo sistema: {action}

RESPOSTA FINAL:
"""
    return generate_text(prompt)
