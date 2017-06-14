import os
import ttk
import datetime
import threading
from Tkinter import *

from tts.tts import TTSConverter
from owm.owmfetcher import OWMFetcher


debug_current_line = 0

'''-----------------Event functions-----------------'''
def write_line_in_debug(text):
    global debug_current_line
    debug_output.insert(END, text + "\n")
    debug_current_line += 1
    debug_output.see(END)


def print_weather_data(observation):
    debug_output.config(state=NORMAL)
    write_line_in_debug("-------------------------------------------------------------")
    write_line_in_debug(" Weather query at {} returned:".format(datetime.datetime.now()))
    write_line_in_debug("   Last observation: {}".format(observation.get_reference_time(timeformat='iso')))
    write_line_in_debug("   Temperature: {}".format(observation.get_temperature(unit='celsius')))
    write_line_in_debug("   Cloud coverage: {}".format(observation.get_clouds()))
    write_line_in_debug("   Rain: {}".format(observation.get_rain()))
    write_line_in_debug("   Humidity: {}".format(observation.get_humidity()))
    write_line_in_debug("   Detailed status: {}".format(observation.get_detailed_status()))
    write_line_in_debug("-------------------------------------------------------------\n")
    debug_output.config(state=DISABLED)


def perform_weather_check():
    tts_converter = TTSConverter("../../audio/")

    relative_path_to_key = "../../OWM.txt"
    current_dir = os.path.dirname(__file__)
    key_path = os.path.join(current_dir, relative_path_to_key)

    owm_fetcher = OWMFetcher(key_path)
    weather = owm_fetcher.get_current_weather()
    print_weather_data(weather)

    threading.Thread(target=tts_converter.say, args=[weather.get_detailed_status()]).start()

    root.after(2000, perform_weather_check)

'''-----------------Main window-----------------'''
root = Tk()
root.title("Rainy")
root.wm_iconbitmap("umbrella.ico")
root.resizable(width=False, height=False)

'''-----------------Frames-----------------'''
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

left_frame = ttk.Frame(mainframe)
left_frame.grid(column=0, row=0, sticky=(N, W, E, S))

center_frame = ttk.Frame(mainframe)
center_frame.grid(column=1, row=0, sticky=(N, W, E, S))

right_frame = ttk.Frame(mainframe)
right_frame.grid(column=2, row=0, sticky=(N, W, E, S))

'''-----------------Widgets-----------------'''
'''Image'''
image = PhotoImage(file="rain.gif")
# ttk.Label(right_frame, image=image).grid(column=0, row=0, sticky=(N, W, E, S))
ttk.Label(left_frame, image=image).pack(expand=YES, fill=BOTH)

'''Debug window'''
scrollbar = Scrollbar(center_frame)
scrollbar.grid(column=1, row=0, sticky=(N, W, E, S))
# scrollbar.pack(side=RIGHT, fill=Y)
debug_output = Text(center_frame, yscrollcommand=scrollbar.set, width=100, height=15)
debug_output.grid(column=0, row=0, sticky=(N, W, E, S))
debug_output.config(state=DISABLED)
scrollbar.config(command=debug_output.yview)

'''Form'''
location = StringVar()
location.set("Karlsruhe")
time = StringVar()
time.set("now")
ttk.Label(right_frame, text="Location").grid(column=0, row=0, sticky=W)
ttk.Entry(right_frame, textvariable=location).grid(column=0, row=1, sticky=W)
ttk.Label(right_frame, text="Time").grid(column=0, row=2, sticky=W)
ttk.Entry(right_frame, textvariable=time).grid(column=0, row=3, sticky=W)

'''-----------------Events-----------------'''
hours = 3
root.after(1000*60*60*hours, perform_weather_check)

perform_weather_check()

''''Start!'''
root.mainloop()
