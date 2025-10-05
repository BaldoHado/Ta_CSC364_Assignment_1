import socket
import sys
import time
import os
import glob
from utils import (
    create_socket,
    HOST,
    read_csv,
    find_default_gateway,
    generate_forwarding_table_with_range,
    process_packet,
)

# Main Program

# 0. Remove any output files in the output directory
# (this just prevents you from having to manually delete the output files before each run).
files = glob.glob("./output/*")
for f in files:
    os.remove(f)

# 1. Connect to the appropriate sending ports (based on the network topology diagram).

router_2_socket = create_socket(HOST, 8002)
router_4_socket = create_socket(HOST, 8004)

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

    process_packet(
        packet,
        default_gateway_port,
        forwarding_table_with_range,
        1,
        [("8002", "2", router_2_socket), ("8004", "4", router_4_socket)],
    )

    # Sleep for some time before sending the next packet (for debugging purposes)
    time.sleep(1)
