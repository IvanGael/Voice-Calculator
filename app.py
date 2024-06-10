# pip install SpeechRecognition pyttsx3 pyaudio

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import re

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to perform arithmetic operation
def perform_operation(operation):
    try:
        # Replace verbal commands with symbols
        operation = operation.lower()
        operation = re.sub(r'plus', '+', operation)
        operation = re.sub(r'minus', '-', operation)
        operation = re.sub(r'times', '*', operation)
        operation = re.sub(r'divided by', '/', operation)
        operation = re.sub(r'into', '*', operation)
        operation = re.sub(r'divide by', '/', operation)
        operation = re.sub(r'over', '/', operation)
        operation = re.sub(r'%', '/100', operation)
        
        result = eval(operation)
        return result
    except Exception as e:
        return str(e)

# Function to listen for voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            result = perform_operation(command)
            entry_var.set(result)
            update_history(command, result)
            speak_result(result)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results; check your network connection")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Function to provide spoken feedback
def speak_result(result):
    engine.say(f"The result is {result}")
    engine.runAndWait()

# Function to update history
def update_history(command, result):
    history_listbox.insert(tk.END, f"{command} = {result}")

# Create the main window
root = tk.Tk()
root.title("Voice-Activated Calculator")

# Create an entry widget
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
entry.grid(row=0, column=0, columnspan=4)

# Create a button to activate the voice command
listen_button = tk.Button(root, text="Listen", padx=20, pady=20, font=("Arial", 18), command=listen)
listen_button.grid(row=1, column=0, columnspan=4)

# Create a history listbox
history_label = tk.Label(root, text="History", font=("Arial", 18))
history_label.grid(row=2, column=0, columnspan=4)
history_listbox = tk.Listbox(root, height=10, width=50, font=("Arial", 14))
history_listbox.grid(row=3, column=0, columnspan=4)

root.mainloop()
