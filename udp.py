import socket
import threading
import time

# UDP socket settings
IP = "127.0.0.1"  #Localhost broadcast
BROADCAST_PORT = 7500  #Port for broadcasting
RECEIVE_PORT = 7501  #Port where receiver listens

def udp_receiver():
    """Function to receive UDP messages on port 7501."""
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_socket.bind((IP, RECEIVE_PORT))
    
    print(f"Receiver listening on {IP}:{RECEIVE_PORT}...")

    while True:
        data, addr = recv_socket.recvfrom(1024)  #Buffer size= 1024 bytes
        message = data.decode()
        print(f"Received message: {message} from {addr}")

def udp_sender(equipment_id):
    """Function to send UDP messages to 7500 (broadcast)."""
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = str(equipment_id)
    send_socket.sendto(message.encode(), (IP, BROADCAST_PORT))
    print(f"Broadcasted equipment ID: {message}")

def udp_forwarder():
    """Function to forward messages from 7500 to 7501."""
    forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    forward_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    forward_socket.bind((IP, BROADCAST_PORT))

    print(f"Forwarder listening on {IP}:{BROADCAST_PORT} and forwarding to {IP}:{RECEIVE_PORT}...")

    while True:
        data, addr = forward_socket.recvfrom(1024)
        print(f"Forwarder received: {data.decode()} from {addr}, forwarding to {IP}:{RECEIVE_PORT}")
        
        # Forward to receiver
        forward_socket.sendto(data, (IP, RECEIVE_PORT))

def start_services():
    """Start receiver and forwarder in separate threads."""
    threading.Thread(target=udp_receiver, daemon=True).start()
    threading.Thread(target=udp_forwarder, daemon=True).start()
    print("Receiver and Forwarder started.")



if __name__ == "__main__":
    start_services()

    # Wait for messages to be processed before script exits
    time.sleep(200)
