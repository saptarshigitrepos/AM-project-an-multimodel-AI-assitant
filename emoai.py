import sys
import threading
import random
import time
import os
import json
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS
import openai  # Import the openai library

# Load environment variables from .env file
load_dotenv()

# Set up OpenRouter API key
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# Memory file path
memory_file = "memories.json"
MAX_MEMORY_ENTRIES = 20  # Limit stored interactions


# Load previous conversations from a file
def load_memory(filename: str) -> List[Dict[str, str]]:
    """Load conversation memory from a JSON file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Memory file corrupted. Starting fresh.")
    return []  # Return an empty list if the file doesn't exist or is corrupted


# Save current conversations to a file
def save_memory(memory: List[Dict[str, str]]) -> None:
    """Save conversation memory to a JSON file named memories.json."""
    trimmed_memory = memory[-MAX_MEMORY_ENTRIES:]  # Keep only the last MAX_MEMORY_ENTRIES interactions
    try:
        with open(memory_file, 'w') as f:
            json.dump(
                [{"timestamp": datetime.now().isoformat(), **entry}
                 for entry in trimmed_memory],
                f,
                indent=2  # Pretty print JSON for readability
            )
    except Exception as e:
        print(f"Error saving memory: {str(e)}")


# ASCII Art for Welcome Message (with color)
# ANSI color codes
NEON_GREEN = "\033[91;5m"
RESET = "\033[0m"

# Console Size
WIDTH = 80
HEIGHT = 20

# Matrix Rain Characters
BINARY_CHARS = ["0", "1", " "]

# Shared flag for stopping the rain effect
running = True

def clear_screen():
    """Clears the console screen."""
    os.system("cls" if os.name == "nt" else "clear")

def binary_rain():
    """Generates continuous Matrix-style raining binary in the background."""
    columns = [0] * WIDTH
    while running:
        rain_screen = [" " * WIDTH for _ in range(HEIGHT)]

        for i in range(WIDTH):
            if random.random() > 0.98:  # Randomly start a new rain stream
                columns[i] = 0

            if columns[i] < HEIGHT:
                rain_screen[columns[i]] = (
                    rain_screen[columns[i]][:i]
                    + random.choice(BINARY_CHARS)
                    + rain_screen[columns[i]][i + 1 :]
                )
                columns[i] += 1

        print(NEON_GREEN + "\n".join(rain_screen) + RESET)
        time.sleep(0.1)
        clear_screen()

def binary_effect(text, duration=0.6, delay=0.03):
    """Applies a Matrix-style binary glitch effect before revealing the text."""
    scrambled = ''.join(random.choice("01") if c != " " else " " for c in text)
    print(NEON_GREEN + scrambled + RESET, end="\r", flush=True)
    time.sleep(delay)

    for _ in range(int(duration / delay)):
        scrambled = ''.join(
            text[i] if random.random() > 0.6 else random.choice("01")
            for i in range(len(text))
        )
        print(NEON_GREEN + scrambled + RESET, end="\r", flush=True)
        time.sleep(delay)

    print(NEON_GREEN + text + RESET)

def smooth_appearance(text, delay=0.02):
    """Displays text smoothly without distortion."""
    for char in text:
        print(NEON_GREEN + char + RESET, end="", flush=True)
        time.sleep(delay)
    print()

def display_welcome():
    """Displays the ASCII AM logo with binary glitch effect, and the tagline/version info normally."""
    ascii_art = [
        " █████    ███    ███",  # AM logo part 1
        "██   ██   ████  ████",  # AM logo part 2
        "███████   ██ ████ ██",  # AM logo part 3
        "██   ██   ██  ██  ██",  # AM logo part 4
        "██   ██   ██      ██"   # AM logo part 5
    ]

    tagline = "Allied Master Computer"
    version_info = "The Multi-Model AI Assistant (Version 1.0 ca.1984)"

    # Apply the binary glitch effect **only** to the AM logo
    for line in ascii_art:
        binary_effect(line, duration=0.4, delay=0.02)

    time.sleep(0.5)

    # Display tagline and version info normally (no binary effect)
    smooth_appearance("\n" + tagline.center(100) + "\n", delay=0.02)
    smooth_appearance(version_info.center(100) + "\n", delay=0.02)

# Start the Matrix rain in the background
rain_thread = threading.Thread(target=binary_rain, daemon=True)
rain_thread.start()

# Run the welcome animation
display_welcome()

# Stop the rain effect after the animation
running = False
rain_thread.join()

print("\n" + NEON_GREEN + "System Ready..." + RESET)


    # Typing Effect Function


def type_effect(text: str) -> None:
    """Simulate typing effect in console output."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)  # Adjust speed here
    print()  # Move to the next line after typing


