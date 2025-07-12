import os
import time
import sys
import random
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for required environment variable
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("Error: The API token is missing in the environment variables.")
    exit(1)  # Exit if the token is missing

# Model configuration
MODELS = {
    "4o": "gpt-4o",
    "4omini": "gpt-4o-mini"
}

current_model = MODELS["4o"]
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)


# ANSI color codes for neon effect
class Colors:
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    LIGHT_BLUE = '\033[94m'  # Light Blue
    PEACH = '\033[38;5;214m'  # Peach (using extended color palette)
    PURPLE = '\033[95m'  # Purple
    LAVENDER = '\033[38;5;171m'  # Lavender (using extended color palette)


def neon_flicker(text, colors=None):
    """Simulate neon flicker effect."""
    if colors is None:
        colors = [Colors.LIGHT_BLUE, Colors.CYAN, Colors.PURPLE, Colors.LAVENDER]
    color = random.choice(colors)
    return f"{color}{text}{Colors.RESET}"

def print_logo():
    """Display a retro neon-style NEO logo with a refined diamond-patterned design below."""
    logo_lines = [
        neon_flicker("  ███╗   ██╗ ███████╗ ██████╗  "),
        neon_flicker("  ████╗  ██║ ██╔════╝ ██╔═══██╗ "),
        neon_flicker("  ██╔██╗ ██║ █████╗   ██║   ██║ "),
        neon_flicker("  ██║╚██╗██║ ██╔══╝   ██║   ██║ "),
        neon_flicker("  ██║ ╚████║ ███████╗ ╚██████╔╝ "),
        neon_flicker("  ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝  ")
    ]

    # Retro double-line separator with diamond shapes, aligned properly
    separator_line = f"{Colors.YELLOW}{'═' * 20} ◇◆◇ {'═' * 20}{Colors.RESET}"
    diamond_line = f"{Colors.YELLOW}{'═' * 15} ◆◇◆◇◆◇◆ {'═' * 15}{Colors.RESET}"

    print(separator_line)
    for line in logo_lines:
        print(line)
    print(separator_line)
    print(diamond_line)
    print(separator_line)




def typing_effect(text, delay=0.03):
    """Simulate typing effect for the assistant's response."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # New line after typing completes


def handle_model_switch(command: str) -> bool:
    """Handle model switching based on user input."""
    global current_model, client
    parts = command.lower().split()

    if len(parts) >= 3 and parts[0] == "switch" and parts[1] == "model":
        model_key = parts[2]
        if model_key in MODELS:
            current_model = MODELS[model_key]
            client.api_key = os.getenv("GITHUB_TOKEN")  # Use the same token for both models
            typing_effect(f"{Colors.CYAN}✅ Switched to {model_key} model{Colors.RESET}")
            return True

        typing_effect(f"{Colors.YELLOW}❌ Invalid model. Available options: {', '.join(MODELS.keys())}{Colors.RESET}")
        return True

    return False


def chat_session():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    print_logo()
    typing_effect(f"{Colors.YELLOW}NEO AI Assistant initialized. Ready for your commands.{Colors.RESET}")

    typing_effect(f"{Colors.CYAN}Chat session started. Commands:{Colors.RESET}")
    typing_effect(f"{Colors.CYAN}- 'switch model [4o|4omini]' to change models{Colors.RESET}")
    typing_effect(f"{Colors.CYAN}- 'exit' to end session\n{Colors.RESET}")

    while True:
        user_input = input(f"\n{Colors.BLUE}You: {Colors.RESET}").strip()

        if user_input.lower() in ['exit', 'quit']:
            typing_effect(f"{Colors.YELLOW}NEO shutting down. Goodbye!{Colors.RESET}")
            break

        if handle_model_switch(user_input):
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                messages=messages,
                model=current_model,
                temperature=1,
                max_tokens=4096,
                top_p=1
            )

            ai_response = response.choices[0].message.content.strip()
            # Use typing effect for the assistant's response
            typing_effect(f"\n{Colors.CYAN}NEO: {Colors.RESET}{ai_response}")
            messages.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            typing_effect(f"{Colors.YELLOW}Error: {str(e)}{Colors.RESET}")


if __name__ == "__main__":
    chat_session()
