# 🤖 AI Enabled Chatbot (Python + Gemini API + Voice Assistant)
A fully interactive AI Enabled chatbot built using Python, Gemini API, Tkinter GUI, Speech Recognition &amp; Text-to-Speech. The bot supports voice input, spoken responses, clean chat UI with icons, timestamps, message bubbles, typing indicator, and chat history saving. A minimal personal assistant -> open -> speak/text -> get smart replies instantly.

# ✨ Features
GUI chat window with sender/receiver message bubbles	
Voice input using SpeechRecognition	
Text-to-speech chatbot voice replies	
Gemini-powered responses with chat history context	
Custom icons for user & bot	
Typing indicator animation	
Timestamps for each message	
Chat history saved locally	
Clear chat & exit buttons

# 🛠 Tech Used
Python - Core logic
Tkinter -	GUI Interface
Google Gemini API -	Chat responses
SpeechRecognition -	Voice Input
pyttsx3 -	Text-to-speech output
Pillow - Icons + image handling

# 🚀 Setup & Installation
1️⃣ Install requirements
pip install google-generativeai pillow SpeechRecognition pyttsx3
You also need tkinter (pre-installed in most Python setups).

2️⃣ Add your Gemini API Key
Create apikey.py inside project folder:
api_data = "YOUR_API_KEY_HERE"
(or set as environment variable GENAI_API_KEY)

3️⃣ Run the App
python CHATTERBOT.py

# 📌 Future Enhancements
Chat export as PDF
Dark/Light theme toggle
Emotion-based responses using sentiment detection
Whisper + streaming voice chat

# If you like this project → leave a ⭐ on GitHub, it’ll make my whole day ✨
