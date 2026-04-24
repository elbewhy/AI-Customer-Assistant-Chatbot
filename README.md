# Sunlite Energy AI Customer Assistant Chatbot

![Chatbot Demo](https://img.shields.io/badge/Status-Live-green)

A responsive, AI-powered customer support chatbot for Sunlite Energy, built with Python, Flask, Tailwind CSS, and JavaScript. This project demonstrates full-stack development, API integration, and real-time AI interactions for customer service.

---

## 🌟 Live Demo
Try the chatbot live here: [AI Customer Assistant](https://ai-customer-assistant-chatbot.onrender.com)

---

## 🛠️ Features
- AI-powered conversation using Google Gemini API.
- Dynamic FAQ integration via `faq.txt`.
- Responsive, WhatsApp-style chat UI with Tailwind CSS.
- Mobile-friendly input field and fully visible send button.
- Smooth auto-scroll to the latest messages.
- Easy configuration via `.env` file for API keys.
- Full-stack Flask application with HTML, CSS, and JS.

---

## 📂 Project Structure

AI-Customer-Assistant-Chatbot/
│
├─ app.py # Flask backend
├─ requirements.txt # Python dependencies
├─ .env # API key and configuration
├─ prompt_template.txt # AI prompt template
├─ faq.txt # Company FAQ data
├─ templates/
│ └─ index.html # Main frontend HTML
└─ static/
├─ css/
│ └─ style.css # Tailwind + custom CSS
└─ js/
└─ script.js # JS for chat functionality


---

## ⚡ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/elbewhy/Sunlite-Energy-AI-Assistant-Chatbot.git
   cd Sunlite-Energy-AI-Assistant-Chatbot

2. Create and Activate Virtual environment:

   python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create .env file in the root:

   GEMINI_API_KEY=your_api_key_here
GEMINI_ENDPOINT=https://api.example.com/v1/generate

5. Run the app locally:
   python app.py


🎨 Frontend
Built with Tailwind CSS for a modern, responsive design.

Input area + send button fully responsive on mobile.

Chat bubbles for user & AI messages with smooth scrolling.

🤖 Backend
Flask backend handles /chat POST requests.

Reads prompts from prompt_template.txt and FAQs from faq.txt.
Sends requests to Gemini API using requests library.

📈 Future Improvements

Add authentication for admin and customer users.

Support multi-language responses.

Add voice input/output for accessibility.

Deploy a custom AI model for domain-specific queries.

📧 Contact

Developed by Abubakar Ruwa
Email: abubakarruwa5@gmail.com

Phone: +2347062255636

