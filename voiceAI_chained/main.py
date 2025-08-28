import speech_recognition as sr
from graph import graph
from dotenv import load_dotenv
load_dotenv()

def main():

    r = sr.Recognizer()  # Speech to Text

    with sr.Microphone() as source:    # Mic Access
        r.adjust_for_ambient_noise(source)   # Ambient Noise Adjustment

        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")
        stt = r.recognize_google(audio)
        print(f"You said: {stt}")

        for event in graph.stream({"messages": [{"role": "user", "content": stt}]}):
            if "messages" in event:
                event["messages"][-1].pretty_print()

main()