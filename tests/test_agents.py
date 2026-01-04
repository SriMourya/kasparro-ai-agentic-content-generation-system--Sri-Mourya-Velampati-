
import pytest
from unittest.mock import MagicMock, patch
from src.agents.question_generator_agent import QuestionGeneratorAgent
from src.domain.models import ProductModel, FAQList, FAQItem
from src.core.config import settings

@pytest.fixture
def mock_product():
    return ProductModel(
        name="Test Product",
        concentration="10%",
        skin_type=["All"],
        key_ingredients=["Water"],
        benefits=["Hydration"],
        how_to_use="Apply daily",
        side_effects="None",
        price=10.0,
        currency="USD"
    )

def test_question_generator_loop(mock_product):
    """
    Test that the generator effectively loops to get enough FAQs.
    """
    item_gen = lambda i: FAQItem(question=f"Q{i}", answer=f"A{i}", category="Test")
    
    list1 = FAQList(items=[item_gen(i) for i in range(10)])
    list2 = FAQList(items=[item_gen(i) for i in range(10, 20)])
    
    with patch('src.agents.question_generator_agent.ChatGoogleGenerativeAI') as MockLLM:
        agent = QuestionGeneratorAgent()
        
        with patch.object(QuestionGeneratorAgent, '_call_llm', side_effect=[list1, list2]) as mock_call:
            result = agent.generate(mock_product)
            
            assert len(result.items) >= settings.MIN_FAQ_COUNT
            assert len(result.items) == 20
            # Ensure calling twice
            assert mock_call.call_count == 2
