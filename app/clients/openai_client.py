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

    def speak(self, id, message):
        from pathlib import Path

        speech_file_path = Path(__file__).parent.parent / f"public/{id}.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=message
        )
        response.stream_to_file(speech_file_path)