# Search Function using DuckDuckGo API with DDGS
def search_web(query: str) -> str:
    """Search the web using DuckDuckGo API."""
    try:
        with DDGS() as ddgs:
            results = [result for result in ddgs.text(query, max_results=5)]
            if results:
                return "\n".join([result['body'] for result in results])
            else:
                return "No relevant information found."
    except Exception as e:
        return f"Error during search: {str(e)}"


# Available models dictionary with their respective API keys and providers
available_models = {
    "deepseek": {"model_id": "deepseek-r1-distill-llama-70b", "api_key": os.environ.get("GROQ_API_KEY"),
                 "provider": "groq"},
    "deepseekr1qwen": {"model_id": "deepseek-r1-distill-qwen-32b", "api_key": os.environ.get("DEEPSEEKR1QWEN_API_KEY"),
                       "provider": "groq"},
    "llama": {"model_id": "llama-3.3-70b-versatile", "api_key": os.environ.get("LLAMA_API_KEY"),
                    "provider": "groq"},
    "llama3.290b": {"model_id": "llama-3.2-90b-vision-preview", "api_key": os.environ.get("LLAMA3.2_API_KEY"),
                    "provider": "groq"},
    "gemma": {"model_id": "gemma2-9b-it", "api_key": os.environ.get("GEMMA_API_KEY"), "provider": "groq"},
    "qwen2.5coder": {"model_id": "qwen-2.5-coder-32b", "api_key": os.environ.get("QWEN2.5CODER_API_KEY"),
                     "provider": "groq"},
    "qwenqwq": {"model_id": "qwen-qwq-32b", "api_key": os.environ.get("QWENQWQ_EXPERIMENT_API_KEY"),
                "provider": "groq"},
    "mistrals24b": {"model_id": "mistralai/mistral-small-3.1-24b-instruct:free",
                    "api_key": os.environ.get("MISTRAL_API_KEY"),
                    "provider": "openrouter"}
}

# Set default model and initialize Groq client
current_model = available_models["llama"]
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Initialize Groq client with API key


# Function to generate dynamic responses using Groq or OpenAI via OpenRouter
def generate_dynamic_response(user_input: str) -> str:
    """Generate a dynamic response using Groq or OpenAI via OpenRouter."""
    try:
        if current_model["provider"] == "groq":
            completion = client.chat.completions.create(
                model=current_model["model_id"],
                messages=[{"role": "user", "content": user_input}],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content.strip()

        elif current_model["provider"] == "openrouter":
            response = openai.ChatCompletion.create(
                model=current_model["model_id"],
                messages=[{"role": "user", "content": user_input}],
                max_tokens=1024,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        else:
            return f"Provider '{current_model['provider']}' not supported."

    except Exception as e:
        return f"Oops, I ran into an issue generating a response: {str(e)}"


# Main Functionality of EmoAI Chatbot
def main() -> None:
    """Main function to run the EmoAI chatbot."""
    display_welcome()  # Display ASCII art welcome message

    print("Anything got you brainstorming?\n")  # Change prompt message

    memory = load_memory(memory_file)

    while True:
        user_input = input("Type something or search: \n").strip()

        if not user_input:  # Skip empty inputs
            continue

        if user_input.lower().startswith("switch model"):
            model_name = user_input[13:].strip()
            if model_name in available_models:
                global current_model  # Use global variable to change current model instance
                current_model = available_models[model_name]
                type_effect(f"Switched to model: {current_model['model_id']}")
            else:
                type_effect(
                    f"Model '{model_name}' not found. Available models are: {', '.join(available_models.keys())}.")
            continue

        response = generate_dynamic_response(user_input)
        type_effect(response)


if __name__ == "__main__":
    main()
