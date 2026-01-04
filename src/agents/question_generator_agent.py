from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.domain.models import ProductModel, FAQList, FAQItem
from src.core.config import settings
from src.core.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

class QuestionGeneratorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(temperature=0.7, model="models/gemini-flash-latest")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _call_llm(self, chain, input_data):
        return chain.invoke(input_data)

    def generate(self, product: ProductModel) -> FAQList:
        """
        Generates FAQ items based on the product model using an LLM.
        Enforces a minimum of 15 FAQs with deduplication.
        """
        logger.info(f"Generating FAQs for {product.name}")
        structured_llm = self.llm.with_structured_output(FAQList)
        
        # Updated prompt to explicitly request more FAQs
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful content strategist. Generate at least 20 relevant, high-quality frequently asked questions and answers for the given product. Cover categories like Usage, Safety, Ingredients, and Purchase."),
            ("user", "Product: {product_name}\nDetails: {product_details}\n\nExisting Questions (to avoid): {existing_questions}")
        ])
        
        chain = prompt | structured_llm
        
        all_faqs: list[FAQItem] = []
        unique_questions = set()
        attempts = 0
        max_attempts = 5

        while len(all_faqs) < settings.MIN_FAQ_COUNT and attempts < max_attempts:
            attempts += 1
            logger.info(f"Generation attempt {attempts}. Current count: {len(all_faqs)}")
            
            try:
                result = self._call_llm(chain, {
                    "product_name": product.name,
                    "product_details": product.model_dump_json(),
                    "existing_questions": ", ".join(list(unique_questions))
                })
                
                if result and result.items:
                    for item in result.items:
                        # Simple deduplication
                        if item.question not in unique_questions:
                            unique_questions.add(item.question)
                            all_faqs.append(item)
            except Exception as e:
                logger.error(f"Error generating FAQs: {e}")
                
        if len(all_faqs) < settings.MIN_FAQ_COUNT:
             logger.warning(f"Could not generate {settings.MIN_FAQ_COUNT} FAQs. Only got {len(all_faqs)}.")

        return FAQList(items=all_faqs)
