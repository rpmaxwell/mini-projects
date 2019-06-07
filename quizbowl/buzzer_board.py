import RPi.GPIO as io
from socketIO_client import SocketIO, BaseNamespace
import threading
import time


players = {
    1: {'player_name': 'Euclid', 'player_id': 1, 'pin_id': 26},
    2: {'player_name': 'Euclid', 'player_id': 1, 'pin_id': 19}
}


def on_connect(*args):
    print('connected', args)

def buzzer_callback(*args):
    io.output(LIGHT_PIN, io.HIGH)
    time.sleep(1)
    io.output(LIGHT_PIN, io.LOW)
    print('buzz sent!', args)

def on_buzz(*args):
    print('buzz sent!', args)
    

def send_buzz(player_record):
    global quizbowl_namespace
    quizbowl_namespace.emit('buzz_request', player_record, on_buzz)
    return 1

def buzzer_process(player_record, run_event):
    buzzer_pin = player_record['pin_id']
    while run_event.is_set():
        button_state = io.input(buzzer_pin)
        if button_state == False:
            print('button pressed')
            send_buzz(player_record)


def test():
    while True:
        for player in players.keys():
            buzzer_pin = players[player]['pin_id']
            button_state = io.inupt(buzzer_pin)
            if button_state == False:
                print('button pressed')
                send_buzz(players[player])

if __name__ == '__main__':
    BUTTON_PIN = 26
    LIGHT_PIN = 13
    with SocketIO('maxwell.casa', 80) as socketIO:
        print('connecting...')
        quizbowl_namespace = socketIO.define(BaseNamespace, '/device_reading')
        print('connected to local server')
        quizbowl_namespace.on('my_response', on_connect)
    io.setmode(io.BCM)
    for player in players.keys():
        io.setup(players[player]['pin_id'], io.IN, pull_up_down=io.PUD_UP)
        print('player {} set up!'.format(player))
    run_event = threading.Event()
    thread1 = threading.Thread(target=buzzer_process, args=(players[1], run_event))
    thread1.start()
    time.sleep(.5)
    thread2 = threading.Thread(target=buzzer_process, args=(players[2], run_event))
    thread2.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('closing threads... ')
        run_event.clear()
        thread1.join()
        thread2.join()
        print('threads closed')

    # buzzer_process(quizbowl_namespace)
