from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # Diğer sitelerin senin API'ne bağlanabilmesi için

# --- AYARLAR ---
HILMAN_MASTER_KEY = "Hilman-123456789" # Kendi özel anahtarın
GROQ_API_KEY = "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"

@app.route('/v1/chat', methods=['POST'])
def hilman_api():
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {HILMAN_MASTER_KEY}":
        return jsonify({"error": "Yetkisiz erişim! HilmanAI anahtarı geçersiz."}), 403

    data = request.json
    user_message = data.get("message", "")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Sen HilmanAI'sın. Çok zeki ve profesyonelsin."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return jsonify({
            "status": "success",
            "model": "HilmanAI-v1",
            "response": result['choices'][0]['message']['content']
        })
    except:
        return jsonify({"error": "Sistem meşgul, sonra tekrar dene."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
