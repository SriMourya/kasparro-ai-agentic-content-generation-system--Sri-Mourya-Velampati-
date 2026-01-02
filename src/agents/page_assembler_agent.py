import os
from src.domain.models import ProductModel, FAQList, ComparisonModel

class PageAssemblerAgent:
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir

    def save_product_page(self, product: ProductModel, filename: str = "product_page.json"):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(product.model_dump_json(indent=2))
        print(f"Saved {path}")

    def save_faq_page(self, faq_list: FAQList, filename: str = "faq.json"):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(faq_list.model_dump_json(indent=2))
        print(f"Saved {path}")
    
    def save_comparison_page(self, comparison: ComparisonModel, filename: str = "comparison_page.json"):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(comparison.model_dump_json(indent=2))
        print(f"Saved {path}")
