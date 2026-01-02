from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.domain.models import ProductModel, FAQList

class QuestionGeneratorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(temperature=0.7, model="models/gemini-flash-latest")

    def generate(self, product: ProductModel) -> FAQList:
        """
        Generates FAQ items based on the product model using an LLM.
        """
        structured_llm = self.llm.with_structured_output(FAQList)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful content strategist. Generate 5-8 relevant, high-quality frequently asked questions and answers for the given product."),
            ("user", "Product: {product_name}\nDetails: {product_details}")
        ])
        chain = prompt | structured_llm
        return chain.invoke({
            "product_name": product.name,
            "product_details": product.model_dump_json()
        })
