import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from your .env file")

client = genai.Client(api_key=API_KEY)

from pathlib import Path

# Create speeches folder
SPEECHES_DIR = Path(__file__).parent / "speeches"
SPEECHES_DIR.mkdir(exist_ok=True)


def get_next_speech_number():
    """Find the next available speech number."""
    existing_files = list(SPEECHES_DIR.glob("speech_*.wav"))

    if not existing_files:
        return 1

    numbers = []

    for file in existing_files:
        try:
            number = int(file.stem.split("_")[1])
            numbers.append(number)
        except (IndexError, ValueError):
            pass

    return max(numbers, default=0) + 1


def text_to_speech(text):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash-tts",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ],
            config={
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "voice": "Kore"
                    }
                }
            }
        )

        audio_data = (
            response.candidates[0]
            .content.parts[0]
            .inline_data.data
        )

        # Get next number
        number = get_next_speech_number()

        # Create filenames
        audio_file = SPEECHES_DIR / f"speech_{number:03d}.wav"
        text_file = SPEECHES_DIR / f"speech_{number:03d}.txt"

        # Save audio
        audio_file.write_bytes(audio_data)

        # Save original text
        text_file.write_text(text, encoding="utf-8")

        print("\nSpeech generated successfully!")
        print(f"Text : {text_file}")
        print(f"Audio: {audio_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    text = input("\nEnter text (or type 'exit' to quit): ").strip()

    if text.lower() == "exit":
        print("Goodbye!")
        break

    if not text:
        print("Please enter some text.")
        continue

    text_to_speech(text)