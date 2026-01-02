import sys
import os

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.graph import create_graph

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

    product_b_data = {
        "Product Name": "RadianceX Serum",
        "Concentration": "5% Vitamin C",
        "Price": "₹1200",
        "Key Ingredients": "Vitamin C, Aloe Vera"
    }
    
    # Check API Key (Soft check, let LangChain handle auth errors if any)
    # Check API Key (Soft check, let LangChain handle auth errors if any)
    if not os.environ.get("GOOGLE_API_KEY"):
         print("WARNING: GOOGLE_API_KEY environment variable not found. Agents may fail.")

    print("--- Starting Agentic Content Generation Pipeline ---")
    
    # 2. Create Graph
    try:
        app = create_graph()
        
        # 3. Run Graph
        initial_state = {
            "raw_data": glowboost_data,
            "product_b_data": product_b_data
        }
        
        app.invoke(initial_state)
        print("\n--- Pipeline Completed Successfully ---")
        print("Outputs generated: product_page.json, faq.json, comparison_page.json")
        
    except Exception as e:
        print(f"--- Pipeline Failed ---")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
