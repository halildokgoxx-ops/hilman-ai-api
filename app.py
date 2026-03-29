import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # Diğer sitelerden erişim için gerekli

# --- HİLMAN-AI AYARLARI ---
# Kendi belirlediğin API anahtarın (Kaggle'da bunu kullanacaksın)
MY_KEY = "Hilman-123456789" 

# Groq API Anahtarın
GROQ_KEY = "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"

# En güncel Llama modeli (llama3-70b-8192 yerine bu geldi)
MODEL_NAME = "llama-3.3-70b-versatile"

@app.route('/')
def home():
    return "<h1>🤖 HilmanAI API Sistemi Aktif!</h1><p>Sürüm: 1.0.1 - Durum: 7/24 Cevap Vermeye Hazır.</p>"

@app.route('/v1/chat', methods=['POST'])
def chat():
    # 1. Güvenlik Kontrolü (API Key Doğrulama)
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {MY_KEY}":
        return jsonify({"error": "Yetkisiz Erişim: Hilman Key Hatalı!"}), 401

    # 2. Gelen Mesajı Al
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Mesaj içeriği eksik!"}), 400
        
    user_msg = data.get("message", "")

    # 3. Groq API ile İletişim Kur
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Sen HilmanAI'sın. Çok zeki, profesyonel bir yazılım mühendisi ve yaratıcı bir asistansın."},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7
    }

    try:
        # Groq'a gönder (25 saniye zaman aşımı ekledik)
        response = requests.post(url, json=payload, headers=headers, timeout=25)
        res_data = response.json()

        # Yanıtı Kontrol Et ve Gönder
        if 'choices' in res_data:
            return jsonify({
                "status": "success",
                "model": "HilmanAI-v1",
                "response": res_data['choices'][0]['message']['content']
            })
        else:
            # Groq tarafındaki hata mesajını yakala
            groq_error = res_data.get('error', {}).get('message', 'Bilinmeyen Groq hatası')
            return jsonify({"error": f"Groq Hatasi: {groq_error}"}), 502

    except Exception as e:
        return jsonify({"error": f"HilmanAI Sunucu Hatasi: {str(e)}"}), 500

if __name__ == "__main__":
    # Render'ın portunu otomatik ayarla
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
