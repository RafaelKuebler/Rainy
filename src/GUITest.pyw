#!/usr/bin/env python

import os
import ttk
import threading
from Tkinter import *

from tts.tts import TTSConverter
from owm.owmfetcher import OWMFetcher
from evaluator.evaluator import OWMInterpreter


owm_fetcher = None
owm_interpreter = None
tts_converter = None
last_weather = None
last_evaluation = None


def init():
    global owm_fetcher
    global owm_interpreter
    global tts_converter

    relative_path_to_key = "../OWM.txt"
    relative_path_to_audio = "../audio/"
    current_dir = os.path.dirname(__file__)
    audio_path = os.path.join(current_dir, relative_path_to_audio)
    key_path = os.path.join(current_dir, relative_path_to_key)

    tts_converter = TTSConverter(audio_path)
    owm_fetcher = OWMFetcher(key_path)

    owm_interpreter = OWMInterpreter(None)


def write_line_in_debug(text):
    log.config(state=NORMAL)
    log.insert(END, str(text) + '\n')
    log.config(state=DISABLED)
    log.see(END)


def print_weather_data(observation):
    weather_string = owm_interpreter.string_weather_data(observation)
    write_line_in_debug(weather_string)


def read_last_evaluation():
    if last_evaluation:
        to_say = "Recommended: {}".format(last_evaluation)
        write_line_in_debug("Reading last evaluation...")
        threading.Thread(target=tts_converter.say, args=[to_say]).start()
    else:
        write_line_in_debug("No weather data: leave first!")


def clear_log():
    log.config(state=NORMAL)
    log.delete('1.0', END)
    log.config(state=DISABLED)


'''-----------------Event functions-----------------'''
def perform_weather_check():
    global owm_fetcher
    global owm_interpreter
    global tts_converter
    global last_weather
    global last_evaluation

    write_line_in_debug("Fetching weather data...")
    last_weather = owm_fetcher.get_current_weather()
    print_weather_data(last_weather)

    to_say = "The weather status right now is: {}".format(last_weather.get_detailed_status())
    threading.Thread(target=tts_converter.say, args=[to_say]).start()

    last_evaluation = owm_interpreter.interpret_weather(last_weather)
    write_line_in_debug(last_evaluation)


'''-----------------Main window-----------------'''
root = Tk()
root.title("Rainy")
root.wm_iconbitmap("../resources/umbrella.ico")
root.resizable(width=False, height=False)

image = PhotoImage(file="../resources/rain.gif")


'''-----------------Frames-----------------'''
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

left_frame = ttk.Frame(mainframe, width=image.width(), height=image.height())
left_frame.grid_propagate(False)
left_frame.grid(column=0, row=0, sticky=(N, W, E, S))
left_frame.columnconfigure(0, weight=1)
left_frame.rowconfigure(0, weight=1)

center_frame = ttk.Frame(mainframe, width=700, height=image.height())
center_frame.grid_propagate(False)
center_frame.grid(column=1, row=0, sticky=(N, W, E, S))
center_frame.columnconfigure(0, weight=1)
center_frame.rowconfigure(0, weight=1)

right_frame = ttk.Frame(mainframe, height=image.height())
right_frame.grid(column=2, row=0, sticky=(N, W, E, S), padx=10, pady=20)
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(7, weight=1)


'''-----------------Widgets-----------------'''
'''Image'''
ttk.Label(left_frame, image=image).grid(column=0, row=0, sticky=(N, W, E, S))


'''Debug window'''
scrollbar = Scrollbar(center_frame)
scrollbar.grid(column=1, row=0, sticky=(N, W, E, S))
log = Text(center_frame, yscrollcommand=scrollbar.set)
log.grid(column=0, row=0, sticky=(N, W, E, S))
log.config(state=DISABLED)
scrollbar.config(command=log.yview)


'''Form'''
location = StringVar()
location.set("Karlsruhe")
time = StringVar()
time.set("now")
ttk.Label(right_frame, text="Location").grid(column=0, row=0, sticky=W)
ttk.Entry(right_frame, textvariable=location).grid(column=0, row=1, sticky=W)
ttk.Label(right_frame, text="Time").grid(column=0, row=2, sticky=W)
ttk.Entry(right_frame, textvariable=time).grid(column=0, row=3, sticky=W)

ttk.Button(right_frame, text="Leave house", command=perform_weather_check).grid(column=0, row=4)
ttk.Button(right_frame, text="Read evaluation", command=read_last_evaluation).grid(column=0, row=5)
ttk.Button(right_frame, text="Clear log", command=clear_log).grid(column=0, row=6)


'''-----------------Events-----------------'''
root.after(0, perform_weather_check)
root.after(6000, read_last_evaluation)
hours = 3
root.after(1000*60*60*hours, perform_weather_check)


'''-----------------Start-----------------'''
init()

root.mainloop()
