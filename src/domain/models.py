from typing import List, Optional
from pydantic import BaseModel, Field

class KeyIngredient(BaseModel):
    name: str

class ProductModel(BaseModel):
    name: str = Field(description="Name of the product")
    concentration: str = Field(description="Concentration of key ingredients")
    skin_type: List[str] = Field(default_factory=list, description="Suitable skin types")
    key_ingredients: List[str] = Field(default_factory=list, description="List of key ingredients")
    benefits: List[str] = Field(default_factory=list, description="List of main benefits")
    how_to_use: str = Field(description="Usage instructions")
    side_effects: str = Field(description="Potential side effects")
    price: float = Field(description="Price of the product")
    currency: str = Field(default="INR", description="Currency code")

class FAQItem(BaseModel):
    question: str = Field(description="The question")
    answer: str = Field(description="The answer to the question")
    category: str = Field(description="Category of the question (e.g. Informational, Usage, Safety, Purchase)")

class FAQList(BaseModel):
    items: List[FAQItem] = Field(description="List of FAQ items")

class ComparisonResult(BaseModel):
    product_a_name: str = Field(description="Name of Product A")
    product_b_name: str = Field(description="Name of Product B")
    comparison_points: List[str] = Field(description="List of key comparison points")
    verdict: str = Field(description="Final verdict or recommendation")

class ComparisonModel(BaseModel):
    product_a: ProductModel
    product_b: ProductModel
    analysis: Optional[ComparisonResult] = None
