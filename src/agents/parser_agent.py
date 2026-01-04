import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.domain.models import ProductModel
from src.core.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

class ParserAgent:
    def __init__(self):
        # Ensure GOOGLE_API_KEY is set in environment
        self.llm = ChatGoogleGenerativeAI(temperature=0, model="models/gemini-flash-latest")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _call_llm(self, chain, input_data):
        return chain.invoke(input_data)

    def parse(self, raw_data: dict) -> ProductModel:
        """
        Parses raw dictionary data into a structured ProductModel using an LLM.
        """
        logger.info("Parsing raw product data")
        structured_llm = self.llm.with_structured_output(ProductModel)
        
        # Convert dict to string for the prompt
        text_data = json.dumps(raw_data, indent=2)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert product data parser. Extract structured product data from the provided raw text/json. Ensure all fields are correctly mapped."),
            ("user", "{input}")
        ])
        chain = prompt | structured_llm
        
        try:
            return self._call_llm(chain, {"input": text_data})
        except Exception as e:
            logger.error("Failed to parse product data", exc_info=True)
            raise e
