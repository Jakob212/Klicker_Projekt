import tkinter as tk
from tkinter import simpledialog, Toplevel, Listbox
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener, KeyCode
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
import json
import threading
import os
import time


keyboard_controller = KeyboardController()
mouse_controller = MouseController()

is_recording = False
events = []

def capture_event(event_type, event_data):
    global events
    timestamp = time.time()  
    events.append((timestamp, event_type, *event_data))

def on_press(key):
    global is_recording
    if key == Key.f10 and not is_recording:  # Starte die Aufnahme mit F10
        start_recording()
    elif key == Key.f11 and is_recording:  # Stoppe die Aufnahme mit F11
        stop_recording()
    elif key == Key.f12:  # Beende das Skript mit F12
        stop_recording() if is_recording else None
        print("Skript wird beendet...")
        os._exit(0)  # Sofortiger Ausstieg aus dem Skript

def on_click(x, y, button, pressed):
    if is_recording:
        button_str = repr(button)
        capture_event('mouse_click', [x, y, button_str, pressed])

def start_recording():
    global is_recording, events
    is_recording = True
    events.clear()
    print("Aufnahme gestartet. Drücken Sie F11, um zu stoppen.")

def stop_recording():
    global is_recording
    is_recording = False
    filename = simpledialog.askstring("Datei speichern", "Geben Sie einen Dateinamen ein:")
    if filename:
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(events, f)
        print(f"Aufnahme gestoppt und gespeichert unter: {filename}")
    else:
        print("Speichern abgebrochen.")
    events.clear()

def replay_events(filename):
    print(f"Skript {filename} wird abgespielt...")
    with open(filename, 'r') as f:
        events = json.load(f)
    last_time = 0
    for event in events:
        timestamp, etype, *args = event
        time.sleep(timestamp - last_time)  # Verzögerung einfügen
        last_time = timestamp
        if etype == 'key_press':
            key_str = args[0]
            key = eval(key_str)
            keyboard_controller.press(key)
            keyboard_controller.release(key)
        elif etype == 'mouse_click':
            x, y, button_str, pressed = args
            button = eval(button_str)
            mouse_controller.position = (x, y)
            if pressed:
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)
    print("Skriptwiedergabe abgeschlossen.")

def show_files():
    top = Toplevel()
    top.title("Wählen Sie eine Datei zum Abspielen")
    listbox = Listbox(top)
    listbox.pack(fill=tk.BOTH, expand=True)
    files = [f for f in os.listdir('.') if f.endswith('.json')]
    for file in files:
        listbox.insert(tk.END, file)
    def on_select(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        filename = w.get(index)
        replay_events(filename)
        top.destroy()
    listbox.bind('<<ListboxSelect>>', on_select)

app = tk.Tk()
app.title("Ereignisaufzeichner")

start_button = tk.Button(app, text="Start Aufnahme (F10)", command=lambda: on_press(Key.f10))
start_button.pack()

stop_button = tk.Button(app, text="Stop Aufnahme (F11)", command=lambda: on_press(Key.f11))
stop_button.pack()

replay_button = tk.Button(app, text="Ereignisse abspielen", command=show_files)
replay_button.pack()

threading.Thread(target=lambda: KeyboardListener(on_press=on_press).join(), daemon=True).start()

app.mainloop()
