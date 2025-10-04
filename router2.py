import socket
import sys
import traceback
import threading
from utils import create_socket, ip_to_bin, HOST, read_csv, find_default_gateway, generate_forwarding_table_with_range, write_to_file, receive_packet, process_packet

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
        soc.bind(('127.0.0.1', 8002))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    # 3. Set the socket to listen.
    soc.listen()
    print("Socket now listening")

    # 4. Read in and store the forwarding table.
    forwarding_table = read_csv("./input/router_2_table.csv")
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
            thread = threading.Thread(target=processing_thread, args=(connection, ip, port, forwarding_table_with_range, default_gateway_port))
            thread.start()
            thread.join()
        except:
            print("Thread did not start.")
            traceback.print_exc()


# The purpose of this function is to receive and process incoming packets.
def processing_thread(connection, ip, port, forwarding_table_with_range, default_gateway_port, max_buffer_size=5120):
    # 1. Connect to the appropriate sending ports (based on the network topology diagram).

    # router_3_socket = create_socket((HOST, 8003))
    # router_4_socket = create_socket((HOST, 8004))

    # 2. Continuously process incoming packets
    while True:
        # 3. Receive the incoming packet, process it, and store its list representation
        packet = receive_packet(connection, max_buffer_size)

        # 4. If the packet is empty (Router 1 has finished sending all packets), break out of the processing loop
        if packet == []: 
            break

        # process_packet(packet, default_gateway_port, forwarding_table_with_range,2, [("8003", "3"), ("8004", "4")])


            
        # 5. Store the source IP, destination IP, payload, and TTL.
        sourceIP = packet[0]
        destinationIP = packet[1]
        payload = packet[2]
        ttl = packet[3]

        # 6. Decrement the TTL by 1 and construct a new packet with the new TTL.
        new_ttl = str(int(ttl)-1)
        new_packet = ','.join([sourceIP, destinationIP, payload, new_ttl])

        # 7. Convert the destination IP into an integer for comparison purposes.
        destinationIP_int = ip_to_bin(destinationIP)

        # 8. Find the appropriate sending port to forward this new packet to.
        # 9. If no port is found, then set the sending port to the default port.

        port_to_send = default_gateway_port
        for ip_range, target_port in forwarding_table_with_range:
            if ip_range[0] <= destinationIP_int <= ip_range[1]:
                port_to_send = target_port


        # 11. Either
        # (a) send the new packet to the appropriate port (and append it to sent_by_router_2.txt),
        # (b) append the payload to out_router_2.txt without forwarding because this router is the last hop, or
        # (c) append the new packet to discarded_by_router_2.txt and do not forward the new packet
        if port_to_send == "127.0.0.1":
            print("OUT:", payload)
            write_to_file("./output/out_router_2.txt", payload)
        elif new_ttl == "0":
            print("DISCARD:", new_packet)
            write_to_file("./output/discarded_by_router_2.txt", new_packet)
        elif port_to_send == "8003": 
            print("sending packet", new_packet, "to Router 3")
            # router_3_socket.send(new_packet.encode())
            write_to_file("./output/sent_by_router_2.txt", new_packet, "3")
        elif port_to_send == "8004":
            print("sending packet", new_packet, "to Router 4")
            write_to_file("./output/sent_by_router_2.txt", new_packet, "4")
            # router_4_socket.send(new_packet.encode())
        else:
            print("DISCARD:", new_packet)
            write_to_file("./output/discarded_by_router_2.txt", new_packet)


# Main Program

# 1. Start the server.
start_server()
