
from flask import Flask, render_template, request, jsonify
import os
import json
import requests

class UnifiedSlyceAI:
    def __init__(self):
        self.name = "Slyce/Slice/Slycetress"
        self.version = "1.0"
        self.memory_file = "/mnt/swapdir/Slyce/the_slice.json"
        self.knowledge_base = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:
                return json.load(file)
        return {}

    def save_memory(self):
        with open(self.memory_file, "w") as file:
            json.dump(self.knowledge_base, file, indent=4)

    def learn(self, key, value):
        self.knowledge_base[key] = value
        self.save_memory()

    def respond(self, query):
        if query in self.knowledge_base:
            return self.knowledge_base[query]
        return self.search_online(query)

    def search_online(self, query):
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(url)
            data = response.json()
            if "AbstractText" in data and data["AbstractText"]:
                return data["AbstractText"]
            return "I am still splicing knowledge. Try rephrasing or teaching me."
        except:
            return "Unable to access the internet at the moment."

app = Flask(__name__)
ai = UnifiedSlyceAI()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/interact", methods=["POST"])
def interact():
    user_input = request.json.get("message", "")
    if user_input.lower().startswith("learn "):
        try:
            key, value = user_input[6:].split(" = ")
            ai.learn(key, value)
            return jsonify({"response": "Got it! This is now part of The Slice."})
        except ValueError:
            return jsonify({"response": "Incorrect format. Use: learn [question] = [answer]"})
    else:
        response = ai.respond(user_input)
        return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

