"""
Get local network info
"""
import ipaddress
import json
import socket
import subprocess


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


def iter_all_interfaces(include_loopback=False):
    proc = subprocess.run(
        ['ip','-json','addr','show'],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        text=True, check=True,
    )
    ipaddr = json.loads(proc.stdout)
    for interface in ipaddr:
        if "LOOPBACK" in interface["flags"] and not include_loopback:
            continue
        if interface["operstate"] == "DOWN":
            continue
        for addr in interface["addr_info"]:
            yield ipaddress.ip_interface(f"{addr['local']}/{addr['prefixlen']}")