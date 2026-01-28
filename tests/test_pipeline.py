from app.core.pipeline import process_email

def test_email_flow():
    result = process_email("Obrigado, problema resolvido.")
    assert result["stage"] == "encerramento"
