from speech_recog import Listener
import time

l = Listener()
l.set_on_hear(lambda a: print(a))

l.start_listening()
print('Listening started! Play something!')
l.listen()
l.stop_listening()