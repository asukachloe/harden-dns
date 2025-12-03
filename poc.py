import socket
import struct
import sys
import requests

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

def send_to_google():
    requests.get('https://google.com')

domains = sys.argv[1:]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('8.8.8.8', 53))
for domain in domains:
    msg = build_query(domain)
    length = len(msg)
    prefix = struct.pack('>H', length)
    sock.sendall(prefix + msg)
sock.close()
send_to_google()
