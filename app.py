import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Instead of raising, we can log and use an error message if the key is missing
    print("❌ WARNING: GEMINI_API_KEY not found. AI functionality will be disabled.")

# Configure Gemini (only if key exists)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Load files
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
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({"reply": "API Key is missing on the server. Please check the .env file."}), 503

    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({"reply": "Empty message."}), 400

        # Load prompt template & FAQ
        prompt_template = load_txt("prompt_template.txt")
        faq = load_txt("faq.txt")

        # Construct system prompt (using the standard prompt template)
        system_prompt = (
            prompt_template + "\n\n---\nCompany FAQ:\n" + faq + "\n\n"
        )
        final_prompt = system_prompt + f"User: {user_msg}\nAssistant:"

        # Gemini Flash model
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(final_prompt)

        reply = response.text if response and response.text else "No response from model."

        # The key 'reply' is sent to the frontend
        return jsonify({"reply": reply})

    except Exception as e:
        # Logging detailed error to server console
        print(f"ERROR processing chat request: {e}")
        return jsonify({"reply": "Sorry — there was an error contacting the AI backend."}), 500


if __name__ == "__main__":
    app.run(debug=True)
