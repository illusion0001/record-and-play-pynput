from pynput import mouse
from pynput import keyboard
import time
import json
import sys

# Global variable
storage: list = []

def on_press(key):
    try:
        json_object = {'action':'pressed_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        if key == keyboard.Key.esc:
            return False
        json_object = {'action':'pressed_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)

def on_release(key):
    try:
        json_object = {'action':'released_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        json_object = {'action':'released_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)

def on_move(x, y):
    if len(storage) >= 1:
        if storage[-1]['action'] != "moved":
            json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
            storage.append(json_object)
        elif storage[-1]['action'] == "moved" and time.time() - storage[-1]['_time'] > 0.02:
            json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
            storage.append(json_object)

def on_click(x, y, button, pressed):
    json_object = {'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':time.time()}
    storage.append(json_object)

def on_scroll(x, y, dx, dy):
    json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x':x, 'y':y, '_time': time.time()}
    storage.append(json_object)

def main():

    if len(sys.argv) == 2:
        name_of_recording = str(sys.argv[1])
    else:
        exit("Please supply recording name")

    print("Press 'esc' to end recording.")

    # Collect events until exit key is pressed (handled in on_press)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
        with mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as mouse_listener:
            keyboard_listener.join()  # pause script until keyboard listener exits

    # Dump storage into outfile
    with open('data/{}.json'.format(name_of_recording), 'w') as outfile:
        json.dump(storage, outfile, indent=4)
    print('Input recording stopped and saved.')

if __name__ == "__main__":
    main()
