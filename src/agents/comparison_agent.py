from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.domain.models import ProductModel, ComparisonResult

class ComparisonAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(temperature=0.5, model="models/gemini-flash-latest")

    def compare(self, product_a: ProductModel, product_b: ProductModel) -> ComparisonResult:
        """
        Generates a comparison between two products using an LLM.
        """
        structured_llm = self.llm.with_structured_output(ComparisonResult)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert product reviewer. Compare the two products based on their specs and benefits. Be objective but highlight the strengths of Product A."),
            ("user", "Product A: {product_a_json}\n\nProduct B: {product_b_json}")
        ])
        chain = prompt | structured_llm
        return chain.invoke({
            "product_a_json": product_a.model_dump_json(),
            "product_b_json": product_b.model_dump_json()
        })
