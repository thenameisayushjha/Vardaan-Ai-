# Vardaan-Ai-
A professional Python-based virtual assistant for task automaticimport pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import sys
import time
import re
import webbrowser
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QThread

# --- CONFIGURATION & PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: Ensure these assets are in the same directory as the script
BG_PATH = os.path.join(SCRIPT_DIR, "bg.gif")
LOADER_PATH = os.path.join(SCRIPT_DIR, "loader.gif")

class VardaanBrain(QThread):
    """
    Background thread to handle voice recognition and logic 
    without freezing the main GUI window.
    """
    def __init__(self):
        super().__init__()

    def run(self):
        self.wish_user()
        while True:
            self.query = self.capture_voice_input()
            if self.query != "none":
                self.process_logic(self.query)

    def speak(self, text):
        """Standard Text-to-Speech Engine Initialization"""
        print(f"Vardaan: {text}")
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', 180)
            # Remove brackets and extra whitespace for cleaner speech
            clean_text = re.sub(r'\([^)]*\)', '', text).replace('\n', ' ')
            engine.say(clean_text)
            engine.runAndWait()
        except Exception as e:
            print(f"Speech Engine Error: {e}")

    def capture_voice_input(self):
        """Converts audio from the microphone into string format"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("\nListening for commands...")
            r.pause_threshold = 1
            r.energy_threshold = 400 
            try:
                audio = r.listen(source, timeout=None, phrase_time_limit=8)
                print("Recognizing speech...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User Request: {query}\n")
            except Exception:
                return "none"
            return query.lower()

    def process_logic(self, query):
        """Main Command Logic Processor"""
        
        # System Commands
        if any(cmd in query for cmd in ['exit', 'quit', 'shutdown', 'goodbye']):
            self.speak("System shutting down. Goodbye, Ayush.")
            sys.exit()

        # Web & Search Commands
        elif 'youtube search' in query or 'play' in query:
            self.speak("Searching YouTube...")
            search_query = query.replace("youtube search", "").replace("play", "").replace("on youtube", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif 'open google' in query:
            self.speak("What should I search for you, Sir?")
            search_data = self.capture_voice_input()
            if search_data != "none":
                webbrowser.open(f"https://www.google.com/search?q={search_data}")

        # Information Retrieval
        elif 'wikipedia' in query or 'who is' in query or 'what is' in query:
            self.speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia...")
                self.speak(summary)
            except Exception:
                self.speak("I couldn't find any relevant information on Wikipedia.")

        # Automation & Utilities
        elif 'open notepad' in query:
            self.speak("Opening Notepad.")
            os.system("notepad")

        elif 'the time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")

        elif 'identity' in query or 'who are you' in query:
            self.speak("I am Vardaan, your customized AI desktop assistant.")

    def wish_user(self):
        """Initial Greeting Logic based on local time"""
        time.sleep(1)
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning, Ayush.")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon, Ayush.")
        else:
            self.speak("Good Evening, Ayush.")
        self.speak("System initialized. I am now online.")


class VardaanInterface(QMainWindow):
    """Main Graphical User Interface class using PyQt5"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Vardaan AI Assistant")
        self.setFixedSize(1200, 800)
        
        # Black Background Styling
        self.setStyleSheet("background-color: black;")

        # Background Animation Label
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1200, 800)
        if os.path.exists(BG_PATH):
            self.movie_bg = QMovie(BG_PATH)
            self.bg_label.setMovie(self.movie_bg)
            self.movie_bg.start()

        # Core Animation (Arc Reactor/Earth)
        self.loader_label = QLabel(self)
        self.loader_label.setGeometry(350, 150, 500, 500)
        self.loader_label.setAlignment(Qt.AlignCenter)
        if os.path.exists(LOADER_PATH):
            self.movie_loader = QMovie(LOADER_PATH)
            self.loader_label.setMovie(self.movie_loader)
            self.movie_loader.start()
        else:
            self.loader_label.setText("ANIMATION_NOT_FOUND")
            self.loader_label.setStyleSheet("color: #00e5ff; font-weight: bold;")

        self.launch_brain()

    def launch_brain(self):
        self.brain_thread = VardaanBrain()
        self.brain_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    terminal_ui = VardaanInterface()
    terminal_ui.show()
    sys.exit(app.exec_())
    
