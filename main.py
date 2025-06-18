import pyaudio
import wave
import threading
import time
import numpy as np
import speech_recognition as sr
import matplotlib.pyplot as plt

def show_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
    plt.plot(time_axis, samples)
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

def transcribe_audio(data, rate, width, filename="transcription.txt"):
    r = sr.Recognizer()
    audio = sr.AudioData(data, rate, width)
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        text = "Could not understand the audio."
    except sr.RequestError as e:
        text = f"API Error: {e}"
    print("Transcription:", text)
    with open(filename, "w") as f:
        f.write(text)
    print(f"Saved: {filename}")

def save_audio(data, rate, width, filename="audio.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"Saved: {filename}")

def record_until_enter():
    p = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 1024
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
    frames = []

    stop_event = threading.Event()

    def wait_for_enter():
        input("Press Enter to stop recording...\n")
        stop_event.set()

    def spinner():
        spinner_chars = ['|', '/', '-', '\\']
        idx = 0
        while not stop_event.is_set():
            print(f"\rRecording... {spinner_chars[idx % len(spinner_chars)]}", end='')
            idx += 1
            time.sleep(0.1)
        print("\r", end='')

    threading.Thread(target=wait_for_enter).start()
    threading.Thread(target=spinner).start()

    while not stop_event.is_set():
        try:
            data = stream.read(frames_per_buffer)
            frames.append(data)
        except Exception as e:
            print("Error reading stream:", e)
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    sample_width = p.get_sample_size(format)
    audio_data = b''.join(frames)
    return audio_data, rate, sample_width

def main():
    print("Start speaking. Press Enter to stop.")
    audio_data, rate, width = record_until_enter()
    save_audio(audio_data, rate, width)
    show_waveform(audio_data, rate)
    transcribe_audio(audio_data, rate, width)

if __name__ == "__main__":
    main()
    