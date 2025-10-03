import socket
import sys
import traceback
from threading import Thread
from utils import create_socket


# The purpose of this function is to receive and process an incoming packet.
def receive_packet(connection, max_buffer_size):
    # 1. Receive the packet from the socket.
    ## received_packet = ...
    # 2. If the packet size is larger than the max_buffer_size, print a debugging message
    packet_size = sys.getsizeof(received_packet)
    if packet_size > max_buffer_size:
        print("The packet size is greater than expected", packet_size)
    # 3. Decode the packet and strip any trailing whitespace.
    ## decoded_packet = ...
    # 3. Append the packet to received_by_router_2.txt.
    print("received packet", decoded_packet)
    ## ...
    # 4. Split the packet by the delimiter.
    ## packet = ...
    # 5. Return the list representation of the packet.
    return packet



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
        soc.bind('127.0.0.1', SERVER_PORT_NUM)
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    # 3. Set the socket to listen.
    soc.listen()
    print("Socket now listening")

    # 4. Read in and store the forwarding table.
    ## forwarding_table = ...
    # 5. Store the default gateway port.
    ## default_gateway_port = ...
    # 6. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
    ## forwarding_table_with_range = ...

    # 7. Continuously process incoming packets.
    while True:
        # 8. Accept the connection.
        ## connection, address = ...
        ## ip, port = ...
        print("Connected with " + ip + ":" + port)
        # 9. Start a new thread for receiving and processing the incoming packets.
        try:
            ## ...
        except:
            print("Thread did not start.")
            traceback.print_exc()


# The purpose of this function is to receive and process incoming packets.
def processing_thread(connection, ip, port, forwarding_table_with_range, default_gateway_port, max_buffer_size=5120):
    # 1. Connect to the appropriate sending ports (based on the network topology diagram).
    ## ...

    # 2. Continuously process incoming packets
    while True:
        # 3. Receive the incoming packet, process it, and store its list representation
        ## packet = ...

        # 4. If the packet is empty (Router 1 has finished sending all packets), break out of the processing loop
        ## if ...:
            break

        # 5. Store the source IP, destination IP, payload, and TTL.
        ## sourceIP = ...
        ## destinationIP = ...
        ## payload = ...
        ## ttl = ...

        # 6. Decrement the TTL by 1 and construct a new packet with the new TTL.
        ## new_ttl = ...
        ## new_packet = ...

        # 7. Convert the destination IP into an integer for comparison purposes.
        ## destinationIP_bin = ...
        ## destinationIP_int = ...

        # 8. Find the appropriate sending port to forward this new packet to.
        ## ...

        # 9. If no port is found, then set the sending port to the default port.
        ## ...

        # 11. Either
        # (a) send the new packet to the appropriate port (and append it to sent_by_router_2.txt),
        # (b) append the payload to out_router_2.txt without forwarding because this router is the last hop, or
        # (c) append the new packet to discarded_by_router_2.txt and do not forward the new packet
        ## if ...:
            print("sending packet", new_packet, "to Router 3")
            ## ...
        ## elif ...:
            print("sending packet", new_packet, "to Router 4")
            ## ...
        ## elif ...:
            print("OUT:", payload)
            ## ...
        else:
            print("DISCARD:", new_packet)
            ## ...


# Main Program

# 1. Start the server.
start_server()
