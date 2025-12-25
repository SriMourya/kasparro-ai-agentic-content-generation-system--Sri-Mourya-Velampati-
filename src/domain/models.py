from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class KeyIngredient:
    name: str

@dataclass
class ProductModel:
    name: str = ""
    concentration: str = ""
    skin_type: List[str] = field(default_factory=list)
    key_ingredients: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    how_to_use: str = ""
    side_effects: str = ""
    price: float = 0.0
    currency: str = "INR"

@dataclass
class FAQItem:
    question: str
    answer: str
    category: str

@dataclass
class ComparisonModel:
    product_a: ProductModel
    product_b: ProductModel
