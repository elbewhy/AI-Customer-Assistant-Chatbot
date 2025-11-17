import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

app = Flask(__name__)

# Helper: load file content
def load_txt(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'empty message'}), 400

    # Load prompt template and FAQ
    prompt_template = load_txt('prompt_template.txt')
    faq = load_txt('faq.txt')

    # Construct the prompt for the model
    system_prompt = prompt_template + "\n\nCompany FAQ:\n" + faq
    # A simple user prompt wrapper
    user_prompt = f"User: {user_message}"

    # Build the payload for Gemini (this uses a generic REST POST example; adjust as per your SDK)
    payload = {
        "prompt": system_prompt + "\n\n" + user_prompt,
        "max_output_tokens": 512
    }

    # NOTE: You must replace the endpoint below with the official Gemini API endpoint/SDK call.
    GEMINI_ENDPOINT = os.getenv('GEMINI_ENDPOINT', 'https://api.example.com/v1/generate')

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(GEMINI_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=30)
        resp.raise_for_status()
        result = resp.json()
        # The structure depends on the API—here we expect a simple 'text' field
        assistant_text = result.get('output', result.get('text', 'Sorry, no response from model.'))
    except Exception as e:
        assistant_text = "Sorry — there was an error contacting the AI backend."

    return jsonify({"reply": assistant_text})

if __name__ == '__main__':
    app.run(debug=True)
