# SQL MATE

A focused LLM chatbot built with Flask and the Google Gemini API.

## Files
- `app.py` — Flask server and Gemini chatbot logic. API key and port are directly configurable here.
- `config.py` — SQL MATE identity, behavior, and strict domain instructions.
- `requirements.txt` — Python dependencies.
- `templates/index.html` — Complete UI with HTML, CSS, and JavaScript in one file.

## Run
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Open `app.py` and replace `PASTE_YOUR_GEMINI_API_KEY_HERE` with your Gemini API key.
5. Run `python app.py`.
6. Open `http://127.0.0.1:5000`.

Change `PORT` in `app.py` if you want another port.

## Security note
For local learning this setup keeps the key in `app.py` as requested. Do not commit a real API key to a public GitHub repository or expose it in frontend JavaScript.
