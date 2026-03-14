import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app) 

# Render ab API key environment variable se lega, code se nahi
groq_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
CLOUD_MODEL = "llama-3.1-8b-instant"

history = [
    {"role": "system", "content": "You are Vardaan, a highly intelligent mobile AI system developed by Ayush under VAJRA Tech. Act exactly like ChatGPT: answer fully, be direct, and highly informative. No length limits. Always communicate in clear, professional English."}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global history
    data = request.json
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"reply": "I couldn't hear that clearly."})

    history.append({"role": "user", "content": user_query})
    
    try:
        response = client.chat.completions.create(
            model=CLOUD_MODEL,
            messages=history,
            max_tokens=2048,
            temperature=0.6
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        
        if len(history) > 15:
            history = [history[0]] + history[-10:]
            
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "System Error: Brain connection lost."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)