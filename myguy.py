import struct
import pyaudio
import subprocess
import speech_recognition as sr
import pyttsx3
import pvporcupine
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)






def main():
    # Path to your Porcupine wake word model
    model_file_path = "C:\\Users\\User\\Desktop\\projects\\learn\\my-guy-open--me_en_windows_v3_0_0.ppn"

    # Your access key obtained from Porcupine
    access_key = "m4isCpKV3TFqfzBiSpSEaXt/0CmzZMaOwuQ9SjOhtJzaAkz4mltTyQ=="

    # Initialize Porcupine with the wake word model and access key
    handle = pvporcupine.create(
        keyword_paths=[model_file_path], 
        sensitivities=[0.5], 
        access_key=access_key)

    # Initialize PyAudio
    pa = pyaudio.PyAudio()

    # Open stream
    audio_stream = pa.open(
        rate=handle.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=handle.frame_length)

    print("Listening for wake word...")

    try:
        while True:
            pcm = audio_stream.read(handle.frame_length)
            pcm = struct.unpack_from("h" * handle.frame_length, pcm)
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                # Call function to handle command after wake word detection
                handle_command()
    except KeyboardInterrupt:
        print("Stopping...")

    # Clean up
    audio_stream.close()
    handle.delete()


def open_application(application_name):
    try:
        if application_name.lower() == "calculator":
            subprocess.Popen("calc.exe")
            speak("Opening Calculator...")
            print("Opening Calculator...")
        elif application_name.lower() == "notepad":
            subprocess.Popen("notepad.exe")
            speak("Opening Notepad...")
            print("Opening Notepad...")
        elif application_name.lower() == "browser":
            # Specify the full path for Chrome
            subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            speak("Opening Browser...")
            print("Opening Browser...")
        elif application_name.lower() == "file explorer":
            subprocess.Popen("explorer.exe")
            speak("Opening File Explorer...")
            print("Opening File Explorer...")
        elif application_name.lower() == "command prompt":
            subprocess.Popen("cmd.exe")
            speak("Opening Command Prompt...")
            print("Opening Command Prompt...")
        elif application_name.lower() == "visual studio code":
            # Specify the full path for Visual Studio Code
            subprocess.Popen("C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\\code.cmd")
            speak("Opening Visual Studio Code...")
            print("Opening Visual Studio Code...")

        elif application_name.lower( )== "zoom":
            subprocess.Popen("C:\\Users\\User\\AppData\\Roaming\\Zoom\\Bin\\Zoom.exe")
            speak("opening Zoom...")
            print("Opening Zoom...")
        elif application_name.lower()=="shutdown": 
            subprocess.Popen("shutdown /s /t 1")
            speak("shutting down the computer")
            print("Shutting down the computer")
                   
        else:
            speak(f"Application '{application_name}' not supported.")
            print(f"Application '{application_name}' not supported.")
    except Exception as e:
        speak(f"Error opening {application_name}: {e}")
        print(f"Error opening {application_name}: {e}")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()





def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Adjust the timeout as needed
        except sr.WaitTimeoutError:
            print("Timeout occurred while listening for audio.")
            return
        
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        
        # Check if the command starts with "open"
        if command.startswith("open"):
            # Extract the application name by removing "open" and any leading/trailing spaces
            app_name = command[len("open"):].strip()
            open_application(app_name)
        else:
            print("Command does not start with 'open'.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your command.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def prompt_for_assistance():
    speak("Hi Tresor, how can I assist you today?")
    handle_input()  # Call handle_input() regardless of user input


def prompt_input_method():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Do you want to input text or speak?")
        print("1. Input text")
        print("2. Speak")
        print("Please say 'input text' or 'speak'.")
        try:
            audio = recognizer.listen(source, timeout=5)
            choice = recognizer.recognize_google(audio).lower()
            if "input text" in choice:
                return "text"
            elif "speak" in choice:
                return "speak"
            else:
                print("Invalid choice. Please say 'input text' or 'speak'.")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand you.")
            print("Sorry, I couldn't understand you.")
        except sr.RequestError:
            print("Failed to request results from Google Speech Recognition service.")

def handle_input():
    input_method = prompt_input_method()
    if input_method == "text":
        user_input = input("Enter your command: ")
        open_application(user_input)
    elif input_method == "speak":
        listen_for_command()




        
def handle_command():
    # Function to handle command after wake word detection
    # This function is called when the wake word is detected
    prompt_for_assistance()

@app.route('/api/wakeword', methods=['POST'])
def wakeword_endpoint():
    # Start a new thread to listen for the wake word
    threading.Thread(target=main).start()
    return jsonify({"message": "Listening for wake word..."}), 200        

if __name__ == "__main__":
    threading.Thread(target=main).start()
    app.run(debug=False)
    
