# AI Customer Support Chatbot

A lightweight, production-ready AI customer support chatbot built with **Python (Flask)**, **HTML**, **TailwindCSS**, and **JavaScript**, using **Google Gemini** as the generative model. The project reads company information from `faq.txt`, uses a structured prompt from `prompt_template.txt`, and issues requests to Gemini using an API key stored in a `.env` file.

---

## Features
- AI-powered responses using Gemini (via API key)
- Contextual knowledge injection from `faq.txt`
- Configurable personality and instructions via `prompt_template.txt`
- Modern frontend with TailwindCSS (CDN) and vanilla JS
- Simple Flask backend with a `/chat` endpoint
- Secure handling of API keys using `.env`
- Dockerfile and setup scripts for easy deployment

---

## Quickstart (local)

1. Clone repository:
```bash
git clone https://github.com/your-username/your-chatbot.git
cd your-chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (Powershell)
venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` in project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_APP=app.py
```

5. Run the app:
```bash
python app.py
```

6. Open your browser at `http://127.0.0.1:5000`

---

## Project Structure

```
chatbot/
├── app.py
├── requirements.txt
├── Dockerfile
├── setup.sh
├── .env.example
├── .gitignore
├── faq.txt
├── prompt_template.txt
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

---

## How it works (high-level)
1. Frontend sends user message to `/chat` endpoint via fetch.
2. Backend loads `prompt_template.txt` and `faq.txt`, constructs a system prompt and user prompt.
3. Backend calls Gemini API with the composed prompt and returns the model reply to the frontend.
4. Frontend renders the assistant response.

---

## Files of interest

- `faq.txt` — Company information and FAQs fed into prompts for domain knowledge.
- `prompt_template.txt` — System instructions and templates used to control model behavior.
- `app.py` — Flask app with `/` and `/chat` endpoints and Gemini API interaction.
- `templates/index.html` — Frontend UI using TailwindCSS and vanilla JS.
- `static/js/script.js` — Handles sending messages and updating the UI.

---

## Deployment

### Docker (production)
Build:
```bash
docker build -t chatbot:latest .
```
Run:
```bash
docker run -p 5000:5000 --env-file .env chatbot:latest
```

### Gunicorn (on VPS)
```bash
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:8000 app:app
```

---

## Security & Best Practices
- Never commit `.env` containing `GEMINI_API_KEY`.
- Use HTTPS in production.
- Add rate limiting and authentication on the `/chat` endpoint if exposing publicly.
- Log minimal user data and respect privacy.

---

## Contributing
See `CONTRIBUTING.md` for guidelines.

---

## License
This project is released under the MIT License. See `LICENSE`.

