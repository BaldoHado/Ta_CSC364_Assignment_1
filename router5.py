import socket
import sys
import traceback
import threading
from utils import (
    create_socket,
    HOST,
    read_csv,
    find_default_gateway,
    generate_forwarding_table_with_range,
    receive_packet,
    process_packet,
)

SERVER_PORT_NUM = 8005
ROUTER_NUM = 5

# The purpose of this function is to
# (a) create a server socket,
# (b) listen on a specific port,
# (c) receive and process incoming packets,
# (d) forward them on, if needed.
def start_server():
    # 1. Create a socket.
    ## host = ...
    ## port = ...
    ## soc = ...

    soc = socket.socket()

    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    # 2. Try binding the socket to the appropriate host and receiving port (based on the network topology diagram).
    try:
        soc.bind(("127.0.0.1", SERVER_PORT_NUM))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    # 3. Set the socket to listen.
    soc.listen()
    print("Socket now listening")

    # 4. Read in and store the forwarding table.
    forwarding_table = read_csv(f"./input/router_{ROUTER_NUM}_table.csv")
    # 5. Store the default gateway port.
    default_gateway_port = find_default_gateway(forwarding_table)
    # 4. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
    forwarding_table_with_range = generate_forwarding_table_with_range(forwarding_table)

    # 7. Continuously process incoming packets.
    while True:
        # 8. Accept the connection.
        connection, address = soc.accept()
        ip, port = address
        print(f"Connected with {ip}:{port}")
        # 9. Start a new thread for receiving and processing the incoming packets.
        try:
            thread = threading.Thread(
                target=processing_thread,
                args=(
                    connection,
                    ip,
                    port,
                    forwarding_table_with_range,
                    default_gateway_port,
                ),
            )
            thread.start()
        except:
            print("Thread did not start.")
            traceback.print_exc()


# The purpose of this function is to receive and process incoming packets.
def processing_thread(
    connection,
    ip,
    port,
    forwarding_table_with_range,
    default_gateway_port,
    max_buffer_size=5120,
):
    while True:
        packet = receive_packet(connection, max_buffer_size, ROUTER_NUM)

        if packet == []:
            break

        process_packet(
            packet,
            default_gateway_port,
            forwarding_table_with_range,
            ROUTER_NUM,
            [],
        )

start_server()
