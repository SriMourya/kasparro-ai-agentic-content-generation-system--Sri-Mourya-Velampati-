from typing import List, Dict
from src.core.agent_base import Agent, AgentContext
from src.domain.models import ProductModel, FAQItem

class QuestionGeneratorAgent(Agent):
    """
    Generates categorized user questions based on the ProductModel.
    Uses rule-based templates to ensure deterministic output for this system demo.
    """
    def __init__(self):
        super().__init__(name="QuestionGeneratorAgent")

    def process(self, context: AgentContext) -> None:
        product: ProductModel = context.get("product_model")
        if not product:
            print("QuestionGeneratorAgent: No ProductModel found in context.")
            return

        print("QuestionGeneratorAgent: Generating questions...")
        
        questions: List[FAQItem] = []

        # 1. Informational Category
        questions.append(FAQItem(
            question=f"What is {product.name}?",
            answer=f"{product.name} is a serum containing {product.concentration}. It features key ingredients like {', '.join(product.key_ingredients)}.",
            category="Informational"
        ))
        questions.append(FAQItem(
            question=f"What are the main benefits of {product.name}?",
            answer=f"The main benefits are: {', '.join(product.benefits)}.",
            category="Informational"
        ))
        questions.append(FAQItem(
            question=f"What is the concentration of {product.name}?",
            answer=f"It contains {product.concentration}.",
            category="Informational"
        ))

        # 2. Usage Category
        questions.append(FAQItem(
            question=f"How should I apply {product.name}?",
            answer=product.how_to_use,
            category="Usage"
        ))
        questions.append(FAQItem(
            question="Can I use this in the morning?",
            answer="Yes, it is recommended to apply in the morning before sunscreen.",
            category="Usage"
        ))
        questions.append(FAQItem(
            question="How many drops should I use?",
            answer="Apply 2-3 drops.",
            category="Usage"
        ))

        # 3. Safety Category
        questions.append(FAQItem(
            question="Are there any side effects?",
            answer=product.side_effects,
            category="Safety"
        ))
        questions.append(FAQItem(
            question="Is this product safe for sensitive skin?",
            answer=f"It may cause {product.side_effects}, so patch testing is recommended.",
            category="Safety"
        ))
        for st in product.skin_type:
             questions.append(FAQItem(
                question=f"Is {product.name} good for {st} skin?",
                answer=f"Yes, it is specifically formulated for {st} skin types.",
                category="Safety"
            ))

        # 4. Purchase Category
        questions.append(FAQItem(
            question=f"How much does {product.name} cost?",
            answer=f"It is priced at {product.currency} {product.price}.",
            category="Purchase"
        ))
        questions.append(FAQItem(
            question="Is this product affordable?",
            answer="At ₹699, it offers great value for a 10% Vitamin C serum.",
            category="Purchase"
        ))

        # 5. Comparison/Ingredients
        for ing in product.key_ingredients:
            questions.append(FAQItem(
                question=f"Does it contain {ing}?",
                answer=f"Yes, {ing} is a key ingredient.",
                category="Ingredients"
            ))
        
        # Ensure we have at least 15
        while len(questions) < 15:
             questions.append(FAQItem(
                question=f"Generic question {len(questions)+1} about {product.name}",
                answer="Generic answer.",
                category="General"
             ))

        # Store as simple dicts for JSON serialization
        faq_data = [
            {"question": q.question, "answer": q.answer, "category": q.category}
            for q in questions
        ]
        
        context.set("faq_list", faq_data)
        print(f"QuestionGeneratorAgent: Generated {len(questions)} questions.")
