import os
import time

from dotenv import load_dotenv
from ollama import Client
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer

from llm_prompt_model import LLMPromptModel

load_dotenv(override=True)

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")  # Change to your available model
ollama_client = None


def get_ollama_client():
    """Get or create ollama client instance."""
    global ollama_client
    if ollama_client is None:
        print("\n" + "=" * 60)
        print(f"Connecting to Ollama at {OLLAMA_HOST}")
        ollama_client = Client(host=OLLAMA_HOST)
    return ollama_client


def llm_call(input: LLMPromptModel) -> str:
    """Call ollama model and return response text."""
    client = get_ollama_client()
    print("\n" + "=" * 60)
    print(f"Using LLM to Process Request. LLM-Model: {OLLAMA_MODEL}")
    llm_input = input.prompt + input.data_payload
    print(f"\nPrompt:\n{llm_input}\n")
    response = client.generate(model=OLLAMA_MODEL, prompt=llm_input, stream=False)
    return response.get("response", "")



##print("\n" + "=" * 60)
##prompt = "what color I'll get if I mix blue and yellow?"
##print("\nGetting Result of Prompt. Please wait...")
##result = llm_call(prompt)
##print("\n" + "=" * 60)
##print("Prompt Result: \n")
##print(result)
##print("=" * 60 + "\n")