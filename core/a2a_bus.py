# core/a2a_bus.py
import asyncio

class A2ABus:
    def __init__(self):
        self.agents = {}

    def register(self, name, agent):
        self.agents[name] = agent

    def send(self, sender, receiver, message):
        if receiver not in self.agents:
            raise ValueError(f"Receiver agent '{receiver}' not found")
        
        target_agent = self.agents[receiver]
        receive_method = getattr(target_agent, 'receive', None)

        if not receive_method:
            raise AttributeError(f"Agent '{receiver}' does not have a 'receive' method.")

        print(f"[A2A] {sender} → {receiver}: {str(message)[:50]}...")
        
        # Check if the receive method is an async coroutine
        if asyncio.iscoroutinefunction(receive_method):
            # This is a simplified approach. In a real async app, you'd need
            # to ensure the event loop is handled correctly. Since the commander
            # is run in a separate thread via the scheduler, this should be okay.
            return asyncio.run(receive_method(message))
        else:
            return receive_method(message)
