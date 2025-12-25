from typing import Dict, Any, List

def _get_value(data: Any, key: str, default: Any = None) -> Any:
    """Helper to get value from dict or object."""
    if isinstance(data, dict):
        return data.get(key, default)
    return getattr(data, key, default)

def _get_nested(data: Any, path: str, default: Any = None) -> Any:
    """Helper to traverse dot-notation path."""
    keys = path.split(".")
    curr = data
    for k in keys:
        if isinstance(curr, dict):
            curr = curr.get(k)
        else:
            curr = getattr(curr, k, None)
        if curr is None:
            return default
    return curr

def format_price(data: Dict[str, Any], key: str = "product.price", currency_symbol: str = "₹") -> str:
    """Formats price with currency symbol. Defaults to looking at 'product.price'."""
    price = _get_nested(data, key, 0)
    return f"{currency_symbol}{price}"

def generate_benefits_list(data: Dict[str, Any], key: str = "product.benefits") -> str:
    """Formats benefits into an HTML-like list or markdown bullet points."""
    benefits = _get_nested(data, key, [])
    if isinstance(benefits, str):
        benefits = [b.strip() for b in benefits.split(",")]
    
    return "\n".join([f"- {b}" for b in benefits])

def extract_ingredients_text(data: Dict[str, Any], key: str = "product.key_ingredients") -> str:
    """Formats ingredients as a comma-separated string."""
    ingredients = _get_nested(data, key, [])
    if isinstance(ingredients, list):
        return ", ".join(ingredients)
    return str(ingredients)

def create_meta_title(data: Dict[str, Any], name_key: str = "product.name", conc_key: str = "product.concentration") -> str:
    """Generates a SEO meta title."""
    name = _get_nested(data, name_key, "Product")
    conc = _get_nested(data, conc_key, "")
    return f"{name} - {conc} | Official Store"

def compare_price(data: Dict[str, Any], p1_key: str = "product.price", p2_key: str = "product_b.price") -> str:
    """Compares price between main product and another product in the data context."""
    p1_price = _get_nested(data, p1_key, 0)
    p2_price = _get_nested(data, p2_key, 0)
    
    try:
        p1_val = float(p1_price)
        p2_val = float(p2_price)
    except (ValueError, TypeError):
        return "N/A"

    if p1_val < p2_val:
        return "More Affordable"
    elif p1_val > p2_val:
        return "Premium Choice"
    else:
        return "Same Price"

# Registry of logic blocks
LOGIC_BLOCKS = {
    "format_price": format_price,
    "generate_benefits_list": generate_benefits_list,
    "extract_ingredients_text": extract_ingredients_text,
    "create_meta_title": create_meta_title,
    "compare_price": compare_price
}
