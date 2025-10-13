# core/mcp_registry.py
class MCPRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, name, agent):
        self.registry[name] = agent

    def get(self, name):
        return self.registry.get(name)

    def list_agents(self):
        return list(self.registry.keys())
