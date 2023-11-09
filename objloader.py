import speech_recognition as sr

def recognize_single_word():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    while True:
        # Open the microphone and capture audio
        with sr.Microphone() as source:
            print("Please speak a single word, or say 'exit' to quit:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Recognize the speech using Google Web Speech API
            word = recognizer.recognize_google(audio)
            print("Recognized Word:", word)

            if word.lower() == 'exit':
                print("Exiting the program.")
                break
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

if __name__ == "__main__":
    recognize_single_word()
