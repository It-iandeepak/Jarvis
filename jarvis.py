import openai
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv

load_dotenv()
print("API Key from .env:", os.getenv("OPENAI_API_KEY"))

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Speaking speed

import os
import random
import openai
import speech_recognition as sr

# Set your OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Your name so Jarvis can address you
USER_NAME = "Boss"

# Friendly greeting responses
GREETINGS = [
    f"Hello {USER_NAME}, how can I help you today?",
    f"Good to see you, {USER_NAME}. What's on your mind?",
    f"At your service, {USER_NAME}."
]

# Task acknowledgement responses
ACKNOWLEDGEMENTS = [
    "Right away.",
    "On it.",
    "Consider it done.",
    "Absolutely."
]

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        print("⚠️ Speech Recognition API error")
        return ""

def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        return f"Error: {str(e)}"

def speak(text, voice="Alex"):
    # Use macOS 'say' with a natural voice
    os.system(f'say -v {voice} "{text}"')

def main():
    # Greet when starting
    greet = random.choice(GREETINGS)
    print(f"🤖 Jarvis: {greet}")
    speak(greet)

    while True:
        query = listen()
        if not query:
            continue

        if query.lower() in ["exit", "quit", "stop"]:
            speak(f"Goodbye {USER_NAME}. Until next time.")
            break

        if "open chrome" in query.lower():
            speak(random.choice(ACKNOWLEDGEMENTS))
            os.system("open -a 'Google Chrome'")
            continue

        # Get AI response
        reply = ask_chatgpt(query)
        print(f"🤖 Jarvis: {reply}")
        speak(reply)

if __name__ == "__main__":
    main()
