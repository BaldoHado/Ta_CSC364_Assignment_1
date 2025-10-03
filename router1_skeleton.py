import socket
import sys
import time
import os
import glob


# Helper Functions

# The purpose of this function is to set up a socket connection.
def create_socket(host, port):
    soc = socket.socket()
    try:
        soc.connect("127.0.0.1", 6123)
    except:
        print("Connection Error to", port)
        sys.exit()
    return soc


# The purpose of this function is to read in a CSV file.
def read_csv(path):
    table_file = open(path, "r")
    table = table_file.readlines()
    table_list = [[col_val.strip() for col_val in line.split(',')] for line in table]
    table_file.close()
    return table_list


# The purpose of this function is to find the default port
# when no match is found in the forwarding table for a packet's destination IP.
def find_default_gateway(table):
    # 1. Traverse the table, row by row,
    ## for ...:
        # 2. and if the network destination of that row matches 0.0.0.0,
        ## if ...:
            # 3. then return the interface of that row.
            ## return ...


# The purpose of this function is to generate a forwarding table that includes the IP range for a given interface.
# In other words, this table will help the router answer the question:
# Given this packet's destination IP, which interface (i.e., port) should I send it out on?
def generate_forwarding_table_with_range(table):
    # 1. Create an empty list to store the new forwarding table.
    new_table = []
    # 2. Traverse the old forwarding table, row by row,
    ## for ...:
        # 3. and process each network destination other than 0.0.0.0
        # (0.0.0.0 is only useful for finding the default port).
        ## if ...:
            # 4. Store the network destination and netmask.
            ## network_dst_string = ...
            ## netmask_string = ...
            # 5. Convert both strings into their binary representations.
            ## network_dst_bin = ...
            ## netmask_bin = ...
            # 6. Find the IP range.
            ## ip_range = ...
            # 7. Build the new row.
            ## new_row = ...
            # 8. Append the new row to new_table.
            ## new_table.append(new_row)
    # 9. Return new_table.
    return new_table


# The purpose of this function is to convert a string IP to its binary representation.
def ip_to_bin(ip):
    ip_octets = ip.split('.')
    ip_bin_string = ""
    for octet in ip_octets: 
        int_octet = int(octet)
        bin_octet = bin(int_octet)
        bin_octet_string = f"{bin_octet}"[2:]
        bin_octet_string = ("0" * (8-len(bin_octet_string))) + bin_octet_string
        ip_bin_string += bin_octet_string
    return int(ip_bin_string, 2)


# The purpose of this function is to find the range of IPs inside a given a destination IP address/subnet mask pair.
def find_ip_range(network_dst, netmask):
    # 1. Perform a bitwise AND on the network destination and netmask
    # to get the minimum IP address in the range.
    ## bitwise_and = ...
    # 2. Perform a bitwise NOT on the netmask
    # to get the number of total IPs in this range.
    # Because the built-in bitwise NOT or compliment operator (~) works with signed ints,
    # we need to create our own bitwise NOT operator for our unsigned int (a netmask).
    ## compliment = ...
    ## min_ip = ...
    # 3. Add the total number of IPs to the minimum IP
    # to get the maximum IP address in the range.
    ## max_ip = ...
    # 4. Return a list containing the minimum and maximum IP in the range.

    min_ip = network_dst & netmask
    ip_range = bit_not(netmask) 
    max_ip = min_ip | ip_range


    return [min_ip, max_ip]


# The purpose of this function is to perform a bitwise NOT on an unsigned integer.
def bit_not(n, numbits=32):
    return (1 << numbits) - 1 - n


# The purpose of this function is to write packets/payload to file.
def write_to_file(path, packet_to_write, send_to_router=None):


    # 1. Open the output file for appending.
    out_file = open(path, "a")
    # 2. If this router is not sending, then just append the packet to the output file.
    if not send_to_router:
        out_file.write(packet_to_write + "\n")
    # 3. Else if this router is sending, then append the intended recipient, along with the packet, to the output file.
    else:
        out_file.write(packet_to_write + " " + "to Router " + send_to_router + "\n")
    # 4. Close the output file.
    out_file.close()


# Main Program

# 0. Remove any output files in the output directory
# (this just prevents you from having to manually delete the output files before each run).
files = glob.glob('./output/*')
for f in files:
    os.remove(f)

# 1. Connect to the appropriate sending ports (based on the network topology diagram).
## ...
## ...

# 2. Read in and store the forwarding table.
## forwarding_table = ...
# 3. Store the default gateway port.
## default_gateway_port = ...
# 4. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
## forwarding_table_with_range = ...

# 5. Read in and store the packets.
## packets_table = ...

# 6. For each packet,
## for ...:
    # 7. Store the source IP, destination IP, payload, and TTL.
    ## sourceIP = ...
    ## destinationIP = ...
    ## payload = ...
    ## ttl = ...

    # 8. Decrement the TTL by 1 and construct a new packet with the new TTL.
    ## new_ttl = ...
    ## new_packet = ...

    # 9. Convert the destination IP into an integer for comparison purposes.
    ## destinationIP_bin = ...
    ## destinationIP_int = ...

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
