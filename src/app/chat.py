import streamlit as st
from src.services.chat import ChatModel


class Chat:
    def __init__(self):
        self.chat_model = ChatModel()

    def chat_box(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [
                dict(role="assistant", content=f"Hello. How can i help you today?")
            ]
        print(st.session_state.messages)
        # Display chat messages from history on app rerun.
        for message in st.session_state.messages:
            st.chat_message(message['role']).write(message['content'])

        if prompt := st.chat_input("Say something"):
            st.chat_message("user").write(prompt)
            user_message = dict(role="user", content=prompt)
            st.session_state.messages.append(user_message)
            bot_response = self.chat_model.chat(prompt)
            if bot_response:
                st.chat_message("assistant").write(bot_response)
                bot_message = dict(role="assistant", content=bot_response)
                st.session_state.messages.append(bot_message)
