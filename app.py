<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vardaan AI</title>
    <script src="[https://cdn.jsdelivr.net/npm/marked/marked.min.js](https://cdn.jsdelivr.net/npm/marked/marked.min.js)"></script>
    <style>
        body {
            background-color: #000000;
            color: #00FBFF;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            height: 90vh;
            justify-content: space-between;
        }
        #chat-box {
            flex-grow: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            border: 2px solid #00FBFF;
            padding: 15px;
            border-radius: 15px;
            text-align: left;
            font-size: 18px;
            box-shadow: 0 0 10px #00FBFF;
        }
        .user-msg { color: #ffffff; margin: 10px 0; }
        .vardaan-msg { color: #00FBFF; margin: 10px 0; }
        
        /* Code Box ka naya design */
        pre {
            background-color: #1a1a1a;
            color: #00ff00;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #00FBFF;
        }
        code {
            font-family: Consolas, monospace;
        }

        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
        }
        #mic-btn {
            background-color: transparent;
            border: 2px solid #00FBFF;
            color: #00FBFF;
            padding: 15px 30px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 0 10px #00FBFF;
            transition: 0.3s;
        }
        #mic-btn.listening {
            background-color: #00FBFF;
            color: #000000;
        }
        /* Naya Stop Button */
        #stop-btn {
            background-color: #ff0033;
            border: 2px solid #ff0033;
            color: white;
            padding: 15px 30px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 0 10px #ff0033;
            display: none; /* Starting mein chupa rahega */
        }
    </style>
</head>
<body>

    <h1>VARDAAN AI</h1>
    <div id="chat-box"></div>

    <div class="controls">
        <button id="mic-btn" onclick="startListening()">Tap to Speak 🎙️</button>
        <button id="stop-btn" onclick="stopSpeaking()">🛑 Stop</button>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const micBtn = document.getElementById('mic-btn');
        const stopBtn = document.getElementById('stop-btn');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';

        const synth = window.speechSynthesis;

        function addMessage(sender, text, className) {
            // Agar Vardaan bol raha hai, toh marked.js usko proper box banayega
            let formattedText = (sender === "Vardaan") ? marked.parse(text) : text;
            chatBox.innerHTML += `<div class="${className}"><b>${sender}:</b> ${formattedText}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function speakText(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0; 
            
            // Jab aawaz shuru ho, stop button dikhao
            utterance.onstart = () => { stopBtn.style.display = "inline-block"; };
            // Jab aawaz khatam ho, stop button chupa do
            utterance.onend = () => { stopBtn.style.display = "none"; };
            
            synth.speak(utterance);
        }

        // NAYA: Stop button ka asli logic
        function stopSpeaking() {
            synth.cancel(); // Aawaz turant band
            stopBtn.style.display = "none"; // Button gayab
            micBtn.innerText = "Tap to Speak 🎙️";
            micBtn.classList.remove("listening");
        }

        function startListening() {
            synth.cancel(); // Naya sunne se pehle purana band karo
            stopBtn.style.display = "none";
            recognition.start();
            micBtn.innerText = "Listening...";
            micBtn.classList.add("listening");
        }

        recognition.onresult = async (event) => {
            const userQuery = event.results[0][0].transcript;
            micBtn.innerText = "Thinking...";
            micBtn.classList.remove("listening");
            
            addMessage("Ayush", userQuery, "user-msg");

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: userQuery })
                });
                
                const data = await response.json();
                const reply = data.reply;
                
                // Code box fix wale text ko HTML mein dalo
                addMessage("Vardaan", reply, "vardaan-msg");
                
                // Par bolne ke liye raw text bhejo taaki aawaz atke nahi
                speakText(reply); 
                
                micBtn.innerText = "Tap to Speak 🎙️";
            } catch (error) {
                addMessage("System", "Error: Server connection failed.", "vardaan-msg");
                micBtn.innerText = "Tap to Speak 🎙️";
            }
        };

        recognition.onerror = (event) => {
            micBtn.innerText = "Tap to Speak 🎙️";
            micBtn.classList.remove("listening");
        };
    </script>
</body>
</html>
