from llm_axe import OllamaChat, Agent, OnlineAgent
from config import SMALL_MODEL, EXPERT_MODEL, CUSTOM_PROMPT

class ChatLogic:
    def __init__(self):
        # Initialize small and expert language models
        self.llm_small = OllamaChat(model=SMALL_MODEL)
        self.llm_expert = OllamaChat(model=EXPERT_MODEL)
        # Online search agent using the expert model
        self.searcher = OnlineAgent(self.llm_expert)
        # Agents with custom system prompts for handling queries
        self.small_agent = Agent(self.llm_small, custom_system_prompt=CUSTOM_PROMPT)
        self.expert_agent = Agent(self.llm_expert, custom_system_prompt=CUSTOM_PROMPT)
        # Flags to track expert mode and web search mode
        self.expert_mode = False
        self.web_search_mode = False

    def toggle_expert(self):
        """
        Toggle expert mode on/off.
        Turning off expert mode also disables web search mode.
        """
        self.expert_mode = not self.expert_mode
        if not self.expert_mode:
            self.web_search_mode = False

    def toggle_web_search(self):
        """
        Toggle web search mode on/off.
        Only available if expert mode is enabled.
        """
        if self.expert_mode:
            self.web_search_mode = not self.web_search_mode

    def process_message(self, message: str) -> str:
        """
        Process an incoming message by selecting the appropriate agent based on the current modes.
        - If not in expert mode, use the small model agent.
        - If in expert mode and web search enabled, use the online search agent.
        - Otherwise, use the expert model agent.
        """
        if not self.expert_mode:
            return self.small_agent.ask(message)
        if self.web_search_mode:
            return self.searcher.search(message)
        return self.expert_agent.ask(message)