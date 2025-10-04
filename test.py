from utils import *

table = read_csv('./input/router_1_table.csv')
print(f"Read CSV Table: {table}")

print(f"Default Gateway: {find_default_gateway(table)}")

forwarding_table = generate_forwarding_table_with_range(table)

print(f"Forwarding Table: {forwarding_table}")

print(f"Ip to Bin: {ip_to_bin('127.0.0.1')}")