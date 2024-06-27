import socket
import threading
import time

# Function to send UDP packets
def send_udp_packets(destination, packet_size=1472, interval=0):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Prepare packet data with specified size
        data = b'X' * packet_size

        # Send UDP packets
        while True:
            sock.sendto(data, (destination, 12345))  # Using port 12345 as an example
            if interval:
                time.sleep(interval)

# Main function
if __name__ == "__main__":
    destination = "8.8.8.8"
    packet_size = 1472  # Adjust packet_size as needed
    interval = 0  # Adjust interval as needed
    num_threads = 16  # Adjust number of threads as needed

    # Create and start separate threads to send UDP packets concurrently
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=send_udp_packets, args=(destination, packet_size, interval))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
