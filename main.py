from socket import *
import threading
import time
import pickle
from queue import Queue

peeps = {}
helpmsg = """
/sync                       - Sync the identity data (happens on login)
/save                       - Saves the identity file
/load                       - Loads the identity file
/exit                       - Quits, and sends a signoff message"""

UDP_IP = "<broadcast>"  # This is the broadcast IP
UDP_PORT = 6969  # Haha funny number

# Hacky ip solution, wont
s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]

send = socket(AF_INET, SOCK_DGRAM)
send.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
send.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Enable UDP broadcasting

# This is the naming ping
name = input("Nickname: ")
name_pack = ("~~setname~~||" + name.strip('|') + '||' + local_ip).encode('utf-8')
send.sendto(name_pack, ('<broadcast>', 6969))

# Call for a node sync
send.sendto('~~sync~~'.encode('utf8'), ('<broadcast>', 6969))

sock = socket(AF_INET,
              SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))


class listen(threading.Thread):
    """The listner thread"""

    def run(self):
        global peeps

        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            data = data.decode('utf8')  # decode data into string

            latestaddr = str(addr[0])  # grab the latestaddr

            if data.startswith('~~setname~~'):
                # If we have a new person, then add the data stuff.
                peeps[data.split('||')[2]] = data.split('||')[1]
                continue
                
            if data.startswith('~~sync~~'):
                # This syncs up everyones data
                for peep in peeps.keys():
                    name_pack = ("~~setname~~||" + peeps[peep] + '||' + peep).encode('utf-8')
                    send.sendto(name_pack, ('<broadcast>', 6969))

            if latestaddr in peeps.keys():
                # this'll lookup the uname
                print(peeps[latestaddr] + ": " + str(data))

            else:
                # Shouldn't happen, but it's good to catch edge cases
                print(str(addr[0]) + ": " + str(data))


class speak(threading.Thread):
    """The speaker thread"""

    def run(self):
        global peeps

        while True:
            # The message to send
            msg = input("> ")

            if msg.startswith("/save"):
                # Save the iden data
                with open('peeps.chat', 'wb') as f:
                    pickle.dump(peeps, f)
                    time.sleep(0.2)
                continue

            elif msg.startswith("/load"):
                # Load the iden data
                with open('peeps.chat', 'rb') as f:
                    peeps = pickle.load(f)
                    time.sleep(0.2)
                continue

            elif msg.startswith("/help") or msg.startswith("/?"):
                print(helpmsg)
                time.sleep(0.2)
                continue

            elif msg.startswith("/peeps"):
                # printout peeps for debugging, that's why its not in the docs
                print(peeps)
                time.sleep(0.2)
                continue

            elif msg.startswith("/exit"):
                exit(69) # Why not

            msg = msg.encode() # ByTe LiKe StRiNg ExpEcTeD, NoT sTr
            send.sendto(msg, ('<broadcast>', 6969))
            time.sleep(0.2)


if __name__ == '__main__':
    lst = listen()
    lst.daemon = True
    lst.start()
    print("Listening ....")

    snd = speak()
    snd.start()
