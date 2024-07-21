import json

from openai import OpenAI
from src.definitions.credentials import EnvVariables, Credentials
from src.utils.llm_functions import TOOLS
from src.services.calendly import Calendly


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
            max_tokens=self.max_tokens,
            temperature=0.5,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        # Must add this. Otherwise, openai will throw a BadRequestError
        messages.append(response_message)
        print(messages)

        tool_calls = response_message.tool_calls
        if tool_calls:
            tool_call_id = tool_calls[0].id
            tool_function_name = tool_calls[0].function.name
            func_dict = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_function_name
            }
            results = None

            if tool_function_name == 'get_availability':
                results = json.dumps(Calendly().list_user_availability_schedules())
            else:
                print("Function does not exist")
                return
            if results:
                func_dict.update({"content": results})
                messages.append(func_dict)
                model_response_with_function_call = self.model.chat.completions.create(
                    model=self.chat_model,
                    messages=messages
                )
                return model_response_with_function_call.choices[0].message.content

        else:
            return response_message.content
