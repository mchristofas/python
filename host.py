import socket

def read_ips_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_hostnames(ip_list):
    hostnames = {}
    for ip in ip_list:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            hostnames[ip] = hostname
        except socket.herror:
            hostnames[ip] = "Hostname not found"
    return hostnames

def main():
    input_file = "ips.txt"  # Change this to your actual file path
    ip_addresses = read_ips_from_file(input_file)
    results = get_hostnames(ip_addresses)
    
    for ip, hostname in results.items():
        print(f"{ip}: {hostname}")

if __name__ == "__main__":
    main()
