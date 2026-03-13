import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app) 

# It's best practice to use environment variables for API keys
# Set 'GROQ_API_KEY' in your system or hosting environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Error: GROQ_API_KEY environment variable is not set!")

# Groq API Setup
client = Groq(api_key=GROQ_API_KEY)
CLOUD_MODEL = "llama-3.1-8b-instant"

history = [
    {"role": "system", "content": "You are Vardaan, a highly intelligent mobile AI system developed by Ayush under VAJRA Tech. Act exactly like ChatGPT: answer fully, be direct, and highly informative. No length limits."}
]

# The route that renders your app's frontend (HTML)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global history
    data = request.json
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"reply": "No input received."})

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
        
        # Managing memory to avoid crossing context limits
        if len(history) > 15:
            history = [history[0]] + history[-10:]
            
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "System Error: Connection to the brain lost."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
