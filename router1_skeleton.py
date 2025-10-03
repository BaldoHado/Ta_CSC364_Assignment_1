import socket
import sys
import time
import os
import glob
from utils import ip_to_bin, HOST, read_csv, find_default_gateway, generate_forwarding_table_with_range

# Main Program

# 0. Remove any output files in the output directory
# (this just prevents you from having to manually delete the output files before each run).
files = glob.glob('./output/*')
for f in files:
    os.remove(f)

# 1. Connect to the appropriate sending ports (based on the network topology diagram).

router_2_socket = socket.socket((HOST, 8002))
router_4_socket = socket.socket((HOST, 8004))

# 2. Read in and store the forwarding table.
forwarding_table = read_csv("./input/router_1_table.csv")
# 3. Store the default gateway port.
default_gateway_port = find_default_gateway(forwarding_table)
# 4. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
forwarding_table_with_range = generate_forwarding_table_with_range(forwarding_table)

# 5. Read in and store the packets.
packets_table = read_csv("./input/packets.csv")

# 6. For each packet,
for packet in packets_table:
    # 7. Store the source IP, destination IP, payload, and TTL.
    sourceIP = packet[0]
    destinationIP = packet[1]
    payload = packet[2]
    ttl = packet[3]

    # 8. Decrement the TTL by 1 and construct a new packet with the new TTL.
    new_ttl = ttl-1
    new_packet = [sourceIP, destinationIP, payload, new_ttl]

    # 9. Convert the destination IP into an integer for comparison purposes.
    destinationIP_bin = ip_to_bin(destinationIP)
    destinationIP_int = int(destinationIP_bin)

    # 9. Find the appropriate sending port to forward this new packet to.
    ## ...

    # 10. If no port is found, then set the sending port to the default port.
    ## ...

    # 11. Either
    # (a) send the new packet to the appropriate port (and append it to sent_by_router_1.txt),
    # (b) append the payload to out_router_1.txt without forwarding because this router is the last hop, or
    # (c) append the new packet to discarded_by_router_1.txt and do not forward the new packet
    ## if ...:
        print("sending packet", new_packet, "to Router 2")
        ## ...
    ## elif ...
        print("sending packet", new_packet, "to Router 4")
        ## ...
    ## elif ...:
        print("OUT:", payload)
        ## ...
    else:
        print("DISCARD:", new_packet)
        ## ...

    # Sleep for some time before sending the next packet (for debugging purposes)
    time.sleep(1)
