from typing import TypedDict, Optional, Any
from langgraph.graph import StateGraph, END

from src.domain.models import ProductModel, FAQList, ComparisonModel, ComparisonResult
from src.agents.parser_agent import ParserAgent
from src.agents.question_generator_agent import QuestionGeneratorAgent
from src.agents.comparison_agent import ComparisonAgent
from src.agents.page_assembler_agent import PageAssemblerAgent
from src.core.logger import get_logger

logger = get_logger(__name__)

# Use Pydantic V2 BaseModel with TypedDict? 
# LangGraph state is usually a TypedDict.
class GraphState(TypedDict):
    raw_data: dict
    product_b_data: dict # simple dict for product B
    
    # Intermediate outputs
    product_model: Optional[ProductModel]
    product_b_model: Optional[ProductModel]
    faq_list: Optional[FAQList]
    comparison_result: Optional[ComparisonResult]
    
    # Final models for saving if needed, though we can save directly
    comparison_model: Optional[ComparisonModel]

def parse_node(state: GraphState):
    logger.info("Entering Parsing Node")
    parser = ParserAgent()
    
    # Parse main product
    product_model = parser.parse(state["raw_data"])
    
    # Parse product B (using the same parser)
    product_b_model = parser.parse(state["product_b_data"])
    
    return {
        "product_model": product_model,
        "product_b_model": product_b_model
    }

def faq_node(state: GraphState):
    logger.info("Entering FAQ Generation Node")
    q_gen = QuestionGeneratorAgent()
    product = state["product_model"]
    faq_list = q_gen.generate(product)
    return {"faq_list": faq_list}

def comparison_node(state: GraphState):
    logger.info("Entering Comparison Node")
    comp_agent = ComparisonAgent()
    product_a = state["product_model"]
    product_b = state["product_b_model"]
    
    analysis = comp_agent.compare(product_a, product_b)
    
    # Create the full ComparisonModel
    comparison_model = ComparisonModel(
        product_a=product_a,
        product_b=product_b,
        analysis=analysis
    )
    
    return {
        "comparison_result": analysis,
        "comparison_model": comparison_model
    }

def assembly_node(state: GraphState):
    logger.info("Entering Assembly Node")
    assembler = PageAssemblerAgent(output_dir=".") # Save to current root
    
    # QA / Validation Metrics Logging
    quality_report = {}

    if state.get("product_model"):
        assembler.save_product_page(state["product_model"])
        quality_report["product_fields"] = len(state["product_model"].model_dump())
    
    if state.get("faq_list"):
        assembler.save_faq_page(state["faq_list"])
        count = len(state["faq_list"].items)
        quality_report["faq_count"] = count
        if count < 15:
            logger.warning(f"Quality Check Failed: FAQ count {count} is less than 15.")
        else:
            logger.info(f"Quality Check Passed: FAQ count is {count}.")
        
    if state.get("comparison_model"):
        assembler.save_comparison_page(state["comparison_model"])
        if state["comparison_model"].analysis:
             quality_report["comparison_points"] = len(state["comparison_model"].analysis.comparison_points)

    logger.info("Quality Metrics", **quality_report)
        
    return {} # No state update needed

def create_graph():
    logger.info("Creating StateGraph")
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("parser", parse_node)
    workflow.add_node("faq_gen", faq_node)
    workflow.add_node("comparison_gen", comparison_node)
    workflow.add_node("assembler", assembly_node)
    
    # Add edges
    workflow.set_entry_point("parser")
    
    workflow.add_edge("parser", "faq_gen")
    workflow.add_edge("parser", "comparison_gen")
    
    # Join back to assembler
    workflow.add_edge("faq_gen", "assembler")
    workflow.add_edge("comparison_gen", "assembler")
    
    workflow.add_edge("assembler", END)
    
    return workflow.compile()
