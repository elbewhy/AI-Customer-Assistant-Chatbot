import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ WARNING: GEMINI_API_KEY not found. AI responses will not work.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

def load_txt(path):
    """Helper to read text files safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ File missing: {path}")
        return ""

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({"reply": "Server error: API key missing."}), 503

    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({"reply": "Please enter a message."}), 400

        # Load texts
        prompt_template = load_txt("prompt_template.txt")
        faq = load_txt("faq.txt")

        system_prompt = (
            prompt_template +
            "\n\n---\nCompany FAQ:\n" +
            faq +
            "\n\n"
        )

        final_prompt = f"{system_prompt}\nUser: {user_msg}\nAssistant:"

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(final_prompt)

        reply = response.text if response and response.text else "No response from server."

        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"reply": "Server error while processing request."}), 500


if __name__ == "__main__":
    app.run(debug=True)
    
