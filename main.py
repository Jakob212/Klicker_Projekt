import tkinter as tk

def start_recording():

    pass

def stop_recording():

    pass

def play_events():

    pass

app = tk.Tk()
app.title("Ereignisaufzeichner")

start_button = tk.Button(app, text="Start Aufnahme", command=start_recording)
start_button.pack()

stop_button = tk.Button(app, text="Stop Aufnahme", command=stop_recording)
stop_button.pack()

play_button = tk.Button(app, text="Ereignisse abspielen", command=play_events)
play_button.pack()

app.mainloop()
