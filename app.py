from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from config import SYSTEM_INSTRUCTION
import os

# ============================================================
# SQL MATE - Configuration
# Change these variables as needed.
# ============================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-lite"
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

app = Flask(__name__)

# Create Gemini client only when an API key is configured.
client = None
if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("PASTE_"):
    client = genai.Client(api_key=GEMINI_API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    global client

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if client is None:
        return jsonify({
            "error": "Gemini API key is not configured. Open app.py and replace "
                     "PASTE_YOUR_GEMINI_API_KEY_HERE with your API key."
        }), 500

    # Keep a reasonable conversation window so the app stays lightweight.
    clean_history = []
    if isinstance(history, list):
        for item in history[-12:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = str(item.get("content", "")).strip()
            if role in ("user", "model") and content:
                clean_history.append({
                    "role": role,
                    "parts": [{"text": content}]
                })

    try:
        # The domain behavior is enforced primarily through config.py.
        # The latest user message is appended after the previous turns.
        contents = clean_history + [
            {"role": "user", "parts": [{"text": message}]}
        ]

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3,
                max_output_tokens=2048,
            ),
        )

        answer = getattr(response, "text", None)
        if not answer:
            answer = "I couldn't generate a response right now. Please try again."

        return jsonify({"answer": answer})

    except Exception as exc:
        return jsonify({
            "error": f"Gemini request failed: {str(exc)}"
        }), 500


if __name__ == "__main__":
    print(f"SQL MATE running on http://127.0.0.1:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
