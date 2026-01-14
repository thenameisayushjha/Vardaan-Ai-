# Vardaan-Ai-
A professional Python-based virtual assistant for task automatic 

import pyttsx3
import datetime
import sys

class VardaanAI:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.set_voice()

    def set_voice(self):
        voices = self.engine.getProperty('voices')
        # Setting a professional male voice
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180) # Professional speed

    def speak(self, text):
        print(f"Vardaan: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def greet_user(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good morning. Systems are online.")
        elif 12 <= hour < 18:
            self.speak("Good afternoon. How can I assist you today?")
        else:
            self.speak("Good evening. Vardaan AI is at your service.")

    def run(self):
        self.greet_user()
        while True:
            query = input("\nUser Query: ").lower()

            if 'exit' in query or 'terminate' in query:
                self.speak("Shutting down systems. Goodbye.")
                sys.exit()

            elif 'status' in query:
                self.speak("All systems are functioning within normal parameters.")

            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%H:%M")
                self.speak(f"The current time is {current_time}.")

            elif 'identity' in query or 'who are you' in query:
                self.speak("I am Vardaan, a virtual assistant designed for task automation and system management.")

            else:
                self.speak("Command not recognized. Please refine your query.")

if __name__ == "__main__":
    assistant = VardaanAI()
    assistant.run()
    
