import os
import logging
import time
from typing import Dict, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from multiprocessing import Value, Lock

# Global rate limiting counters
API_CALL_COUNTER = Value('i', 0)
API_CALL_LOCK = Lock()

class TextSummarizer:
    def __init__(self, model_name: str = "llama-3.1-70b-versatile", max_retries: int = 3, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.max_retries = max_retries
        self.chain = self._initialize_chain()

    def _initialize_chain(self):
        """Initialize the Groq model and parser."""
        model = ChatGroq(model=self.model_name, api_key=self.api_key)
        parser = StrOutputParser()
        return model | parser

    def _get_session_history(self, session_id: str):
        """Initialize session history with SQLite."""
        return SQLChatMessageHistory(session_id, "sqlite:///chatbot_memory.db")

    def _handle_retry(self, attempt: int):
        """Handle retries with exponential backoff."""
        self.logger.info(f"Retrying... Attempt {attempt + 1}")
        time.sleep(2 ** attempt)

    def summarize_text(self, text: str, session_id: str = "default") -> Dict[str, Optional[str]]:
        """
        Summarize the provided text using the Groq model.
        
        Args:
            text (str): The text to summarize
            session_id (str): Unique identifier for the session
            
        Returns:
            dict: Contains the summarized text or None if failed
        """
        if not text:
            self.logger.error("No text provided for summarization")
            return {"summary": None, "error": "No text provided"}

        system_prompt = """You are a text summarization expert. Your task is to:
        1. Provide a concise summary of the main points in no more than 20 words.
        2. Keep the summary clear and well-structured.
        3. Maintain the key information while reducing length.
        4. Use professional language."""


        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Please summarize the following text:\n\n{text}")
        ]

        try:
            with API_CALL_LOCK:
                if API_CALL_COUNTER.value >= 30:  # Adjust based on your rate limit
                    self.logger.warning("Rate limit reached. Waiting...")
                    time.sleep(60)
                    API_CALL_COUNTER.value = 0
                API_CALL_COUNTER.value += 1

            runnable_with_history = RunnableWithMessageHistory(
                self.chain,
                self._get_session_history
            )
            
            for attempt in range(self.max_retries):
                try:
                    response = runnable_with_history.invoke(
                        messages,
                        config={"configurable": {"session_id": session_id}}
                    )
                    return {"summary": response, "error": None}
                except Exception as e:
                    self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == self.max_retries - 1:
                        return {"summary": None, "error": str(e)}
                    self._handle_retry(attempt)

        except Exception as e:
            self.logger.error(f"Summarization failed: {str(e)}")
            return {"summary": None, "error": str(e)}
        