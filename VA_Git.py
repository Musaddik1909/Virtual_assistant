import pyttsx3 #pip install pyttsx3 == text data into speech using python
import datetime
import speech_recognition as sr #pip install SpeechRecognition for speech recognition from microphone
import smtplib #send email
import pyautogui
import webbrowser as wb
import wikipedia 
import pywhatkit
import requests
from time import sleep
from Secrets import senderemail, epwd, to
from email.message import EmailMessage

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getvoices(voice):
    voices = engine.getProperty('voices')
    #print(voices[1].id)
    if voice==1:
        engine.setProperty('voice',voices[0].id)
        speak("hello this is jarvis")  

    if voice==2:
        engine.setProperty('voice',voices[1].id)
        speak("hello this is Friday")  

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S") #hour=I,min=M,secs=S
    speak("The current time is:")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("The date is:")
    speak(date)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome back sir!")
    #time()
    #date()
    #greeting()
    speak("Jarvis at your service, what can I do for you?")

#while True: 
 #  voice =int(input("Press 1 for Male voice \n Press 2 for female voice\n"))
#   speak(audio) 
  # getvoices(voice)
def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon Sir!")
    elif hour >= 18 and hour < 24: 
        speak("Good evening Sir!")
    else :
        speak("Good night Sir!")

#wishme()
def takeCommandCMD():
    query = input("Please tell me how can I help you?\n")
    return query

def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try: 
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
    except Exception as e:
        print(e)
        speak("Say that again Please...")
        return "None"
    return query

def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() #ttls is used for securly sending mails
    server.login(senderemail, epwd)
    email = EmailMessage()
    email['From'] = senderemail
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def sendwhatsmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('Enter')

def searchgoogle():
    speak('What should I search for?')
    search = takeCommandMic()
    wb.open('https://www.google.com/search?q='+search)

#http://api.openweathermap.org/data/2.5/weather?q={Chennai}&units=imperial&appid={f74fee1ac2d7b68fdbf01d4523ead733}    

if __name__== "__main__":
    getvoices(1)
    wishme()
    while True:
        query = takeCommandMic().lower()
        
        if 'time' in query: 
            time()

        elif 'date' in query:
            date()

        elif 'email' in query:
            email_list = {
                'test email':'abc@example.com'
                #test email' : 'id of gmail through which you want to send email'
            }
            try: 
                speak("To whom you want to send the mail?")
                name = takeCommandMic()
                receiver = email_list[name]
                speak("What is the Subject of the mail?")
                subject = takeCommandMic()
                speak('What should I say?')
                content = takeCommandMic()
                sendEmail(receiver, subject, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Unable to send email")
        
        elif 'message' in query:
            user_name = {
                'Jarvis': 'XXXXXXXXXX'
            }
            try: 
                speak("To whom you want to send the whats app message?")
                name = takeCommandMic()
                phone_no = user_name[name]
                speak("What is the message?")
                message = takeCommandMic()
                sendwhatsmsg(phone_no, message)
                speak("Message has been sent")
            except Exception as e:
                print(e)
                speak("Unable to send the message")

        elif 'wikipedia' in query:
            speak('Searching on wikipedia...')
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            print(result)
            speak(result)

        

        elif 'search' in query:
            searchgoogle()

        elif 'youtube' in query:
            speak("what should I search for on youtube")
            topic = takeCommandMic()
            pywhatkit.playonyt(topic)

        elif 'weather' in query:
            city = 'chennai'
            url = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={f74fee1ac2d7b68fdbf01d4523ead733}'
        
            res = requests.get(url)
            data = res.json()

            weather = data['weather'] [0] ['main']
            temp = data['main']['temp']
            desp = data['weather'] [0] ['description']
            temp = round((temp-32) * 5/9)
            print(weather)
            print(temp)
            print(desp)
            speak('Temperature : {} degree celcius'.format(temp))
            speak('Weather is {}'.format(desp))

        elif 'offline' in query:
            quit()

        elif 'stop jarvis' in query:
            quit() 