import google.generativeai as genai  # pip install google-generativeai
import tkinter as tk  # pip install tk
from tkinter import scrolledtext, Entry, Button
import os
import time  # For timestamps
import pyttsx3  # pip install pyttsx3 (For Text-to-Speech)
import speech_recognition as sr  # pip install SpeechRecognition (For Voice Input)
from PIL import Image, ImageTk  # pip install pillow

# Handling API Key Import 
try:
    from apikey import api_data  
    GENAI_API_KEY = api_data
except ModuleNotFoundError:
    GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    print("API Key not found! Please add an API key.")
    exit()

# Configure Gemini API
genai.configure(api_key=GENAI_API_KEY)

# Chat history to remember previous messages
chat_history = []

# Text-to-Speech Engine.
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speed
engine.setProperty('volume', 1.0)  # Adjust volume

# GUI Setup
root = tk.Tk()
root.title("Chatbot")
root.configure(bg="black")

# Load and resize images
try:
    user_img = Image.open("Icons/user_icon.png").resize((30, 30), Image.LANCZOS)
    user_icon = ImageTk.PhotoImage(user_img)

    chatbot_img = Image.open("Icons/chatbot_icon.png").resize((30, 30), Image.LANCZOS)
    chatbot_icon = ImageTk.PhotoImage(chatbot_img)

    send_img = Image.open("Icons/send_icon.png").resize((25, 25), Image.LANCZOS)
    send_icon = ImageTk.PhotoImage(send_img)

    mic_img = Image.open("Icons/mic_icon.png").resize((25, 25), Image.LANCZOS)
    mic_icon = ImageTk.PhotoImage(mic_img)

    # Set chatbot icon in the window title
    root.iconphoto(False, chatbot_icon)
except Exception as e:
    print(f"Error loading images: {e}")
    exit()

# Chatbot title with status indicator
title_frame = tk.Frame(root, bg="black")
title_frame.pack(pady=5)

status_dot = tk.Canvas(title_frame, width=10, height=10, bg="black", highlightthickness=0)
status_dot.create_oval(2, 2, 8, 8, fill="green")  # Green dot for active status
status_dot.pack(side=tk.LEFT, padx=5)

title_label = tk.Label(title_frame, text="Chatbot", font=("Arial", 16, "bold"), bg="black", fg="white", image=chatbot_icon, compound=tk.LEFT)
title_label.pack(side=tk.LEFT)

# Chat display area
conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12), bg="black", fg="white", state=tk.DISABLED)
conversation_area.pack(padx=10, pady=10)

def generate_response(query):
    """Generate a response considering previous chat history."""
    try:
        chat_history.append(f"You: {query}")
        full_prompt = "\n".join(chat_history)

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt, generation_config=genai.GenerationConfig(
            max_output_tokens=500,
            temperature=0.5
        )).text

        chat_history.append(f"Chatbot: {response}")

        # Speak the chatbot's response
        speak_text(response)

        return response
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

def send_message(event=None):
    """Get user input, display it with the user icon, show typing animation, generate response, and display chatbot reply."""
    query = user_input.get().strip()
    if query == "":
        return

    timestamp = time.strftime("%I:%M %p")  # Get current time

    # Enable text area
    conversation_area.config(state=tk.NORMAL)

    # Display user message
    user_frame = tk.Frame(conversation_area, bg="black")
    user_text = tk.Label(user_frame, text=query, font=("Arial", 12, "bold"), fg="lightgreen", bg="#1c1c1c", wraplength=500, justify="right", padx=10, pady=5)
    user_text.pack(side=tk.RIGHT, padx=5)
    user_label = tk.Label(user_frame, image=user_icon, bg="black")
    user_label.pack(side=tk.RIGHT)
    conversation_area.window_create(tk.END, window=user_frame)
    conversation_area.insert(tk.END, f"\n   {timestamp}\n", "timestamp")  # Timestamp

    user_input.delete(0, tk.END)

    # Typing indicator
    typing_label = tk.Label(conversation_area, text="Chatbot is typing...", font=("Arial", 10, "italic"), fg="gray", bg="black")
    conversation_area.window_create(tk.END, window=typing_label)
    conversation_area.insert(tk.END, "\n")
    conversation_area.see(tk.END)
    root.update()  # Refresh UI

    time.sleep(1.5)  # Simulate delay

    # Remove typing indicator
    conversation_area.config(state=tk.NORMAL)
    conversation_area.delete("end-2l", "end")

    # Generate chatbot response
    response = generate_response(query)

    # Display chatbot response
    bot_frame = tk.Frame(conversation_area, bg="black")
    bot_label = tk.Label(bot_frame, image=chatbot_icon, bg="black")
    bot_label.pack(side=tk.LEFT)
    bot_text = tk.Label(bot_frame, text=response, font=("Arial", 12, "bold"), fg="lightblue", bg="#282c34", wraplength=500, justify="left", padx=10, pady=5)
    bot_text.pack(side=tk.LEFT, padx=5)
    conversation_area.window_create(tk.END, window=bot_frame)
    conversation_area.insert(tk.END, f"\n   {timestamp}\n", "timestamp")  # Timestamp

    # Save chat history
    save_chat_history()

    # Disable text area to prevent user edits
    conversation_area.config(state=tk.DISABLED)
    conversation_area.see(tk.END)

def close_chat():
    """Close the chatbot window."""
    root.quit()

def clear_chat():
    """Clear the chat history from the GUI."""
    conversation_area.config(state=tk.NORMAL)
    conversation_area.delete(1.0, tk.END)
    conversation_area.config(state=tk.DISABLED)

def save_chat_history():
    """Save chat history to a text file."""
    with open("chat_history.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(chat_history))

def speak_text(text):
    """Convert chatbot's text response to speech."""
    engine.say(text)
    engine.runAndWait()

def voice_input():
    """Use speech recognition to take voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            conversation_area.config(state=tk.NORMAL)
            conversation_area.insert(tk.END, "\nListening...\n", "timestamp")
            conversation_area.config(state=tk.DISABLED)
            root.update()

            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio)
            user_input.delete(0, tk.END)
            user_input.insert(0, query)
            send_message()
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Could not request results")

# Buttons & Input Field
input_frame = tk.Frame(root, bg="black")
input_frame.pack(pady=5)

user_input = Entry(input_frame, font=("Arial", 14), width=50, bg="black", fg="white", insertbackground="white")
user_input.pack(side=tk.LEFT, padx=5)
user_input.bind("<Return>", send_message)

send_button = Button(input_frame, image=send_icon, command=send_message, bg="black", bd=0)
send_button.pack(side=tk.LEFT)

mic_button = Button(input_frame, image=mic_icon, command=voice_input, bg="black", bd=0)
mic_button.pack(side=tk.LEFT)

# Updated Exit & Clear Chat buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(side=tk.BOTTOM, pady=10, padx=10, anchor="se")

exit_button = Button(button_frame, text="Exit", font=("Arial", 12, "bold"), command=close_chat, bg="red", fg="white")
exit_button.pack(side=tk.RIGHT, padx=5)

clear_button = Button(button_frame, text="Clear Chat", font=("Arial", 12, "bold"), command=clear_chat, bg="gray", fg="white")
clear_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()