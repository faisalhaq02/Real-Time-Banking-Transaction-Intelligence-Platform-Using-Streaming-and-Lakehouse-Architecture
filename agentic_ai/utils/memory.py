from collections import deque

class ConversationMemory:
    def __init__(self, max_turns: int = 6):
        self.history = deque(maxlen=max_turns * 2)

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_messages(self) -> list:
        return list(self.history)

    def clear(self):
        self.history.clear()

# Global memory instance
memory = ConversationMemory()