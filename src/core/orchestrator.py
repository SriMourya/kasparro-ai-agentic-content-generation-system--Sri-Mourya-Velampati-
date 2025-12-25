from typing import List, Dict, Any
from .agent_base import Agent, AgentContext

class Orchestrator:
    """Manages the execution flow of agents."""
    def __init__(self):
        self.agents: List[Agent] = []
        self.context = AgentContext()

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def set_initial_data(self, data: Dict[str, Any]):
        for k, v in data.items():
            self.context.set(k, v)

    def run(self):
        print("Starting Orchestrator Pipeline...")
        for agent in self.agents:
            print(f"Running agent: {agent.name}")
            try:
                agent.process(self.context)
            except Exception as e:
                print(f"Error in agent {agent.name}: {e}")
                raise e
        print("Pipeline completed successfully.")

    def get_context_data(self) -> Dict[str, Any]:
        return self.context.to_dict()
