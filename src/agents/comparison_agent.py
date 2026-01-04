from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.domain.models import ProductModel, ComparisonResult
from src.core.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

class ComparisonAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(temperature=0.5, model="models/gemini-flash-latest")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _call_llm(self, chain, input_data):
        return chain.invoke(input_data)

    def compare(self, product_a: ProductModel, product_b: ProductModel) -> ComparisonResult:
        """
        Generates a comparison between two products using an LLM.
        """
        logger.info(f"Comparing {product_a.name} vs {product_b.name}")
        structured_llm = self.llm.with_structured_output(ComparisonResult)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert product reviewer. Compare the two products based on their specs and benefits. Be objective but highlight the strengths of Product A."),
            ("user", "Product A: {product_a_json}\n\nProduct B: {product_b_json}")
        ])
        
        chain = prompt | structured_llm
        
        try:
            return self._call_llm(chain, {
                "product_a_json": product_a.model_dump_json(),
                "product_b_json": product_b.model_dump_json()
            })
        except Exception as e:
            logger.error(f"Error comparing products: {e}")
            raise e
