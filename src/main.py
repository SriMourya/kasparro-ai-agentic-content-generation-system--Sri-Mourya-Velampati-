import sys
import os
import json
import logging

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.graph import create_graph
from src.core.config import settings
from src.core.logger import setup_logger, get_logger
from langchain_community.cache import SQLiteCache

setup_logger()
logger = get_logger(__name__)

# Setup Caching
try:
    from langchain.globals import set_llm_cache
    set_llm_cache(SQLiteCache(database_path=".langchain.db"))
except ImportError:
    # Fallback for older langchain versions
    import langchain
    langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

def load_data(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Data file not found at {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {filepath}")
        sys.exit(1)

def main():
    logger.info("Starting Agentic Content Generation Pipeline")
    
    # Check Config
    try:
        settings.validate()
    except ValueError as e:
        logger.critical(str(e))
        sys.exit(1)

    # 1. Setup Data
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'products.json')
    all_data = load_data(data_path)
    
    glowboost_data = all_data.get("glowboost")
    product_b_data = all_data.get("product_b")
    
    if not glowboost_data or not product_b_data:
        logger.error("Missing product data in products.json")
        sys.exit(1)

    # 2. Create Graph
    try:
        app = create_graph()
        
        # 3. Run Graph
        initial_state = {
            "raw_data": glowboost_data,
            "product_b_data": product_b_data
        }
        
        logger.info("Invoking graph...")
        app.invoke(initial_state)
        logger.info("Pipeline Completed Successfully")
        print("Outputs generated: product_page.json, faq.json, comparison_page.json")
        
    except Exception as e:
        logger.error("Pipeline Failed", exc_info=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
