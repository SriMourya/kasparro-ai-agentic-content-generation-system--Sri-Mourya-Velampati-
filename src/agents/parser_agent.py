import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.domain.models import ProductModel

class ParserAgent:
    def __init__(self):
        # Ensure GOOGLE_API_KEY is set in environment
        self.llm = ChatGoogleGenerativeAI(temperature=0, model="models/gemini-flash-latest")

    def parse(self, raw_data: dict) -> ProductModel:
        """
        Parses raw dictionary data into a structured ProductModel using an LLM.
        """
        structured_llm = self.llm.with_structured_output(ProductModel)
        
        # Convert dict to string for the prompt
        text_data = json.dumps(raw_data, indent=2)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert product data parser. Extract structured product data from the provided raw text/json. Ensure all fields are correctly mapped."),
            ("user", "{input}")
        ])
        chain = prompt | structured_llm
        return chain.invoke({"input": text_data})
