"""
LLM Client - Connects to local Ollama instance
Supports Llama3, Mistral, and other local models
"""

import requests
import json


class LLMClient:
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chat"

    def chat(self, user_message: str, history: list = None, system_prompt: str = "") -> str:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add conversation history
        if history:
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1024
            }
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

        except requests.exceptions.ConnectionError:
            return (
                "⚠️ Cannot connect to Ollama. Please ensure it's running:\n"
                "1. Install Ollama from https://ollama.ai\n"
                "2. Run: `ollama serve`\n"
                "3. Pull a model: `ollama pull llama3`"
            )
        except requests.exceptions.Timeout:
            return "⏱️ The model is taking too long to respond. Please try again."
        except Exception as e:
            return f"❌ Error communicating with LLM: {str(e)}"

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False

    def list_models(self) -> list:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            data = r.json()
            return [m["name"] for m in data.get("models", [])]
        except:
            return []
