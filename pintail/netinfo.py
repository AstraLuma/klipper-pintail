"""
Get local network info
"""
import ipaddress
import socket


def hostname() -> str:
    fqdn = socket.getfqdn()
    if '.' not in fqdn:
        fqdn = f"{fqdn}.local"
    return fqdn


def get_local_addresses():
    return {ipaddress.ip_address(addr[0]) for f, t, p, n, addr in socket.getaddrinfo(None, 80)}


def get_default_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return ipaddress.ip_address(s.getsockname()[0])
