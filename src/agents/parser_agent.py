from typing import Any, Dict
from src.core.agent_base import Agent, AgentContext
from src.domain.models import ProductModel

class ParserAgent(Agent):
    """
    Parses raw dictionary input into a structured ProductModel.
    Also handles basic validation and data type conversion.
    """
    def __init__(self):
        super().__init__(name="ParserAgent")

    def process(self, context: AgentContext) -> None:
        raw_data = context.get("raw_data")
        if not raw_data:
            print("ParserAgent: No raw_data found in context.")
            return

        print(f"ParserAgent: Parsing raw data for '{raw_data.get('Product Name')}'...")

        # Map raw keys to model fields
        # Input:
        # ● Product Name: GlowBoost Vitamin C Serum
        # ● Concentration: 10% Vitamin C
        # ● Skin Type: Oily, Combination
        # ● Key Ingredients: Vitamin C, Hyaluronic Acid
        # ● Benefits: Brightening, Fades dark spots
        # ● How to Use: Apply 2–3 drops in the morning before sunscreen
        # ● Side Effects: Mild tingling for sensitive skin
        # ● Price: ₹699
        
        try:
            price_str = str(raw_data.get("Price", "0")).replace("₹", "").strip()
            price = float(price_str)
        except ValueError:
            price = 0.0

        skin_type = [s.strip() for s in raw_data.get("Skin Type", "").split(",")]
        ingredients = [i.strip() for i in raw_data.get("Key Ingredients", "").split(",")]
        benefits = [b.strip() for b in raw_data.get("Benefits", "").split(",")]

        product = ProductModel(
            name=raw_data.get("Product Name", ""),
            concentration=raw_data.get("Concentration", ""),
            skin_type=skin_type,
            key_ingredients=ingredients,
            benefits=benefits,
            how_to_use=raw_data.get("How to Use", ""),
            side_effects=raw_data.get("Side Effects", ""),
            price=price,
            currency="INR"
        )

        context.set("product_model", product)
        # Also set it as a dict for the template engine to access easily
        context.set("product", product.__dict__)
        print("ParserAgent: ProductModel created and stored in context.")
