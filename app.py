import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# AYARLAR (Burası Çok Kritik)
MY_KEY = "Hilman-123456789" 
GROQ_KEY = "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"

@app.route('/')
def home():
    return "<h1>HilmanAI Online!</h1>"

@app.route('/v1/chat', methods=['POST'])
def chat():
    # Header Kontrolü
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {MY_KEY}":
        return jsonify({"error": f"Yetkisiz! Beklenen: Bearer {MY_KEY}, Gelen: {auth}"}), 401

    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Mesaj eksik"}), 400

    # Groq API'ye Gönder
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": data['message']}]
        }
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render'ın verdiği portu kullan, yoksa 5000'den aç
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
