import speech_recognition as sr
import webbrowser
import pyttsx3  # Text to speech
import creds
import requests

podCast = {
    "youth and suicide" : "https://www.youtube.com/watch?v=5CMK_OicDKQ&list=PLxae24ZRVSi_ohb4WJeCfYDOSzdGAIVer&index=74",
    "life story of fakhar zaman" : "https://www.youtube.com/watch?v=MPnBm8_40Gw&list=PLxae24ZRVSi_ohb4WJeCfYDOSzdGAIVer&index=75",
    "hope and faith" : "https://www.youtube.com/watch?v=AXKjjfxNhJk&list=PLxae24ZRVSi_ohb4WJeCfYDOSzdGAIVer&index=47",
    "story" : "https://www.youtube.com/watch?v=CqdnYwPKezY&list=PLxae24ZRVSi_ohb4WJeCfYDOSzdGAIVer&index=1"
}

recognizer = sr.Recognizer()    # Speech recognition functionality deti hai
engine = pyttsx3.init()     # Text to speech functionality

def processCommand(c):
    if ( "open google" in c.lower() ):
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif ( "open youtube" in c.lower() ):
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif ( "open facebook" in c.lower() ):
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif ( "open linkedIn" in c.lower() ):
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif ( c.lower().startswith("play") ):
        podcast_name = c[5:].strip().lower()      # this fn will extract everything after the word "play "
        if ( podcast_name in podCast ):
            speak(f"Playing {podcast_name}")
            link = podCast[podcast_name]
            webbrowser.open(link)
        else:
            print(f"Sorry! I couldn't find a podcast named {podcast_name}")
            speak(f"Sorry! I couldn't find a podcast named {podcast_name}")
    elif ( "news" in c.lower() ):
        response = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news,cnn&apiKey={creds.newsapi}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles',[])
            if not articles:
                speak("No articles found in the response")
            else:
                # print(f"Found {len(articles)} articles")

                a=0
                for article in articles:
                    print(article['title'])
                    speak(article['title'])
                    a += 1
                    if(a>=5):
                        with sr.Microphone() as source:
                            speak("do you want to continue?")
                            print("do you want to continue?...")
                            audio = r.listen(source)
                            command = r.recognize_google(audio)
                        if( "continue" in command.lower() ):
                            a=0
                        elif ( "no" in command.lower() ):
                            speak("Okay.. Understood!")
                            break

        else:
            print(f"No news","Status Code: {response.status_code}")

def speak(text):
    engine.say(text)
    engine.runAndWait()

if(__name__=="__main__"):
    speak("Initializing darwin")
    while True:
        # Listen for the wake word "darwin"
        # Obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing")
        try:
            with sr.Microphone() as source:
                print("Listening..")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            print(word)
            if( "darwin" in word.lower() ):
                speak("Yeah!")
                with sr.Microphone() as source:
                    print("darwin Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)

            elif ("exit" in word.lower()):
                speak("Goodbye!")
                break
        except Exception as e:
            print("Error: {0}".format(e))
            continue