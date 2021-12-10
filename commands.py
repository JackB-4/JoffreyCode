import threading, queue
def actionSay(lock):
  print("To be added.")


def actionHelp(lock):
  print("-help \n-say")


def console(q, lock):
    while 1:
        input()   # After pressing Enter you'll be in "input mode"
        with lock:
            cmd = input('> ')

        q.put(cmd)
        if cmd == 'quit':
            break

def invalid_input(lock):
    with lock:
        print('--> Unknown command')

def consoleControl():
    cmd_actions = {'help': actionHelp, 'say': actionSay}
    cmd_queue = queue.Queue()
    stdout_lock = threading.Lock()

    dj = threading.Thread(target=console, args=(cmd_queue, stdout_lock))
    dj.start()

    while 1:
        cmd = cmd_queue.get()
        if cmd == 'quit':
            break
        action = cmd_actions.get(cmd, invalid_input)
        action(stdout_lock)