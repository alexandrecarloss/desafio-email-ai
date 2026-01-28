class LLMProvider:
    def generate(self, prompt: str):
        raise NotImplementedError

    def classify(self, text: str, labels: list):
        raise NotImplementedError
