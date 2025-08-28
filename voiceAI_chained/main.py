import speech_recognition as sr
from graph import graph
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv
import asyncio
load_dotenv()

openai = AsyncOpenAI()
messages = []

async def tts(text:str):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def main():

    r = sr.Recognizer()  # Speech to Text

    with sr.Microphone() as source:    # Mic Access
        r.adjust_for_ambient_noise(source)   # Ambient Noise Adjustment

        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")
        stt = r.recognize_google(audio)
        print(f"You said: {stt}")

        for event in graph.stream({"messages": [{"role": "user", "content": stt}]}, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()

# main()
asyncio.run(tts("Hello, how can I assist you today?")) 