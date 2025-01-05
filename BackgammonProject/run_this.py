import subprocess
import time

server_process = subprocess.Popen(['python', 'server.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(2)

client1_process = subprocess.Popen(['python', 'client.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
client2_process = subprocess.Popen(['python', 'client.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

client1_process.wait()
client2_process.wait()

server_process.terminate()
