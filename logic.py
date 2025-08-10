from llm_axe import OllamaChat, Agent, OnlineAgent
from config import SMALL_MODEL, EXPERT_MODEL, CUSTOM_PROMPT

class ChatLogic:
    def __init__(self):
        self.llm_small = OllamaChat(model=SMALL_MODEL)
        self.llm_expert = OllamaChat(model=EXPERT_MODEL)
        self.searcher = OnlineAgent(self.llm_expert)
        self.small_agent = Agent(self.llm_small, custom_system_prompt=CUSTOM_PROMPT)
        self.expert_agent = Agent(self.llm_expert, custom_system_prompt=CUSTOM_PROMPT)
        self.expert_mode = False
        self.web_search_mode = False

    def toggle_expert(self):
        self.expert_mode = not self.expert_mode
        if not self.expert_mode:
            self.web_search_mode = False

    def toggle_web_search(self):
        if self.expert_mode:
            self.web_search_mode = not self.web_search_mode

    def process_message(self, message: str) -> str:
        if not self.expert_mode:
            return self.small_agent.ask(message)
        if self.web_search_mode:
            return self.searcher.search(message)
        return self.expert_agent.ask(message)