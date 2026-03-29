import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

MY_KEY = "Hilman-123456789" 
GROQ_KEY = "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"

@app.route('/')
def home():
    return "HilmanAI Online"

@app.route('/v1/chat', methods=['POST'])
def chat():
    # Yetki Kontrolü
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {MY_KEY}":
        return jsonify({"error": "Gecersiz Hilman Key"}), 401

    data = request.get_json(silent=True)
    user_msg = data.get("message", "Merhaba")

    # Groq API Çağrısı
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": user_msg}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        res_data = response.json()

        # KRİTİK DÜZELTME: 'choices' var mı kontrol et
        if 'choices' in res_data:
            return jsonify({
                "status": "success",
                "response": res_data['choices'][0]['message']['content']
            })
        else:
            # Groq hata döndürdüyse hatayı yazdır
            error_msg = res_data.get('error', {}).get('message', 'Bilinmeyen Groq hatası')
            return jsonify({"error": f"Groq Hatasi: {error_msg}"}), 502

    except Exception as e:
        return jsonify({"error": f"Sunucu Hatasi: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
