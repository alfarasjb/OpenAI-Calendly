from openai import OpenAI

from src.definitions.credentials import EnvVariables, Credentials


class ChatModel:
    def __init__(self):
        self.chat_model = EnvVariables.chat_model()
        self.model = OpenAI(api_key=Credentials.openai_api_key())
        self.chat_history = []
        self.max_tokens = 4096
        self.system_prompt = ""

    def chat(self, user_prompt: str = "") -> str:
        hist_messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        user_message = {"role": "user", "content": user_prompt}
        self.chat_history.append(user_message)
        messages = hist_messages + self.chat_history[-4:]
        response = self.model.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            response_format={"type": "text"},
            max_tokens=self.max_tokens,
            temperature=0.5
        )

        message = response.choices[0].message.content
        self.chat_history.append(
            {"role": "assistant", "content": message}
        )
        return message


