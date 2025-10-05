import socket
import sys
import time
import os
import glob

HOST = "127.0.0.1"

# The purpose of this function is to set up a socket connection.
def create_socket(host, port):
    soc = socket.socket()
    try:
        soc.connect((host, port))
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
    for row in table:
        if row[0] == '0.0.0.0':
            return row[3]


# The purpose of this function is to generate a forwarding table that includes the IP range for a given interface.
# In other words, this table will help the router answer the question:
# Given this packet's destination IP, which interface (i.e., port) should I send it out on?
def generate_forwarding_table_with_range(table):
    new_table = []
    for row in table:
        if row[0] != "0.0.0.0":
            network_dst_string = row[0]
            netmask_string = row[1]
            
            network_dst_bin = ip_to_bin(network_dst_string)
            netmask_bin = ip_to_bin(netmask_string)

            ip_range = find_ip_range(network_dst_bin, netmask_bin)
            new_row = (ip_range, row[3])
            new_table.append(new_row)
    return new_table


# The purpose of this function is to convert a string IP to its binary representation.
def ip_to_bin(ip):
    ip_bin_string = ""

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


# The purpose of this function is to receive and process an incoming packet.
def receive_packet(connection, max_buffer_size, router_num):
    # 1. Receive the packet from the socket.
    received_packet = connection.recv(max_buffer_size).rstrip(b'\x00')
    # 2. If the packet size is larger than the max_buffer_size, print a debugging message
    packet_size = sys.getsizeof(received_packet)
    if packet_size > max_buffer_size:
        print("The packet size is greater than expected", packet_size)
    # 3. Decode the packet and strip any trailing whitespace.
    decoded_packet = received_packet.decode()

    print("received packet", decoded_packet)
    if decoded_packet == "":
        return []
    write_to_file(f"./output/received_by_router_{router_num}.txt", decoded_packet)
    # 4. Split the packet by the delimiter.
    packet = decoded_packet.split(',')
    print("split packet ", packet)
    # 5. Return the list representation of the packet.
    return packet

def process_packet(packet, default_gateway_port, forwarding_table_with_range, current_router_num, target_port_mappings, max_buffer_size=5120):
    sourceIP = packet[0]
    destinationIP = packet[1]
    payload = packet[2]
    ttl = packet[3]
    new_ttl = str(int(ttl)-1)
    new_packet = ','.join([sourceIP, destinationIP, payload, new_ttl])
    print(f"sending packet {new_packet} encoded {new_packet.encode()}")
    destinationIP_int = ip_to_bin(destinationIP)
    port_to_send = None
    for ip_range, target_port in forwarding_table_with_range:
        if ip_range[0] <= destinationIP_int <= ip_range[1]:
            port_to_send = target_port

    if not port_to_send:
        port_to_send = default_gateway_port

    if port_to_send == "127.0.0.1":
        print("OUT:", payload)
        write_to_file(f"./output/out_router_{current_router_num}.txt", payload)
    elif new_ttl == "0":
        print("DISCARD:", new_packet)
        write_to_file(f"./output/discarded_by_router_{current_router_num}.txt", new_packet)
    else:
        for port_num, router_num, router_socket in target_port_mappings:
            if port_to_send == port_num: 
                print(f"sending packet {new_packet} to Router {router_num}")
                write_to_file(f"./output/sent_by_router_{current_router_num}.txt", new_packet, router_num)
                encoded_packet = new_packet.encode()
                padded_packet = encoded_packet.ljust(max_buffer_size, b'\x00')
                router_socket.send(padded_packet)
                break
        else:
            print("DISCARD:", new_packet)
            write_to_file(f"./output/discarded_by_router_{current_router_num}.txt", new_packet)