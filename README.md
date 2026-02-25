import os
import sys
import multiprocessing
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

# ---------------- CONFIGURATION ---------------- #

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FACE_SCAN_GIF = os.path.join(SCRIPT_DIR, "face_scan.gif")
BACKGROUND_GIF = os.path.join(SCRIPT_DIR, "loader.gif.gif")

# -------- LOCAL LLM (OLLAMA) -------- #

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

LOCAL_MODEL = "llama3"

# ---------------- TEXT TO SPEECH ---------------- #

def tts_worker(text):
    """Runs speech synthesis in a separate process."""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


# ---------------- AI BRAIN THREAD ---------------- #

class VardaanBrain(QThread):
    update_text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tts_process = None
        self.history = [
            {
                "role": "system",
                "content": (
                    "You are Vardaan, a highly intelligent AI system developed by Ayush. "
                    "Reply in short, crisp English with accurate facts. Maximum 2 sentences."
                ),
            }
        ]

    def speak(self, text):
        if self.tts_process and self.tts_process.is_alive():
            self.tts_process.terminate()

        self.tts_process = multiprocessing.Process(target=tts_worker, args=(text,))
        self.tts_process.start()

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            self.update_text_signal.emit("Listening...")
            recognizer.pause_threshold = 1

            try:
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=7)
                self.update_text_signal.emit("Recognizing...")
                query = recognizer.recognize_google(audio, language="en-in")
                return query.lower()

            except Exception:
                return None

    def run(self):
        self.update_text_signal.emit("Vardaan Online")

        while True:
            query = self.listen()

            if not query:
                continue

            if any(word in query for word in ["exit", "stop", "power off"]):
                self.update_text_signal.emit("Powering Off...")
                self.speak("Powering off.")
                os._exit(0)

            self.process_query(query)

    def process_query(self, query):
        try:
            self.update_text_signal.emit("Thinking...")
            self.history.append({"role": "user", "content": query})

            response = client.chat.completions.create(
                model=LOCAL_MODEL,
                messages=self.history,
                max_tokens=50,
                temperature=0.5,
            )

            reply = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": reply})

            self.update_text_signal.emit(reply)
            self.speak(reply)

        except Exception as e:
            print(e)
            self.update_text_signal.emit("Brain connection lost.")


# ---------------- UI INTERFACE ---------------- #

class VardaanInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vardaan AI Hub")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background:black;")
        self.setFocusPolicy(Qt.StrongFocus)

        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, 1200, 800)
        self.gif_label.setScaledContents(True)

        self.text_area = QTextEdit(self)
        self.text_area.setGeometry(50, 650, 1100, 120)
        self.text_area.setReadOnly(True)
        self.text_area.setAlignment(Qt.AlignCenter)
        self.text_area.setStyleSheet("""
            background:transparent;
            color:#00FBFF;
            font-size:24px;
            font-family:Consolas;
            border:none;
            font-weight:bold;
        """)

        self.brain = None
        self.start_scan_phase()

    def start_scan_phase(self):
        if os.path.exists(FACE_SCAN_GIF):
            movie = QMovie(FACE_SCAN_GIF)
            self.gif_label.setMovie(movie)
            movie.start()
        else:
            self.gif_label.setText("Face Scan GIF Missing")

        self.update_text("Scanning biometrics...")

        multiprocessing.Process(
            target=tts_worker,
            args=("Identity verified. Welcome Ayush.",),
        ).start()

        QTimer.singleShot(4000, self.start_main_phase)

    def start_main_phase(self):
        if os.path.exists(BACKGROUND_GIF):
            movie = QMovie(BACKGROUND_GIF)
            self.gif_label.setMovie(movie)
            movie.start()

        self.brain = VardaanBrain()
        self.brain.update_text_signal.connect(self.update_text)
        self.brain.start()

    def update_text(self, text):
        self.text_area.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.brain and self.brain.tts_process:
            if self.brain.tts_process.is_alive():
                self.brain.tts_process.terminate()
                self.update_text("Speech Interrupted")


# ---------------- ENTRY POINT ---------------- #

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = VardaanInterface()
    window.show()
    sys.exit(app.exec_())
