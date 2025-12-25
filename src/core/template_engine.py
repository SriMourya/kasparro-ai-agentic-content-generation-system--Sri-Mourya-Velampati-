import json
from typing import Dict, Any, Callable

class TemplateEngine:
    """
    Custom Template Engine.
    Renders a JSON template by processing fields and applying logic blocks.
    """
    def __init__(self, logic_blocks: Dict[str, Callable]):
        self.logic_blocks = logic_blocks

    def render(self, template: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key, value in template.items():
            result[key] = self._process_node(value, data)
        return result

    def _process_node(self, node: Any, data: Dict[str, Any]) -> Any:
        if isinstance(node, dict):
            # Check if it's a dynamic block
            if "_block" in node:
                block_name = node["_block"]
                args = node.get("args", {})
                if block_name in self.logic_blocks:
                    # Execute logic block
                    return self.logic_blocks[block_name](data, **args)
                else:
                    raise ValueError(f"Unknown logic block: {block_name}")
            else:
                # Recurse for nested dicts
                return {k: self._process_node(v, data) for k, v in node.items()}
        
        elif isinstance(node, list):
            return [self._process_node(item, data) for item in node]
        
        elif isinstance(node, str):
            # Simple variable substitution {variable}
            if node.startswith("{") and node.endswith("}"):
                var_name = node[1:-1]
                val = self._get_value_from_path(data, var_name)
                return val if val is not None else node # key not found, return original string or None? returning original for now
            return node
        
        else:
            return node

    def _get_value_from_path(self, data: Any, path: str) -> Any:
        keys = path.split(".")
        curr = data
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            elif hasattr(curr, k):
                 curr = getattr(curr, k)
            else:
                return None
        return curr
