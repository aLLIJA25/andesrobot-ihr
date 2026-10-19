

import queue, sys, sounddevice as sd
from vosk import Model, KaldiRecognizer
import time
import os 
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "../vosk-model-small-en-us-0.15")
model= Model(model_path)



q = queue.Queue()
def callback(indata, frames, time, status):
    if status: print(status, file=sys.stderr)
    q.put(bytes(indata))

samplerate = int(sd.query_devices(None, "input")["default_samplerate"])
rec = KaldiRecognizer(model, samplerate)

print("🎙️  Escuchando... (Ctrl+C para salir)\n")


limtiempo= 30
inicio= time.time() 

with sd.RawInputStream(samplerate=samplerate, blocksize=4000, dtype="int16", channels=1, callback=callback):
    while time.time()- inicio < limtiempo:
        data = q.get()
        if rec.AcceptWaveform(data):
            print(rec.Result())
print("tiempo terminado")
print(rec.FinalResult())

