import sys
import os

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.orchestrator import Orchestrator
from src.core.template_engine import TemplateEngine
from src.domain.logic_blocks import LOGIC_BLOCKS
from src.agents.parser_agent import ParserAgent
from src.agents.question_generator_agent import QuestionGeneratorAgent
from src.agents.page_assembler_agent import PageAssemblerAgent
from src.domain.models import ProductModel

def main():
    # 1. Setup Data
    glowboost_data = {
        "Product Name": "GlowBoost Vitamin C Serum",
        "Concentration": "10% Vitamin C",
        "Skin Type": "Oily, Combination",
        "Key Ingredients": "Vitamin C, Hyaluronic Acid",
        "Benefits": "Brightening, Fades dark spots",
        "How to Use": "Apply 2–3 drops in the morning before sunscreen",
        "Side Effects": "Mild tingling for sensitive skin",
        "Price": "₹699"
    }

    # Fictional Product B
    product_b_data = {
        "Product Name": "RadianceX Serum",
        "Concentration": "5% Vitamin C",
        "Price": "₹1200",
        "Key Ingredients": "Vitamin C, Aloe Vera"
    }
    
    # Pre-parse Product B for the comparison to work easily in logic blocks
    # In a full system, we might have a separate agent parse this too, but for simplicity here:
    product_b_model = ProductModel(
        name=product_b_data["Product Name"],
        concentration=product_b_data["Concentration"],
        key_ingredients=[i.strip() for i in product_b_data["Key Ingredients"].split(",")],
        price=float(product_b_data["Price"].replace("₹", "")),
        currency="INR"
    )

    # 2. Setup Core Infrastructure
    logic_blocks = LOGIC_BLOCKS
    template_engine = TemplateEngine(logic_blocks)
    orchestrator = Orchestrator()

    # 3. Register Agents in DAG order
    # Step 1: Parse Input
    orchestrator.add_agent(ParserAgent())
    
    # Step 2: Generate Content (Enrichment)
    orchestrator.add_agent(QuestionGeneratorAgent())

    # Step 3: Assemble Pages
    # We add 3 instances of PageAssemblerAgent, one for each page
    orchestrator.add_agent(PageAssemblerAgent(
        template_name="faq_template.json",
        output_filename="faq.json",
        template_engine=template_engine
    ))
    orchestrator.add_agent(PageAssemblerAgent(
        template_name="product_page_template.json",
        output_filename="product_page.json",
        template_engine=template_engine
    ))
    orchestrator.add_agent(PageAssemblerAgent(
        template_name="comparison_template.json",
        output_filename="comparison_page.json",
        template_engine=template_engine
    ))

    # 4. Initialize Context
    orchestrator.set_initial_data({
        "raw_data": glowboost_data,
        "product_b": product_b_model, # Injecting Product B directly for comparison
        # Also inject product_b as dict
        "product_b": product_b_model,
        # Wait, the template engine accesses dict keys or attributes? 
        # My TemplateEngine implementation handles both dict access and attribute access!
        # references: 
        # _get_value_from_path lines:
        # if isinstance(curr, dict) and k in curr: curr = curr[k]
        # elif hasattr(curr, k): curr = getattr(curr, k)
        # So passing the object is fine.
    })

    # 5. Run
    orchestrator.run()

if __name__ == "__main__":
    main()
