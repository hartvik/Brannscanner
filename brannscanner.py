import ipaddress
import socket

def scan_ports(ip, port_range):
    open_ports = []
    start_port, end_port = port_range
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  
            result = s.connect_ex((str(ip), port))
            print(str(port)) # For testing purpose
            if result == 0:
                open_ports.append(port)
    return open_ports

def scan_network(network_cidr, port_range):
    open_ports_summary = {}
    try:
        network = ipaddress.ip_network(network_cidr)
        
        # Scan IP-addresses in the network
        for ip in network:
            print(ip) # For testing purpose
            try:
                # Get the hostnames
                hostname, _, _ = socket.gethostbyaddr(str(ip))
                
            except socket.herror:
                hostname = 'Not found'
            except Exception as e:
                print(f"IP Address: {ip} -> Error: {e}")
                continue
            
            # Scan ports
            open_ports = scan_ports(ip, port_range)
            if open_ports:
                print(f"IP Address: {ip} -> Hostname: {hostname} -> Open Ports: {open_ports}")
                open_ports_summary[str(ip)] = len(open_ports)
                
    except ValueError as e:
        print(f"Invalid network: {network_cidr}")
        print(f"Error: {e}")
    return open_ports_summary

def input_networks(networks, port_range):
    total_open_ports = 0
    total_hosts_with_open_ports = 0

    for network_cidr in networks:
        print(f"Scanning network: {network_cidr}")
        open_ports_summary = scan_network(network_cidr, port_range)
        
        # Summarize
        num_hosts_with_open_ports = len(open_ports_summary)
        num_open_ports = sum(open_ports_summary.values())
        
        total_hosts_with_open_ports += num_hosts_with_open_ports
        total_open_ports += num_open_ports
        
        print(f"Summary for network {network_cidr}:")
        print(f"  Hosts with open ports: {num_hosts_with_open_ports}")
        print(f"  Total open ports: {num_open_ports}\n")

    print("Overall summary:")
    print(f"  Total hosts with open ports: {total_hosts_with_open_ports}")
    print(f"  Total open ports: {total_open_ports}")

if __name__ == "__main__":
    networks_to_scan = [
        "10.0.0.0/8",
        "192.168.1.0/24"
    ]
    port_range_to_scan = (1, 65535)
    input_networks(networks_to_scan, port_range_to_scan)
