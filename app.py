import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Use print statement instead of raising an error for deployment flexibility
    print("❌ WARNING: GEMINI_API_KEY not found. AI functionality will be disabled.")

# Configure Gemini (only if key exists)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Load files helper function
def load_txt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ WARNING: File not found: {path}. Using empty content.") 
        return ""

app = Flask(__name__)

@app.route("/")
def index():
    """Renders the main chat interface."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chat requests, constructs prompt, and calls the Gemini API."""
    
    # 1. Check for API key availability immediately
    if not GEMINI_API_KEY:
        return jsonify({"reply": "API Key is missing on the server. AI functionality is disabled."}), 503

    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            # Use 'reply' key consistently for frontend error messages
            return jsonify({"reply": "Empty message."}), 400

        # Load prompt template & FAQ
        prompt_template = load_txt("prompt_template.txt")
        faq = load_txt("faq.txt")

        # Construct the final prompt for the AI
        system_prompt = (
            prompt_template + "\n\n---\nCompany FAQ:\n" + faq + "\n\n"
        )
        final_prompt = system_prompt + f"User: {user_msg}\nAssistant:"

        # Call Gemini Flash model
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(final_prompt)

        reply = response.text if response and response.text else "No response from model."

        # Return the response using the 'reply' key, which the JS expects
        return jsonify({"reply": reply})

    except Exception as e:
        # Logging detailed error to server console
        print(f"ERROR processing chat request: {e}")
        return jsonify({"reply": "Sorry — there was an error contacting the AI backend."}), 500


if __name__ == "__main__":
    app.run(debug=True)
