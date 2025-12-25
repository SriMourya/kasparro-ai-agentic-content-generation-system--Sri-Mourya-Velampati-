import json
import os
from typing import Dict, Any
from src.core.agent_base import Agent, AgentContext
from src.core.template_engine import TemplateEngine

class PageAssemblerAgent(Agent):
    """
    Assembles a final page using a template and the content in the context.
    Writes the output to a JSON file.
    """
    def __init__(self, template_name: str, output_filename: str, template_engine: TemplateEngine):
        super().__init__(name=f"PageAssembler_{output_filename}")
        self.template_name = template_name
        self.output_filename = output_filename
        self.engine = template_engine

    def process(self, context: AgentContext) -> None:
        print(f"{self.name}: Assembling page...")
        
        # Load Template
        # In a real app, this might come from a DB or file. We'll assume it's passed in context or load from file.
        # For this design, let's look for templates in src/templates/
        
        template_path = os.path.join("src", "templates", self.template_name)
        try:
            with open(template_path, "r") as f:
                template = json.load(f)
        except FileNotFoundError:
            print(f"Error: Template {template_path} not found.")
            return

        # Prepare data for template
        # The context contains 'product' (dict) and 'faq_list' (list of dicts)
        # We pass the entire context data to the engine
        data = context.to_dict()

        # Render
        rendered_page = self.engine.render(template, data)

        # Write Output
        with open(self.output_filename, "w") as f:
            json.dump(rendered_page, f, indent=2)
        
        print(f"{self.name}: Page written to {self.output_filename}")
