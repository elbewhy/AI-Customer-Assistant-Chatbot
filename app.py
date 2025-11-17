import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load files
def load_txt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({"error": "Empty message"}), 400

        # Load prompt template & FAQ
        prompt_template = load_txt("prompt_template.txt")
        faq = load_txt("faq.txt")

        system_prompt = (
            prompt_template + "\n\n---\nCompany FAQ:\n" + faq + "\n\n"
        )

        final_prompt = system_prompt + f"User: {user_msg}\nAssistant:"

        # Gemini Flash model
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(final_prompt)

        reply = response.text if response and response.text else "No response from model."

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Sorry — there was an error contacting the AI backend."}), 500


if __name__ == "__main__":
    app.run(debug=True)
