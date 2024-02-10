import tkinter as tk
from pynput import keyboard, mouse
import json
import threading

# Globale Variable, um den Aufzeichnungsstatus zu speichern
is_recording = False
events = []

# Funktion zum Erfassen von Tastatur- und Mausereignissen
def capture_events():
    with keyboard.Listener(on_press=on_press) as k_listener, \
         mouse.Listener(on_click=on_click) as m_listener:
        k_listener.join()
        m_listener.join()

# Callback-Funktionen für Tastatur und Maus
def on_press(key):
    if is_recording:
        try:
            events.append(('key_press', key.char))
        except AttributeError:
            events.append(('key_press', str(key)))

def on_click(x, y, button, pressed):
    if is_recording:
        events.append(('mouse_click', x, y, str(button), pressed))

# Funktionen für die GUI-Schaltflächen
def start_recording():
    global is_recording
    is_recording = True
    # Starten der Ereigniserfassung in einem separaten Thread
    threading.Thread(target=capture_events, daemon=True).start()

def stop_recording():
    global is_recording
    is_recording = False
    # Speichern der Ereignisse in einer Datei
    with open('events.json', 'w') as f:
        json.dump(events, f)
    print("Aufnahme gestoppt und gespeichert.")

def play_events():
    print("Ereignisse abspielen - Diese Funktion muss noch implementiert werden.")

# GUI-Setup
app = tk.Tk()
app.title("Ereignisaufzeichner")

start_button = tk.Button(app, text="Start Aufnahme", command=start_recording)
start_button.pack()

stop_button = tk.Button(app, text="Stop Aufnahme", command=stop_recording)
stop_button.pack()

play_button = tk.Button(app, text="Ereignisse abspielen", command=play_events)
play_button.pack()

app.mainloop()
