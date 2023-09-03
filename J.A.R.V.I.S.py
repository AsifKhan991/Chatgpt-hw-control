import pickle
import sys
import os
import openai
import speech_recognition as sr
import pyttsx3
import serial

COM='COM3'
baud=115200

try:
    arduino = serial.Serial(COM, baud)
    print(' Hardware port found! ')
except serial.serialutil.SerialException:
    print(' Hardware port not found! ')
    port=0
     
openai.api_key = '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'
messages = []
r = sr.Recognizer()
engine = pyttsx3.init()

with open('history.pkl','rb') as f:
    messages=pickle.load(f)
    f.close()

def delete_last(n):
    global messages
    for i in range(n):
        messages.pop()

def print_history():
    for i in messages:
        print(i['role']+':'+i["content"])

def SpeakText(command):
    if command:
        engine.say(command)
        engine.runAndWait()
    
def command_processing(text):
    print(f"JARVIS: [Processing..]")
    if 'hw' in text:
        Hardware_call(text[3:])
    elif 'end' in text:
        arduino.close()
        sys.exit()

def record_history(user,agent):
    global messagaes
    messages.append(user)
    messages.append(agent)
    with open('history.pkl','wb') as f:
        pickle.dump(messages, f)
        f.close()
        
def gpt(message):
    if message:
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages+[{"role": "user", "content": message}])
        reply = chat.choices[0].message.content
        #record_history({"role": "user", "content": message},{"role": "assistant", "content": reply}) #if you wanna save present chat
        if '@' in reply:
            indx=reply.rfind('@')
            command_processing(reply[indx+1:])
            if indx!=0:
                print(f"JARVIS: {reply[:indx]}")
            return reply[:indx]
        else:
            print(f"JARVIS: {reply}")
            return reply
    
def Hardware_call(hw_data):
    hw_data=hw_data+';\n'
    #print(hw_data)
    arduino.write(hw_data.encode())
    if'rtemp' in hw_data:
        temp_val = str(arduino.read(2).decode('utf-8'))
        SpeakText(gpt('$hw-rtemp-'+temp_val))
        
def Speech_rec():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=1)
            print('Listening....')
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            message = MyText.lower()
            print(f"User: {message}")
            return message
    except sr.UnknownValueError:
        print("[Noisy area!]")

#print_history()        
while True:
    message = Speech_rec(); # for audio input
    #message=input('User:') # for text input
    SpeakText(gpt(message))
    
    
