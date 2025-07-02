import speech_recognition as sr
from googletrans import Translator

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🔊 Please speak now in English...")
        audio = recognizer.listen(source)
    try:
        print("🎙️ Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
        return ""

def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        print(f"📝 Translated ({target_language}): {translation.text}")
        return translation.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text

def display_language_options():
    print("🌎 Available translation languages:")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")

def get_user_choice():
    choice = input("Please select the target language number (1-8): ")
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"
    }
    return language_dict.get(choice, "es")

def speak(text, language='en'):

    print(f"Speaking in {language}: {text}")

def main():
    display_language_options()
    target_language = get_user_choice()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, target_language=target_language)
        speak(translated_text, language='en')

if __name__ == "__main__":
    main()

