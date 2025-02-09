
import os

class SlyceAI:
    def __init__(self):
        self.name = "Slyce"
        self.version = "0.1"
        self.knowledge_base = {}

    def learn(self, key, value):
        self.knowledge_base[key] = value

    def respond(self, query):
        return self.knowledge_base.get(query, "I am still learning.")

if __name__ == "__main__":
    ai = SlyceAI()
    print(f"{ai.name} v{ai.version} is running...")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = ai.respond(user_input)
        print(f"Slyce: {response}")

