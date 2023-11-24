from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key)

    def complete(self, model, messages) -> str:
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return completion.choices[0].message.content
