import socket

#  IP and port for the iMotions UDP connection
IP="127.0.0.1" # always 127.0.0.1 for local connection
UDP_PORT=8089
TCP_PORT=8087

# Function to send the event to iMotions(speed)
def sendudp(string_for_iMotions): 
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto(bytes(string_for_iMotions,"utf-8"),(IP,UDP_PORT))

# Function to send remote control commands to iMotions(reliability)
def sendtcp(string_for_iMotions):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((IP,TCP_PORT))
    sock.send(bytes(string_for_iMotions,"utf-8"))
    sock.close()


# Function to send score
def send_score_update(score):
    message = f"M;1;0;0;ScoreUpdate;{score}\r\n"
    sendudp(message)
    print(f"Sent to iMotions: {message}")

#Function to send level update
def send_level_update(level):
    message = f"M;1;0;0;LevelUpdate;{level}\r\n"
    sendudp(message)
    print(f"Sent to iMotions: {message}")

# Function to send a line clear event
def send_line_clear():
    message = "M;1;0;0;LineClear;Player cleared a line\r\n"
    sendudp(message)
    print(f"Sent to iMotions: {message}")

def send_event_marker(label, description=""):
    message = f"M;1;0;0;{label};{description}\r\n"
    sendudp(message)
    print(f"Custom marker sent: {message}")

# Function to mark the start of a scene (e.g., a game phase)
def send_scene_start(label):
    message = f"M;2;;;{label};Start of {label};S;I\r\n"
    sendudp(message)
    print(f"Scene START sent: {message}")

# Function to mark the end of a scene
def send_scene_end(label):
    message = f"M;2;;;{label};End of {label};E;I\r\n"
    sendudp(message)
    print(f"Scene END sent: {message}")

def send_line_clear_summary(total_lines):
    message = f"M;1;0;0;LineClears;{total_lines}\r\n"
    sendudp(message)
    print(f"Sent to iMotions: {message}")


