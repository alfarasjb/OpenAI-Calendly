from typing import Optional

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.tools.render import format_tool_to_openai_function
from langchain_openai import ChatOpenAI

from src.definitions.credentials import Credentials, EnvVariables
from src.utils.llm_functions import TOOLS
import logging

logger = logging.getLogger(__name__)


# TODO: History seems to not work properly.
# TODO: System prompt


class ChatModel:
    def __init__(self):
        self.tools = TOOLS  # Add tools here
        self.functions = [format_tool_to_openai_function(f) for f in self.tools]
        self.model = self.init_chat_model()
        self.memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.chain = RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_openai_functions(x['intermediate_steps'])
        ) | self.prompt | self.model | OpenAIFunctionsAgentOutputParser()
        self.qa = AgentExecutor(agent=self.chain, tools=self.tools, verbose=False, memory=self.memory)

    def init_chat_model(self) -> ChatOpenAI:
        logger.info(f"Initializing chat model. Model: {EnvVariables.chat_model()}")
        return ChatOpenAI(
            model=EnvVariables.chat_model(),
            temperature=0.7,
            api_key=Credentials.openai_api_key(),
            functions=self.functions
        )

    def chat(self, user_prompt: str) -> Optional[str]:
        logger.info(f"User Chat: {user_prompt}")
        if not user_prompt:
            return
        result = self.qa.invoke({"input": user_prompt})
        answer = result['output']
        logger.info(f"AI Response: {answer}")
        return answer
