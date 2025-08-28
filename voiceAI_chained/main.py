import speech_recognition as sr

def main():

    r = sr.Recognizer()  # Speech to Text

    with sr.Microphone() as source:    # Mic Access
        r.adjust_for_ambient_noise(source)   # Ambient Noise Adjustment
        r.pause_threshold = 2

        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        stt = r.recognize_google(audio)
        print(f"You said: {stt}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")

if __name__ == "__main__":
    main()