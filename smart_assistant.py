import os
import random
import speech_recognition
import pyttsx3
import datetime
import wikipedia
import webbrowser


sr = speech_recognition.Recognizer()
sr.pause_threshold = 1
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty('rate', 178)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices)


commands_dict = {
    'commands': {
        'greeting': ['hello', 'hi', 'hello Luke', 'good morning'],
        'create_task': ['add a task', 'create task', 'note'],
        'play_music': ['play music', 'play song', 'start party'],
        'search_wikipedia': ['wiki', 'wikipedia', 'find', 'search'],
        'open_youtube': ['open youtube'],
        'open_google': ['open google'],
        'goodbye': ['stop', 'goodbye', 'good night'],
        'time_now': ['what time is it', 'time']
    }
}


def speak(audio):
    # function for assistant to speak
    engine.say(audio)
    engine.runAndWait()


def listen_command():
    """The function will return the recognized command"""

    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='en-EN').lower()

        return query
    except speech_recognition.UnknownValueError:
        return speak("Sorry, I don't understand you.")


def greeting():
    """Greeting function"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning')

    elif hour > 12 and hour < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    return speak('I am Luke, your Artificial intelligence assistant. Please tell me how may I help you')


def create_task():
    """Create a todo task"""
    speak('What do we add to the to-do list?')

    query = listen_command()

    with open('todo-list.txt', 'a') as file:
        file.write(f' {query}\n')

    return speak(f'Task {query} add in todo-list!')


def play_music():
    """Play a random mp3 file"""

    files = os.listdir('music')
    random_file = f'music/{random.choice(files)}'
    os.system(f'xdg-open {random_file}')

    return speak(f'Dancing for {random_file.split("/")[-1]}')


def search_wikipedia():
    speak('Searching Wikipedia...')
    query = listen_command()
    results = wikipedia.summary(query, sentences=2)
    print(results)
    speak(results)


def open_youtube():
    speak('Open youtube...')
    result = webbrowser.open('youtube.com')
    return result


def open_google():
    speak('Open google...')
    result = webbrowser.open('google.com')
    return result


def goodbye():
    hour = int(datetime.datetime.now().hour)
    if hour >= 18:
        speak('Good Night')
    else:
        speak('Have a good day')

    return speak('If you need me just say hello. I will be here')


def time_now():
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(str_time)
    return speak(f"The time is {str_time}")


def main():
    query = listen_command()

    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())


if __name__ == '__main__':
    while True:
        main()