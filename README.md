# Vardaan-Ai-
A professional Python-based virtual assistant for task automatic 

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import sys
import threading
import time
import re

class VardaanAI:
    def __init__(self):
        # Initializing the voice engine
        self.engine = pyttsx3.init('sapi5')
        self.setup_voice()

    def setup_voice(self):
        """Sets professional male voice and speed."""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 175)

    def speak_worker(self, text):
        """Threaded worker for voice output to prevent system freeze."""
        try:
            # Sanitizing text for smooth speech
            clean_text = re.sub(r'\([^)]*\)', '', text)
            clean_text = clean_text.replace('\n', ' ')
            
            # Fresh engine initialization per thread for stability
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 175)
            engine.say(clean_text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Speaker Error: {e}")

    def speak(self, text):
        """Prints output to console and triggers speech."""
        print(f"Vardaan: {text}")
        t = threading.Thread(target=self.speak_worker, args=(text,))
        t.start()
        t.join()

    def take_command(self):
        """Listens to microphone and recognizes user speech."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("\nListening for commands...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                print("Recognizing speech...")
                query = r.recognize_google(audio, language='en-US')
                print(f"User said: {query}\n")
            except Exception:
                return "None"
            return query.lower()

    def greet_user(self):
        """Greet user based on current time."""
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good morning. Systems initialized.")
        elif 12 <= hour < 18:
            self.speak("Good afternoon. Systems are active.")
        else:
            self.speak("Good evening. Systems online.")
        self.speak("I am Vardaan. How can I assist you today?")

    def handle_query(self, query):
        """Core logic to handle user requests."""
        
        # 1. Termination
        if any(cmd in query for cmd in ['exit', 'stop', 'quit', 'bye']):
            self.speak("Deactivating systems. Have a great day!")
            sys.exit()

        # 2. Wikipedia & Knowledge Retrieval
        elif any(keyword in query for keyword in ['wikipedia', 'who is', 'what is', 'tell me about']):
            self.speak("Processing search request...")
            
            # Sanitizing the query for search
            search_query = query.replace("wikipedia", "").replace("who is", "").replace("tell me about", "").replace("what is", "").strip()
            
            try:
                search_results = wikipedia.search(search_query)
                if not search_results:
                    self.speak("I could not find any relevant information on the requested topic.")
                    return
                
                target_page = search_results[0]
                self.speak(f"Retrieving data for {target_page}...")
                
                results = wikipedia.summary(target_page, sentences=2, auto_suggest=False)
                self.speak("According to Wikipedia sources:")
                self.speak(results)
                
            except wikipedia.DisambiguationError as e:
                self.speak("Multiple entries found. Retrieving information from the primary source.")
                res = wikipedia.summary(e.options[0], sentences=2, auto_suggest=False)
                self.speak(res)
            except Exception as e:
                print(f"System Error: {e}")
                self.speak("I am currently experiencing connection issues with the knowledge database.")

        # 3. Time Retrieval
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")

        # 4. Identity Check
        elif 'who are you' in query:
            self.speak("I am Vardaan, an advanced virtual assistant designed for information retrieval and task automation.")

        # 5. Default Response
        else:
            self.speak("Command received, but it's currently beyond my operational scope.")

    def run(self):
        """Starting the assistant loop."""
        self.greet_user()
        while True:
            query = self.take_command()
            if query != "None":
                self.handle_query(query)

if __name__ == "__main__":
    assistant = VardaanAI()
    assistant.run()

