from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import openai
import datetime


root = Tk()
root.geometry("700x380")
root.resizable(width=False, height=False)
root.title("My ChatBot")
root.config(bg="#0B2447")


openai.api_key = "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"


# get Answers
def get_answer(que):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=que,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    answer = response["choices"][0]["text"].strip()

    formatted_date = datetime.datetime.now().strftime("%d:%m:%y-%H:%M:%S")
    with open("history.txt", 'a') as history_file:
        s = f"************************************\nTime: {formatted_date}\nUser:\n{que}MyChatBot:\n{answer}\n\n\n"
        history_file.write(s)

    return answer


# define a function to convert text to speech
def convert_text_to_speech(text):
    # create a new instance of the pyttsx3 engine
    engine = pyttsx3.init()

    # set the voice property
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty("rate", 185)

    # say the text
    engine.say(text)
    engine.runAndWait()


# Mike
def takeCommand():
    # create a new instance of the recognizer
    r = sr.Recognizer()

    # use the Microphone class to listen for audio input from the default microphone
    with sr.Microphone() as source:
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        r.pause_threshold = 1

        convert_text_to_speech("Listening")

        # record audio input from the microphone
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="en-in")
        user_text.delete(1.0, "end")
        user_text.insert(1.0, command)

        # calling get_answer function for particular command
        bot_answer = get_answer(command)
        bot_text.delete(1.0, "end")
        bot_text.insert(1.0, bot_answer)
        convert_text_to_speech(bot_answer)

    except EXCEPTION as e:
        user_text.insert(1.0, "")
        convert_text_to_speech("May you repeat it again")
        return e


# clear function
def clear(t):
    t.delete(1.0, "end")


# ask function
def ask():
    que = user_text.get(1.0, "end")
    ans = get_answer(que)
    bot_text.delete(1.0, "end")
    bot_text.insert(1.0, ans)


# Heading Frame
f = Frame(root, bd=5, bg="dark blue")
f.pack(side="top", fill="x")
Label(f, text="My ChatBot", font=("Times", 25, "bold"), bg="deep sky blue").pack(side="top", fill="x")

# Images
mike_img = ImageTk.PhotoImage(Image.open("mike_prev_ui.png"))
speaker_img = ImageTk.PhotoImage(Image.open("speaker_prev_ui.png"))

# Buttons
Button(image=speaker_img, bd=0, activebackground="deep sky blue", cursor="hand2", bg="#0B2447",
       command=lambda: convert_text_to_speech(user_text.get(1.0, "end"))).place(x=20, y=110)
Button(image=mike_img, bd=0, activebackground="deep sky blue", cursor="hand2", bg="#0B2447", command=takeCommand).place(
    x=255, y=110)
Button(image=speaker_img, bd=0, activebackground="deep sky blue", cursor="hand2", bg="#0B2447",
       command=lambda: convert_text_to_speech(bot_text.get(1.0, "end"))).place(x=430, y=110)

# Labels
Label(text="User", font=("Times", 23, "bold"), fg="#F7F1E5", bg="#0B2447").place(x=125, y=110)
Label(text="Bot", font=("Times", 23, "bold"), fg="#F7F1E5", bg="#0B2447").place(x=535, y=110)

# Provided Language Text
user_text = Text(font=("Times", 19), relief="ridge", bd=2, bg="ghost white", wrap="word", height=5, width=21, padx=3,
                 pady=5, undo=True)
user_text.place(x=20, y=160)

# Outcome Text
bot_text = Text(font=("Times", 19), relief="ridge", bd=2, bg="ghost white", wrap="word", height=5, width=20, padx=3,
                pady=5, undo=True)
bot_text.place(x=430, y=160)

# Translate Button
Button(text="  Ask  ", font=("Times", 14), bg="deep sky blue", activebackground="dodger blue", cursor="hand2",
       command=ask).place(
    x=325, y=225)

# Exit Button
Button(text="Exit", font=("Times", 12), bg="red", fg="white", activebackground="#F45050", cursor="hand2", command=quit,
       width=5).place(x=625, y=325)

# Clear Buttons
Button(text="Clear", font=("Times", 12), bg="lawn green", activebackground="gold", cursor="hand2",
       command=lambda: clear(user_text), width=5).place(x=20, y=325)
Button(text="Clear", font=("Times", 12), bg="lawn green", activebackground="gold", cursor="hand2",
       command=lambda: clear(bot_text), width=5).place(x=430, y=325)

root.mainloop()

