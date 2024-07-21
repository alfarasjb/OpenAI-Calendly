import streamlit as st
from src.app.chat import Chat


class AppointmentSetterApp:
    def __init__(self):
        self.chat = Chat()

    @staticmethod
    def _initialize_app():
        st.set_page_config(page_title="Appointment Setter", layout='centered')

    def _home_screen(self):
        self.chat.chat_box()

    def main(self):
        self._home_screen()
